from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import Task
from .serializers import TaskSerializer, TaskAnalysisSerializer
from .scoring import DEFAULT_WEIGHTS, StrategyFactory
from .cycle_detector import detect_cycle


# ----------------------------------------------
# STRATEGY SORTING LOGIC (Critical Thinking Task)
# ----------------------------------------------
def apply_strategy(scored_tasks, mode):
    """
    scored_tasks = list of dicts:
        {
            "task": <Task>,
            "score": float,
            "explanation": "text",
            "estimated_hours": int,
            "importance": int,
            "due_date": "YYYY-MM-DD"
        }
    """

    if mode == "fastest":
        # Smallest effort first
        return sorted(scored_tasks, key=lambda x: x["task"].estimated_hours)

    elif mode == "impact":
        # Highest importance
        return sorted(scored_tasks, key=lambda x: x["task"].importance, reverse=True)

    elif mode == "deadline":
        # Earliest due date
        return sorted(
            scored_tasks,
            key=lambda x: x["task"].due_date if x["task"].due_date else "9999-12-31"
        )

    else:  
        # SMART BALANCED → Score-based sorting
        return sorted(scored_tasks, key=lambda x: x["score"], reverse=True)



# ----------------------------------------------
# MAIN VIEW: ANALYZE TASKS
# ----------------------------------------------
class AnalyzeTasksView(APIView):
    @transaction.atomic
    def post(self, request):
        tasks_data = request.data

        # 1. Validate and save tasks
        serializer = TaskSerializer(data=tasks_data, many=True)
        serializer.is_valid(raise_exception=True)
        tasks = serializer.save()

        # 2. Apply dependencies
        for task_obj, incoming in zip(tasks, tasks_data):
            dep_ids = incoming.get("dependencies", [])
            task_obj.dependencies.set(dep_ids)

        # 3. Detect circular dependencies
        cycle_path = detect_cycle(tasks)
        if cycle_path:
            return Response(
                {
                    "error": {
                        "message": "Circular dependency detected",
                        "details": cycle_path,
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 4. Load weights
        weights = {
            k: float(request.query_params.get(f"w_{k}", DEFAULT_WEIGHTS[k]))
            for k in DEFAULT_WEIGHTS
        }

        # 5. Determine strategy mode
        mode = request.query_params.get("mode", "smart")
        strategy = StrategyFactory.get(mode, weights)

        # 6. Compute scores
        scored = []
        for task in Task.objects.all():
            score, explanation = strategy.score(task)

            scored.append({
                "task": task,
                "score": score,
                "explanation": explanation,
            })

        # 7. Apply sorting strategy (Critical thinking requirement)
        sorted_scored = apply_strategy(scored, mode)

        # 8. Serialize tasks only (structure required by API)
        output = TaskAnalysisSerializer(
            [t["task"] for t in sorted_scored],
            many=True
        ).data

        # 9. Inject score + explanation into final response JSON
        for i, item in enumerate(sorted_scored):
            output[i]["score"] = item["score"]
            output[i]["explanation"] = item["explanation"]

        return Response(output)

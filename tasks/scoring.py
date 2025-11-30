import math
from datetime import date

# Default weights
DEFAULT_WEIGHTS = {
    "urgency": 1.5,
    "importance": 2.0,
    "effort": 1.2,
    "dependencies": 1.8,
}

# -----------------------------------------------------
# Strategy Pattern Base
# -----------------------------------------------------
class ScoringStrategy:
    def score(self, task):
        raise NotImplementedError


# -----------------------------------------------------
# Strategy Implementations
# -----------------------------------------------------
class FastestWinsStrategy(ScoringStrategy):
    def score(self, task):
        score = 1 / (task.estimated_hours + 1)
        explanation = "Prioritized because it is a quick win (low effort)."
        return score, explanation


class HighImpactStrategy(ScoringStrategy):
    def score(self, task):
        score = task.importance
        explanation = "High impact: sorted by importance."
        return score, explanation


class DeadlineDrivenStrategy(ScoringStrategy):
    def score(self, task):
        urgency = calculate_urgency(task)
        explanation = "Deadline driven: urgency based on due date."
        return urgency, explanation


class SmartBalanceStrategy(ScoringStrategy):
    def __init__(self, weights):
        self.weights = weights

    def score(self, task):
        urgency = calculate_urgency(task)
        importance = task.importance
        effort_score = calculate_effort(task)
        dependency_score = task.dependencies.count()



        score = (
            urgency * self.weights["urgency"]
            + importance * self.weights["importance"]
            + effort_score * self.weights["effort"]
            + dependency_score * self.weights["dependencies"]
        )

        explanation = (
            f"Urgency={round(urgency,2)}, Importance={importance}, "
            f"EffortScore={round(effort_score,2)}, DependencyScore={dependency_score}"
        )

        return score, explanation


# -----------------------------------------------------
# Helper functions
# -----------------------------------------------------
def calculate_urgency(task):
    if not task.due_date:
        return 0

    days_left = (task.due_date - date.today()).days

    if days_left < 0:
        return 10
    if days_left == 0:
        return 9

    return max(0, 10 - math.log(days_left + 1))


def calculate_effort(task):
    return 10 / (task.estimated_hours + 1)


# -----------------------------------------------------
# Strategy Factory
# -----------------------------------------------------
class StrategyFactory:
    @staticmethod
    def get(mode, weights):
        if mode == "fastest":
            return FastestWinsStrategy()
        elif mode == "impact":
            return HighImpactStrategy()
        elif mode == "deadline":
            return DeadlineDrivenStrategy()
        return SmartBalanceStrategy(weights)

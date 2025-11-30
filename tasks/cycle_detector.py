def detect_cycle(tasks):
    UNVISITED, VISITING, VISITED = 0, 1, 2
    state = {}

    def dfs(task, path):
        state.setdefault(task.id, UNVISITED)

        if state[task.id] == VISITING:
            # Found a cycle → return cycle path
            cycle_start = path.index(task.id)
            cycle_path = path[cycle_start:] + [task.id]
            return cycle_path

        if state[task.id] == VISITED:
            return None

        state[task.id] = VISITING
        path.append(task.id)

        for dep in task.dependencies.all():
            result = dfs(dep, path)
            if result:
                return result

        state[task.id] = VISITED
        path.pop()
        return None

    for t in tasks:
        path = []
        result = dfs(t, path)
        if result:
            return result  # cycle found

    return None  # no cycle

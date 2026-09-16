from .utils import classes_conflict


def build_conflict_graph(data):
    """Build an undirected conflict graph."""

    classes = data["classes"]

    graph = {
        class_info["id"]: set()
        for class_info in classes
    }

    class_groups = {}

    for group, group_classes in data["student_groups"].items():
        for class_id in group_classes:
            class_groups.setdefault(class_id, set()).add(group)

    for i in range(len(classes)):

        for j in range(i + 1, len(classes)):

            class_a = classes[i]
            class_b = classes[j]

            if classes_conflict(
                class_a,
                class_b,
                data,
                class_groups
            ):
                graph[class_a["id"]].add(class_b["id"])
                graph[class_b["id"]].add(class_a["id"])

    return graph


def welsh_powell(graph, time_slots):
    """Apply the Welsh–Powell graph-colouring algorithm."""

    vertices = sorted(
        graph.keys(),
        key=lambda node: len(graph[node]),
        reverse=True
    )

    colours = {}

    for vertex in vertices:

        used_colours = {
            colours[neighbour]
            for neighbour in graph[vertex]
            if neighbour in colours
        }

        colour = 0

        while colour in used_colours:
            colour += 1

        colours[vertex] = colour

    time_assignment = {}

    for class_id, colour in colours.items():

        if colour < len(time_slots):
            time_assignment[class_id] = time_slots[colour]
        else:
            time_assignment[class_id] = None

    return time_assignment, colours
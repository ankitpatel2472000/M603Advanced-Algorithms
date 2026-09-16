from functools import lru_cache


def optimise_rooms(classes, rooms):
    """
    Dynamic Programming room allocation.

    Each class receives a different room.
    Objective: minimise unused room capacity.
    """

    feasible_rooms = []

    for class_info in classes:

        options = []

        for room in rooms:

            if room["capacity"] >= class_info["students"]:
                waste = (
                    room["capacity"]
                    - class_info["students"]
                )

                options.append((room["id"], waste))

        feasible_rooms.append(options)

    @lru_cache(maxsize=None)
    def dp(index, used_rooms):

        if index == len(classes):
            return 0, {}

        class_info = classes[index]

        best_cost = float("inf")
        best_assignment = None

        for room_id, waste in feasible_rooms[index]:

            if room_id in used_rooms:
                continue

            new_used = tuple(
                sorted(used_rooms + (room_id,))
            )

            remaining_cost, remaining_assignment = dp(
                index + 1,
                new_used
            )

            total_cost = waste + remaining_cost

            if total_cost < best_cost:

                best_cost = total_cost

                best_assignment = {
                    class_info["id"]: room_id,
                    **remaining_assignment
                }

        return best_cost, best_assignment

    cost, assignment = dp(0, tuple())

    return cost, assignment
from .utils import room_is_feasible, classes_conflict


def greedy_schedule(data):
    classes = sorted(
        data["classes"],
        key=lambda x: x["students"],
        reverse=True
    )

    rooms = data["rooms"]
    time_slots = data["time_slots"]

    schedule = {}
    unscheduled = []

    class_groups = {}

    for group, group_classes in data["student_groups"].items():
        for class_id in group_classes:
            class_groups.setdefault(class_id, set()).add(group)

    for current_class in classes:

        assigned = False

        for time_slot in time_slots:

            conflict_found = False

            for existing_id, existing_info in schedule.items():

                if existing_info["time"] != time_slot:
                    continue

                if classes_conflict(
                    current_class,
                    existing_info["class"],
                    data,
                    class_groups
                ):
                    conflict_found = True
                    break

            if conflict_found:
                continue

            for room in rooms:

                if not room_is_feasible(current_class, room):
                    continue

                room_used = any(
                    item["time"] == time_slot
                    and item["room"]["id"] == room["id"]
                    for item in schedule.values()
                )

                if room_used:
                    continue

                schedule[current_class["id"]] = {
                    "class": current_class,
                    "time": time_slot,
                    "room": room
                }

                assigned = True
                break

            if assigned:
                break

        if not assigned:
            unscheduled.append(current_class)

    return schedule, unscheduled
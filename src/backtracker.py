from .utils import (
    classes_conflict,
    room_is_feasible,
    room_waste
)


class BacktrackingScheduler:

    def __init__(self, data):
        self.data = data
        self.classes = data["classes"]
        self.rooms = data["rooms"]
        self.time_slots = data["time_slots"]

        self.class_groups = {}

        for group, group_classes in data["student_groups"].items():
            for class_id in group_classes:
                self.class_groups.setdefault(
                    class_id, set()
                ).add(group)

        self.best_schedule = {}
        self.best_unscheduled = len(self.classes)

    def can_assign(self, class_info, time_slot, room, schedule):
        """Check whether assignment is valid."""

        for item in schedule.values():

            if item["time"] != time_slot:
                continue

            other_class = item["class"]

            if item["room"]["id"] == room["id"]:
                return False

            if classes_conflict(
                class_info,
                other_class,
                self.data,
                self.class_groups
            ):
                return False

        if not room_is_feasible(class_info, room):
            return False

        return True

    def backtrack(self, index, schedule):

        scheduled_count = len(schedule)

        if scheduled_count > len(self.best_schedule):
            self.best_schedule = schedule.copy()

        if index == len(self.classes):
            return True

        current_class = self.classes[index]

        for time_slot in self.time_slots:

            sorted_rooms = sorted(
                self.rooms,
                key=lambda room: room["capacity"]
            )

            for room in sorted_rooms:

                if not self.can_assign(
                    current_class,
                    time_slot,
                    room,
                    schedule
                ):
                    continue

                schedule[current_class["id"]] = {
                    "class": current_class,
                    "time": time_slot,
                    "room": room
                }

                if self.backtrack(
                    index + 1,
                    schedule
                ):
                    return True

                del schedule[current_class["id"]]

        if self.backtrack(index + 1, schedule):
            return True

        return False

    def solve(self):
        self.backtrack(0, {})

        scheduled_ids = set(
            self.best_schedule.keys()
        )

        unscheduled = [
            class_info
            for class_info in self.classes
            if class_info["id"] not in scheduled_ids
        ]

        return self.best_schedule, unscheduled
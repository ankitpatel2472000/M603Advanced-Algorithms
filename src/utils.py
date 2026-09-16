import json


def load_data(file_path):
    """Load scheduling data from JSON."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def build_class_groups(data):
    """Reverse the student-group mapping.

    Returns:
        {
            class_id: set(student_groups)
        }
    """
    class_groups = {}

    for group, classes in data["student_groups"].items():
        for class_id in classes:
            class_groups.setdefault(class_id, set()).add(group)

    return class_groups


def classes_conflict(class_a, class_b, data, class_groups):
    """Return True if two classes cannot share a time slot."""

    if class_a["professor"] == class_b["professor"]:
        return True

    groups_a = class_groups.get(class_a["id"], set())
    groups_b = class_groups.get(class_b["id"], set())

    if groups_a.intersection(groups_b):
        return True

    return False


def room_is_feasible(class_info, room):
    """Check whether a room can accommodate a class."""
    return room["capacity"] >= class_info["students"]


def room_waste(class_info, room):
    """Calculate unused room capacity."""
    return room["capacity"] - class_info["students"]
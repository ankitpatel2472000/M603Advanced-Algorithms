import os

from src.utils import load_data, room_waste
from src.greedy_solver import greedy_schedule
from src.graph_engine import build_conflict_graph, welsh_powell
from src.optimizer import optimise_rooms
from src.backtracker import BacktrackingScheduler


DATA_FILE = os.path.join(
    "data",
    "constraints.json"
)


def print_schedule(title, schedule, unscheduled):

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    total_waste = 0

    for class_id, item in sorted(
        schedule.items()
    ):

        class_info = item["class"]
        room = item["room"]

        waste = room_waste(
            class_info,
            room
        )

        total_waste += waste

        fit_description = (
            "Perfect Fit"
            if waste == 0
            else f"Wasted {waste} seats"
        )

        print(
            f"Scheduled {class_id:<10} "
            f"{item['time']:<8} "
            f"{room['id']:<6} "
            f"{fit_description}"
        )

    for class_info in unscheduled:

        print(
            f"Unscheduled {class_info['id']:<8} "
            f"N/A      N/A    "
            f"No feasible assignment"
        )

    print("-" * 70)
    print(f"Scheduled classes   : {len(schedule)}")
    print(f"Unscheduled classes : {len(unscheduled)}")
    print(f"Room capacity waste : {total_waste}")


def main():

    data = load_data(DATA_FILE)

    
    # STAGE 1 – GREEDY
 
    greedy_result, greedy_unscheduled = greedy_schedule(data)

    print_schedule(
        "STAGE 1 – GREEDY BASELINE",
        greedy_result,
        greedy_unscheduled
    )

    
    # STAGE 2 – CONFLICT GRAPH
    

    graph = build_conflict_graph(data)

    time_assignment, colours = welsh_powell(
        graph,
        data["time_slots"]
    )

    print("\n" + "=" * 70)
    print("STAGE 2 – WELSH–POWELL GRAPH COLOURING")
    print("=" * 70)

    for class_id in sorted(time_assignment):

        print(
            f"{class_id:<10} "
            f"Colour {colours[class_id]:<3} "
            f"Time {time_assignment[class_id]}"
        )

   
    # STAGE 3 – DYNAMIC PROGRAMMING
    

    print("\n" + "=" * 70)
    print("STAGE 3 – DYNAMIC PROGRAMMING ROOM OPTIMISATION")
    print("=" * 70)

    dp_schedule = {}
    dp_unscheduled = []

    classes_by_time = {}

    for class_info in data["classes"]:

        time_slot = time_assignment.get(
            class_info["id"]
        )

        if time_slot is None:
            dp_unscheduled.append(class_info)
            continue

        classes_by_time.setdefault(
            time_slot,
            []
        ).append(class_info)

    for time_slot, classes in classes_by_time.items():

        cost, assignment = optimise_rooms(
            classes,
            data["rooms"]
        )

        if assignment is None:
            dp_unscheduled.extend(classes)
            continue

        for class_info in classes:

            class_id = class_info["id"]
            room_id = assignment.get(class_id)

            if room_id is None:
                dp_unscheduled.append(
                    class_info
                )
                continue

            room = next(
                room for room in data["rooms"]
                if room["id"] == room_id
            )

            dp_schedule[class_id] = {
                "class": class_info,
                "time": time_slot,
                "room": room
            }

    print_schedule(
        "STAGE 3 – DP OPTIMISED SCHEDULE",
        dp_schedule,
        dp_unscheduled
    )

  
    # STAGE 4 – BACKTRACKING
   

    print("\n" + "=" * 70)
    print("STAGE 4 – BACKTRACKING / BEST EFFORT")
    print("=" * 70)

    backtracker = BacktrackingScheduler(data)

    final_schedule, final_unscheduled = (
        backtracker.solve()
    )

    print_schedule(
        "FINAL BEST-EFFORT SCHEDULE",
        final_schedule,
        final_unscheduled
    )

   
    # CONFLICT REPORT
   
    print("\n" + "=" * 70)
    print("CONFLICT REPORT")
    print("=" * 70)

    if not final_unscheduled:

        print(
            "All classes were successfully scheduled."
        )

    else:

        for class_info in final_unscheduled:

            print(
                f"Unscheduled: {class_info['id']} | "
                f"Students: {class_info['students']} | "
                f"Professor: {class_info['professor']} | "
                f"Reason: No feasible assignment found"
            )

    
    # MANUAL FIX LOG
    
    print("\n" + "=" * 70)
    print("MANUAL FIX LOG")
    print("=" * 70)

    if final_unscheduled:

        print(
            "The university manager should review "
            "the unscheduled classes."
        )

        print(
            "Possible interventions include an additional "
            "time slot, larger room, or timetable adjustment."
        )

    else:

        print(
            "No manual intervention is required."
        )


if __name__ == "__main__":
    main()
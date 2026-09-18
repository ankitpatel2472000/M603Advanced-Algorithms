# M603 Advanced Algorithms – Campus Puzzle

## University Timetabling Optimisation System

# Video Link: https://youtu.be/1L8UnCtrSZY

This project implements an algorithmic solution to the "Campus Puzzle"
university timetabling problem for the M603 Advanced Algorithms module.

The system creates a feasible university timetable while considering
student-group conflicts, professor conflicts, room availability and room
capacity. Four algorithmic approaches are implemented and evaluated:

1. Greedy Baseline
2. Welsh–Powell Graph Colouring
3. Dynamic Programming for Room Allocation
4. Recursive Backtracking with Best-Effort Scheduling

The implementation is modular and separates each algorithm into its own
Python component.

---

# 1. Project Objective

The objective of the project is to develop a scheduling system capable of
assigning classes to time slots and lecture rooms while satisfying the
important scheduling constraints.

The system must ensure that:

- A student group is not scheduled for two classes at the same time.
- A professor is not scheduled to teach two classes at the same time.
- A room is not allocated to two classes during the same time slot.
- The assigned room has sufficient seating capacity.
- Room-capacity waste is minimised where possible.
- Classes that cannot be scheduled are clearly reported for manual
  intervention.

The project follows a staged algorithmic approach so that the performance
and limitations of different algorithms can be examined.

---

# 2. Repository Structure

```text
M603-Campus-Puzzle/
│
├── data/
│   └── constraints.json
│
├── src/
│   ├── __init__.py
│   ├── utils.py
│   ├── greedy_solver.py
│   ├── graph_engine.py
│   ├── optimizer.py
│   └── backtracker.py
│
├── main.py
├── README.md
└── requirements.txt

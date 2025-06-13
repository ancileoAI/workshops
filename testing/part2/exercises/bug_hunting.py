# Challenge 1: Bug Hunt
# Instructions:
# 1. Read the TaskManager code below
# 2. Find at least 5 bugs, logic issues, or bad practices
# 3. Write down the problems and suggest fixes
# 4. Bonus: Write test cases that would catch the bugs
#
# Time: 15 minutes bug hunt, 5 minutes group share

import pytest
from typing import List, Optional
import datetime


class Task:
    created_at = datetime.datetime.now()

    def __init__(self, id: int, title: str, deadline: Optional[datetime.date] = None):
        self.id = id
        self.title = title
        self.deadline = deadline
        self.completed = False

    def mark_complete(self):
        self.completed = True

    def __str__(self):
        return f"[{'X' if self.completed else ' '}] {self.title} (Due: {self.deadline})"


class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, title: str, deadline: Optional[datetime.date] = None):
        task_id = len(self.tasks) + 1
        task = Task(task_id, title, deadline)
        self.tasks.append(task)

    def remove_task(self, task_id: int):
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                return True
        return False

    def mark_complete(self, task_id: int):
        for task in self.tasks:
            if task.id == task_id:
                task.mark_complete()
                return True

    def overdue_tasks(self):
        today = datetime.date.today()
        overdue = []
        for task in self.tasks:
            if task.deadline and task.deadline < today:
                overdue.append(task)
        return overdue

    def upcoming_tasks(self, within_days: int = 7):
        today = datetime.date.today()
        upcoming = []
        for task in self.tasks:
            if task.deadline and 0 <= (task.deadline - today).days <= within_days:
                upcoming.append(task)
        return upcoming

    def list_tasks(self, include_completed: bool = True):
        return [task for task in self.tasks if include_completed or not task.completed]


# Sample run
if __name__ == "__main__":
    manager = TaskManager()

    manager.add_task("Write report", datetime.date.today() +
                     datetime.timedelta(days=3))
    manager.add_task("Buy groceries")
    manager.add_task("Call Alice", datetime.date.today() -
                     datetime.timedelta(days=1))

    manager.mark_complete(2)

    print("\nAll Tasks:")
    for task in manager.list_tasks():
        print(task)

    print("\nIncomplete Tasks:")
    for task in manager.list_tasks(include_completed=False):
        print(task)

    print("\nOverdue Tasks:")
    for task in manager.overdue_tasks():
        print(task)

    print("\nUpcoming Tasks (next 5 days):")
    for task in manager.upcoming_tasks():
        print(task)

    print("\nTrying to remove non-existent task:")
    result = manager.remove_task(99)
    print("Success:", result)

    print("\nAdding task with past deadline:")
    manager.add_task("Old Task", datetime.date.today() -
                     datetime.timedelta(days=10))
    print("Done.")

# List the bugs you found below:
#
# Bug 1:
# Issue: ________________________________________________
# Location: __________________________________________
# Fix: _______________________________________________

import pytest
import datetime
import time

from testing.part2.exercises.bug_hunting import TaskManager

TODAY = datetime.date.today()


@pytest.fixture
def manager():
    return TaskManager()


class TestBuggyBehavior:
    def test_add_task_with_past_deadline(self, manager):
        past = TODAY - datetime.timedelta(days=1)
        manager.add_task("Task with past deadline", deadline=past)

        with pytest.raises(ValueError):
            manager.add_task("Task with past deadline", deadline=past)

    def test_add_task_with_duplicate_title_raises(self, manager):
        manager.add_task("Unique")
        with pytest.raises(ValueError):
            manager.add_task("Unique")

    def test_mark_complete_nonexistent_task_raises(self, manager):
        with pytest.raises(ValueError):
            manager.mark_complete(999)

    def test_task_ids_unique_per_task(self, manager):
        manager.add_task("Test A")
        manager.add_task("Test B")
        manager.remove_task(1)
        manager.add_task("Test C")  # Should get new ID
        ids = [task.id for task in manager.tasks]
        assert len(set(ids)) == len(
            ids), "Task IDs should be unique and non-reused"

    def test_overdue_tasks_includes_completed(self, manager):
        manager.add_task("Incomplete task", TODAY - datetime.timedelta(days=1))
        task_id = manager.tasks[0].id
        manager.mark_complete(task_id)
        overdue = manager.overdue_tasks()
        # Completed task should not be in overdue_tasks
        assert all(
            not t.completed for t in overdue), "Completed tasks included in overdue_tasks"

    def test_mark_complete_nonexistent_id_returns_false(self, manager):
        result = manager.mark_complete(9999)
        assert result is False

    def test_add_task_with_empty_title(self, manager):
        # Check that empty titles are handled (ideally should reject or raise)
        manager.add_task("")
        assert manager.tasks[0].title != "", "Empty title task added"

    def test_id_generation_not_robust(self, manager):
        manager.add_task("Task 1")
        manager.add_task("Task 2")
        manager.remove_task(1)
        manager.add_task("Task 3")

        ids = [task.id for task in manager.tasks]
        # IDs should be unique and new ID should not reuse removed ID
        assert len(ids) == len(
            set(ids)), "Task IDs are reused after removal (Bug 1)"

    def test_invalid_deadline_type(self, manager):
        past_date = TODAY - datetime.timedelta(days=10)
        # Adding with invalid type should raise error
        with pytest.raises(TypeError):
            manager.add_task("Invalid deadline task", deadline="yesterday")

    def test_removing_nonexistent_task_fails_silently(self, manager):
        with pytest.raises(ValueError):
            manager.remove_task(9999)

    def test_created_timestamp_is_not_same(self, manager):
        manager.add_task("Task with created_at")
        task1 = manager.tasks[0]

        time.sleep(0.01)

        manager.add_task("Task 2")
        task2 = manager.tasks[1]
        assert task1.created_at != task2.created_at

    def test_mark_complete_runs_once(self, manager):
        manager.add_task("Task to complete twice")
        task_id = manager.tasks[0].id
        result1 = manager.mark_complete(task_id)
        result2 = manager.mark_complete(task_id)

        # Ideally second call should raise or return False; here we test it's consistent
        assert result1 is True, "First mark_complete call failed unexpectedly"
        assert result2 is False, "Second mark_complete call behaves inconsistently"

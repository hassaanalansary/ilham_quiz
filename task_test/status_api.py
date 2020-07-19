from __future__ import annotations
import abc


class Status(abc.ABC):
    """any class that inherit from this class has to implement all the methods below
    should never call object.save() as it will trigger infinite loop
    """

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return str(self)

    def edit_title(self, task, new_title):
        # will approve the change bey letting it pass or raise exception
        raise NotImplementedError('')

    def edit_description(self, task, new_description):
        raise NotImplementedError('')

    def link_task(self, task, other_task):
        raise NotImplementedError('')

    def mark_as_in_progress(self, task):
        """alternative to edit_status and easier to read for developers"""
        raise NotImplementedError('')

    def mark_as_done(self, task):
        """alternative to edit_status and easier to read for developers"""
        raise NotImplementedError('')

    def edit_status(self, task, status):
        raise NotImplementedError('')


class New(Status):

    def edit_title(self, task, new_title):
        task.title = new_title

    def edit_description(self, task, new_description):
        task.description = new_description

    def link_task(self, task, other_task):
        """I assumed that this operation is forbidden while in New status."""
        raise ValueError("cannot link_task in 'New' status")

    def mark_as_in_progress(self, task):
        task._status = task.IN_PROGRESS

    def mark_as_done(self, task):
        raise ValueError("cannot change status to done without being InProgress first, "
                         "try running mark_as_in_progress()")

    def edit_status(self, task, status):
        if status == task.IN_PROGRESS:
            self.mark_as_in_progress(task)
        elif status == task.DONE:
            self.mark_as_done(task)
        else:
            raise ValueError(f"Unaccepted status, should be in {task.STATUS_LIST}")


class InProgress(Status):

    def edit_title(self, task, new_title):
        """I assumed that this operation is forbidden while in InProgress status."""
        raise ValueError("cannot edit title in 'In Progress' status")

    def edit_description(self, task, new_description):
        """I assumed that this operation is forbidden while in InProgress status."""
        raise ValueError("cannot edit description in 'In Progress' status")

    def link_task(self, task, other_task):
        task.linked_tasks.add(other_task)

    def mark_as_in_progress(self, task):
        print("Warning: status is already InProgress")  # should be written in a logger

    def mark_as_done(self, task):
        task._status = task.DONE

    def edit_status(self, task, status):
        if status == task.IN_PROGRESS:
            self.mark_as_in_progress(task)
        elif status == task.DONE:
            self.mark_as_done(task)
        else:
            raise ValueError(f"Unaccepted status, should be in {task.STATUS_LIST}")


class Done(Status):

    def edit_title(self, task, new_title):
        raise ValueError("cannot edit_title in 'Done' status")

    def edit_description(self, task, new_description):
        raise ValueError("cannot edit_description in 'Done' status")

    def link_task(self, task, other_task):
        raise ValueError("cannot link_task in 'Done' status")

    def mark_as_in_progress(self, task):
        raise ValueError("status cannot changed back to InProgress after being Done")

    def mark_as_done(self, task):
        print("Warning: status is already Done")  # should be written in a logger

    def edit_status(self, task, status):
        if status == task.IN_PROGRESS:
            self.mark_as_in_progress(task)
        elif status == task.DONE:
            self.mark_as_done(task)
        else:
            raise ValueError(f"Unaccepted status, should be in {task.STATUS_LIST}")

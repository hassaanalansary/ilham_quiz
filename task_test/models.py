from __future__ import annotations
from django.db import models
from task_test import status_api


class Task(models.Model):
    """
        I made sure to put my logic on the lowest possible level, not in serializers nor views
        to keep my serializers and views simple
        so even other developers don't bypass the state constraints
    """
    NEW = 0
    IN_PROGRESS = 1
    DONE = 2

    STATUS_LIST = [
        (NEW, 'New'),
        (IN_PROGRESS, 'In Progress'),
        (DONE, 'Done')
    ]

    STATUS_MAPPING = {
        NEW: status_api.New(),
        IN_PROGRESS: status_api.InProgress(),
        DONE: status_api.Done()
    }
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    _status = models.IntegerField(choices=STATUS_LIST, default=NEW)
    linked_tasks = models.ManyToManyField('Task', blank=True)

    def __str__(self):
        return self.title

    @property
    def status(self):
        """to prevent from changing status manually
        should not be changed manually, use the appropriate status method
        """
        return self.STATUS_MAPPING[self._status]

    def save(self, *args, **kwargs):
        """pass any change first on status manager and make sure that the change doesn't violate it."""
        self.full_clean()  # to enforce choices when an object gets created, which is not enforced by default
        old = Task.objects.filter(id=self.id).first()  # get old value (if any) before update for comparison
        if old:
            if old.title != self.title:
                self.status.edit_title(self, self.title)
            if old.description != self.description:
                self.status.edit_description(self, self.description)
            if old._status != self._status:
                old.status.edit_status(old, self._status)

        super().save(*args, **kwargs)

    def link_task(self, other_task: Task):
        """ add other_task to self.linked_tasks"""
        if not isinstance(other_task, Task):
            raise TypeError(f"other_task should be {self.__class__}. {type(other_task)} is not {self.__class__}")
        self.status.link_task(self, other_task)

    def mark_as_in_progress(self):
        return self.status.mark_as_in_progress(self)

    def mark_as_done(self):
        self.status.mark_as_done(self)

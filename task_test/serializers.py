from rest_framework import serializers

from task_test.models import Task


class TaskSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(source='_status')

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'linked_tasks',
        ]

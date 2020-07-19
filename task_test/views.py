from rest_framework import viewsets
from task_test import serializers, models
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer

    @action(detail=True, methods=['post'])
    def link(self, request, pk):
        """
        Link two tasks together based on the parent task state.
        """
        task = self.get_object()
        other_task = models.Task.objects.get(pk=pk)
        task.link_task(other_task)

        serialized_data = self.serializer_class(task)
        return Response(serialized_data, status=status.HTTP_200_OK)

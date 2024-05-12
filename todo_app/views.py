from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task  # Importing the Task model from models.py
from .serializers import TaskSerializer  # Importing the TaskSerializer from serializers.py

#  handle GET requests for retrieving all tasks
@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all() 
    serializer = TaskSerializer(tasks, many=True)  # Serialize the queryset
    return Response(serializer.data)  # Return serialized data as a response

#  handle POST requests for creating a new task
@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)  # Deserialize request data
    if serializer.is_valid():  
        serializer.save()  
        return Response(serializer.data, status=201)  # Return serialized data with 201 Created status
    return Response(serializer.errors, status=400)  # Return errors with 400 Bad Request status if data is invalid

#  handle PUT and PATCH requests for updating a task
@api_view(['PUT', 'PATCH'])
def update_task(request, pk):  # pk is the primary key of the task to be updated
    try:
        task = Task.objects.get(pk=pk)  # Retrieve the task object by primary key
    except Task.DoesNotExist:  # Handle case where task does not exist
        return Response(status=404)  # Return 404 Not Found if task does not exist
    
    serializer = TaskSerializer(task, data=request.data, partial=True)  # Deserialize request data with partial update
    if serializer.is_valid():  
        serializer.save()  
        return Response(serializer.data)  # Return serialized data
    return Response(serializer.errors, status=400)  # Return errors with 400 Bad Request status if data is invalid

#handle DELETE requests for deleting a task
@api_view(['DELETE'])
def delete_task(request, pk):  # pk is the primary key of the task to be deleted
    try:
        task = Task.objects.get(pk=pk)  # Retrieve the task object by primary key
    except Task.DoesNotExist:  # Handle case where task does not exist
        return Response(status=404)  # Return 404 Not Found if task does not exist
    
    task.delete() 
    return Response(status=204)  # Return 204 No Content upon successful deletion

'''
Response(status=200): Used in task_list function to indicate successful retrieval of tasks.
Response(status=201): Used in create_task function to indicate successful creation of a new task.
Response(status=204): Used in delete_task function to indicate successful deletion of a task.
Response(status=400): Used in create_task and update_task functions to indicate client error, such as invalid data.
Response(status=404): Used in update_task and delete_task functions to indicate that the requested task does not exist.

'''
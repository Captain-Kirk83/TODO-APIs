from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
import json
from .permissions import *

"""
TODO:
Create the appropriate View classes for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""


class TodoCreateView(generics.GenericAPIView):
    """
    TODO:
    Currently, the /todo/create/ endpoint returns only 200 status code,
    after successful Todo creation.

    Modify the below code (if required), so that this endpoint would
    also return the serialized Todo data (id etc.), alongwith 200 status code.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def post(self, request):
        """
        Creates a Todo entry for the logged in user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        todo=Todo.objects.filter(title=serializer.validated_data['title'])
        show=TodoCreateSerializer(todo[0])
        return Response(show.data, status=status.HTTP_200_OK)


class TodoListView(generics.ListAPIView):
    
    permission_classes = [permissions.IsAuthenticated, IsCreator]
    serializer_class = TodoListSerializer

    def get(self,request):
        todos=Todo.objects.filter(creator=request.user)
        for todo in todos:
            todo.role="creator"
            todo.save()
        for obj in Todo.objects.all():
            if request.user in obj.collaborators.all():
                obj.role="collaborator"
                obj.save()
                todos = todos | Todo.objects.filter(id=obj.id)
        #todos = todos1 | todos2
        print(todos)
        serializer=TodoListSerializer(todos, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)


class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrCollaborator]
    serializer_class = TodoDetailSerializer


    def get(self, request, id):
        try:
            todo=Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, todo)
        
        serializer=TodoDetailSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        data=JSONParser().parse(request)
        try:
            todo=Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request,todo)
        serializer=TodoDetailSerializer(todo, data=data)
        if serializer.is_valid():
            serializer.save()
            todo1=TodoDetailSerializer(todo)
            return Response(todo1.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, id):
        data=JSONParser().parse(request)
        try:
            todo=Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request,todo)
        serializer=TodoDetailSerializer(todo, data=data)
        if serializer.is_valid():
            serializer.save()
            todo1=TodoDetailSerializer(todo)
            return Response(todo1.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        try:
            todo=Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request,todo)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TodoAddCollabView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCreator]
    serializer_class = CollaboratorSerializer

    def put(self, request, id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        try:
            todo=Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request,todo)
        todo.collaborators.add(user)
        serializer = TodoDetailSerializer(todo)
        print(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
        #else:
        #    return Response(status=status.HTTP_207_MULTI_STATUS)


class TodoDeleteCollabView(generics.GenericAPIView):
    permission_classes=[permissions.IsAuthenticated, IsCreator]
    serializer_class=CollaboratorSerializer

    def post(self,request,id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        try:
            todo=Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request,todo)
        collab=todo.collaborators.all()
        #print(user in collab)
        #return Response(status=status.HTTP_200_OK)
        if user in collab:
            todo.collaborators.remove(user)
            serializer = TodoDetailSerializer(todo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
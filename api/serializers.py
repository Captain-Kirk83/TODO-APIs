from rest_framework import serializers, exceptions
from .models import *
from django.contrib.auth.models import User


"""
TODO:
Create the appropriate Serializer class(es) for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""


class TodoCreateSerializer(serializers.ModelSerializer):
    """
    TODO:
    Currently, the /todo/create/ endpoint returns only 200 status code,
    after successful Todo creation.

    Modify the below code (if required), so that this endpoint would
    also return the serialized Todo data (id etc.), alongwith 200 status code.
    """
    def save(self, **kwargs):
        data = self.validated_data
        user = self.context['request'].user
        title = data['title']
        todo = Todo.objects.create(creator=user, title=title)
    
    class Meta:
        model = Todo
        fields = ['id', 'title']


class TodoListSerializer(serializers.ModelSerializer):

    class Meta:
        model=Todo
        fields=['id','title','role']


class TodoDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model=Todo
        fields=['id','title', 'collaborators']




class CollaboratorSerializer(serializers.Serializer):
    collab=serializers.CharField(max_length=150)

    def validate(self, attrs):
        username=attrs['collab']
        if username:
            user=User.objects.filter(username=username)
            if user:
                attrs['user']=user[0]
            else:
                message='User does not exist'
                raise exceptions.ValidationError(message)
        else:
            message='No username given as input'
            raise exceptions.ValidationError(message)
        return super().validate(attrs)
from rest_framework.permissions import BasePermission
from .models import *

class IsCreator(BasePermission):

    def has_object_permission(self, request, view, obj):
        print("checkpoint")
        return obj.creator == request.user


class IsCreatorOrCollaborator(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.user in obj.collaborators.all()) or (obj.creator == request.user) 


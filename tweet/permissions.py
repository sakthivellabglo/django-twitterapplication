from rest_framework.permissions import BasePermission, IsAuthenticated
from .views import ListPublicTweetsView,CreateDeleteLikeView


class IsAuthenticatedOrPublicAvailable(IsAuthenticated):

    def has_permission(self, request, view):
       
        if isinstance(view, (ListPublicTweetsView, )):
            return True

        return request.user and request.user.is_authenticated


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if isinstance(view, (CreateDeleteLikeView, )):
            return str(obj.author.id) == str(request.user)

        return obj.owner == request.user
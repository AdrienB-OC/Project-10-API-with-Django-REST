from rest_framework import permissions
from .models import Contributor

UNSAFE_METHODS = ['PUT', 'DELETE']


def is_contrib(view_kwargs, request):
    try:
        p_id = view_kwargs['project_pk']
    except:
        p_id = view_kwargs['pk']

    try:
        contrib = Contributor.objects.get(
            project_id=p_id,
            user_id=request.user)
    except:
        contrib = None

    return contrib is not None


class IsAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        if not view.kwargs:
            return True

        permission = is_contrib(view.kwargs, request)
        return permission

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            permission = is_contrib(view.kwargs, request)
            return permission

        try:
            return obj.author_user_id == request.user
        except:
            return obj.project_id.author_user_id == request.user

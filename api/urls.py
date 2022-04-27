from django.urls import path, include
from .views import ProjectUpdateDeleteView, IssueViewset, CommentViewset, \
    ContributorViewset
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'project', ProjectUpdateDeleteView, basename="project")

users_router = routers.NestedSimpleRouter(router, r'project',
                                          lookup='project')
users_router.register(r'users', ContributorViewset, basename='users')

project_router = routers.NestedSimpleRouter(router, r'project',
                                            lookup='project')
project_router.register(r'issue', IssueViewset, basename='issue')

issue_router = routers.NestedSimpleRouter(project_router, r'issue',
                                          lookup='issue')
issue_router.register(r'comment', CommentViewset, basename='comment')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(project_router.urls)),
    path(r'', include(issue_router.urls)),
    path(r'', include(users_router.urls)),
]

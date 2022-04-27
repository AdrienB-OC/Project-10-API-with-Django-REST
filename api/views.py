from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, \
    IssueSerializer, CommentSerializer, ProjectSerializerGet, \
    IssueSerializerPost, CommentSerializerPost, ContributorSerializerPost
from .permissions import IsAuthor

from authentication.models import User


class ProjectUpdateDeleteView(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_queryset(self):
        contributors = Contributor.objects.filter(user_id=self.request.user)
        pk_list = []
        print(contributors)
        for contrib in contributors:
            pk_list.append(contrib.project_id.pk)
        queryset = Project.objects.all().filter(pk__in=pk_list)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProjectSerializerGet
        return ProjectSerializer

    def get(self, **kwargs):
        context = {}
        obj = Project.objects.all().filter(pk=kwargs['pk'])
        obj = obj[0]

        context['author_user_id'] = obj.author_user_id.pk
        context['title'] = obj.title
        context['description'] = obj.description
        context['type'] = obj.type

        return Response(context, status=200)

    def perform_create(self, serializer):
        serializer.save(author_user_id=self.request.user)
        last = Project.objects.last()
        Contributor.objects.create(user_id=self.request.user,
                                   project_id=last,
                                   role='Project Creator')

    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, pk):
        project = self.get_object(pk)
        project.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ContributorSerializerPost

        return ContributorSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_pk']
        queryset = Contributor.objects.filter(project_id=project_id)

        return queryset

    def perform_create(self, serializer):
        project_id = self.kwargs['project_pk']
        project = Project.objects.get(pk=project_id)

        user_id = self.request.data['email']
        user = User.objects.get(email=user_id)

        serializer.save(user_id=user, project_id=project)

    def delete(self, pk):
        contributor = Contributor.objects.get(pk=pk)
        contributor.delete()


class IssueViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return IssueSerializerPost
        return IssueSerializer

    def get_queryset(self):
        queryset = Issue.objects.all()
        project_id = self.kwargs['project_pk']

        if project_id is not None:
            queryset = Issue.objects.filter(project_id=project_id)

        return queryset

    def perform_create(self, serializer, **kwargs):
        p_id = self.kwargs['project_pk']
        project = Project.objects.get(pk=p_id)

        assignee_id = self.request.data['assignee_user_id']
        assignee = User.objects.get(email=assignee_id)

        serializer.save(project_id=project,
                        author_user_id=self.request.user,
                        assignee_user_id=assignee)

    def put(self, request, pk):
        if pk is None:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        project = self.get_object(pk)
        serializer = IssueSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, pk):
        issue = self.get_object(pk)
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return CommentSerializerPost
        return CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        issue_id = self.kwargs['issue_pk']

        if issue_id is not None:
            queryset = Comment.objects.filter(issue_id=issue_id)

        return queryset

    def get(self, **kwargs):
        context = {}
        obj = Issue.objects.all().filter(pk=kwargs['pk'])
        obj = obj[0]
        context['description'] = obj.description
        context['author_user_id'] = obj.author_user_id.pk
        context['issue_id'] = obj.issue_id
        context['created_time'] = obj.created_time

        return Response(context, status=200)

    def perform_create(self, serializer):
        issue_id = self.kwargs['issue_pk']
        issue = Issue.objects.get(pk=issue_id)
        try:
            Contributor.objects.get(user_id=self.request.user,
                                    project_id=issue.project_id)
        except:
            raise PermissionError({"detail": "Vous n'êtes pas contributeur "
                                             "de ce projet"})

        serializer.save(author_user_id=self.request.user, issue_id=issue)

    def put(self, request, pk):
        if pk is None:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, pk):
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

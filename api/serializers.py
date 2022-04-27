from rest_framework.serializers import ModelSerializer

from .models import Contributor, Project, Issue, Comment
from authentication.serializers import UserSerializer


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['title', 'description', 'type']


class ProjectSerializerGet(ModelSerializer):
    author_user_id = UserSerializer()

    class Meta:
        model = Project
        fields = ['author_user_id', 'title', 'description', 'type']


class ContributorSerializer(ModelSerializer):
    user_id = UserSerializer()

    class Meta:
        model = Contributor
        fields = '__all__'


class ContributorSerializerPost(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['role']


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class IssueSerializerPost(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['title', 'desc', 'tag', 'priority', 'status']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializerPost(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['description']

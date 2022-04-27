from django.db import models
from authentication.models import User


class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=128)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Contributor(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=128)

    class Meta:
        unique_together = ('user_id', 'project_id', )


class Issue(models.Model):
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=255)
    tag = models.CharField(max_length=128)
    priority = models.CharField(max_length=128)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=128)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                       related_name="author")
    assignee_user_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                         related_name="assignee")
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

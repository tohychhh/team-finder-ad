from django.contrib.auth import get_user_model
from django.db import models

from team_finder.constants import (MAX_LENGTH_PROJECT_NAME, MAX_LENGTH_SKILL_NAME,
                                   STATUS_CHOICES, STATUS_OPEN)

User = get_user_model()


class Skill(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_SKILL_NAME, unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_PROJECT_NAME)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    github_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default=STATUS_OPEN)
    participants = models.ManyToManyField(User, related_name='participated_projects', blank=True)
    skills = models.ManyToManyField(Skill, related_name='projects', blank=True)

    def __str__(self):
        return self.name
    
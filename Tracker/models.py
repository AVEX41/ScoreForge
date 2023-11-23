from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_picture = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.username


class ScoreTable(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="score_tables"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    user_favourite = models.BooleanField()

    def __str__(self):
        return f"{self.name} - {self.user.username}"


class ScoreSet(models.Model):
    score_table = models.ForeignKey(
        ScoreTable, on_delete=models.CASCADE, related_name="score_sets"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ScoreSet - {self.id} - {self.timestamp}"


class ScoreNode(models.Model):
    score_set = models.ForeignKey(
        ScoreSet, on_delete=models.CASCADE, related_name="score_nodes"
    )
    score = models.FloatField()
    inner = models.BooleanField()

    def __str__(self):
        return f"ScoreNode - {self.id} - Score: {self.score}, Inner: {self.inner}"

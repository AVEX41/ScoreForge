from django.core.serializers import serialize
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import JsonResponse
import json


class User(AbstractUser):
    def __str__(self):
        return self.username


class ScoreTable(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="score_tables"
    )  # adding the user
    timestamp = models.DateTimeField(auto_now_add=True)  # when
    name = models.CharField(max_length=100)  # name of the table
    description = models.CharField(max_length=500)  # description of the table
    user_favourite = models.BooleanField()  # is it a user favourite
    shots_count = models.IntegerField(null=True)  # how many shots/nodes per set

    def __str__(self):
        return f"{self.name} - {self.user.username}"

    def serialize_score_sets(self):  # serializer
        score_sets = self.score_sets.all()
        serialized_score_sets = serialize("json", score_sets)
        return json.loads(serialized_score_sets)


class ScoreSet(models.Model):
    score_table = models.ForeignKey(
        ScoreTable, on_delete=models.CASCADE, related_name="score_sets"
    )  # linking to the mother/table
    timestamp = models.DateTimeField(auto_now_add=True)  # when
    int_score = models.IntegerField()  # the total score of the set
    decimal_score = models.FloatField()  # total score of the set in decimal
    total_inners = models.IntegerField()  # total inners

    def __str__(self):
        return f"ScoreSet - {self.id} - {self.timestamp}"


class ScoreNode(models.Model):
    score_set = models.ForeignKey(
        ScoreSet, on_delete=models.CASCADE, related_name="score_nodes"
    )  # linking to the mother/table
    score = models.FloatField()  # the score of the shot
    inner = models.BooleanField()  # was it an inner

    def __str__(self):
        return f"ScoreNode - {self.id} - Score: {self.score}, Inner: {self.inner}"

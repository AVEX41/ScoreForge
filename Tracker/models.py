from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import JsonResponse
import json


class User(AbstractUser):
    def __str__(self):
        return self.username

    def serialize_performance_indicators(self):  # returns all the PerformanceIndicators
        competitions = self.performance_indicators.all().values(
            "id", "name", "timestamp", "description", "shots_count"
        )

        # Convert datetime objects to strings
        competitions = list(competitions)
        for competition in competitions:
            competition["timestamp"] = competition["timestamp"].strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        serialized_competitions = json.dumps(competitions, cls=DjangoJSONEncoder)
        return json.loads(serialized_competitions)


class PerformanceIndicator(models.Model):
    id = models.AutoField(primary_key=True)  # id
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="performance_indicators"
    )  # adding the user
    timestamp = models.DateTimeField(auto_now_add=True)  # when
    name = models.CharField(max_length=100)  # name of the table
    description = models.CharField(max_length=500)  # description of the table
    user_favourite = models.BooleanField()  # is it a user favourite
    shots_count = models.IntegerField(null=True)  # how many shots/nodes per set

    def __str__(self):
        return f"{self.name} - {self.user.username}"

    def serialize_performance_indicator(self):  # serializer
        score_sets = self.data_points.all()
        serialized_score_sets = serialize("json", score_sets)
        return json.loads(serialized_score_sets)


class DataPoint(models.Model):
    id = models.AutoField(primary_key=True)  # id
    score_table = models.ForeignKey(
        PerformanceIndicator, on_delete=models.CASCADE, related_name="data_points"
    )  # linking to the mother/table
    timestamp = models.DateTimeField(auto_now_add=True)  # when
    nbr = models.IntegerField()  # the number identifier inside the table
    int_score = models.IntegerField()  # the total score of the set
    decimal_score = models.FloatField(blank=True)  # total score of the set in decimal
    total_inners = models.IntegerField()  # total inners

    def __str__(self):
        return f"ScoreSet - {self.id} - {self.timestamp}"

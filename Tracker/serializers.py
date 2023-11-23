from rest_framework import serializers
from .models import ScoreTable, ScoreSet, ScoreNode


class ScoreNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreNode
        fields = ("shotNumber", "score", "inner")


class ScoreSetSerializer(serializers.ModelSerializer):
    score = ScoreNodeSerializer(many=True, read_only=True)

    class Meta:
        model = ScoreSet
        fields = ("date", "score")


class ScoreTableSerializer(serializers.ModelSerializer):
    score = ScoreSetSerializer(many=True, read_only=True)

    class Meta:
        model = ScoreTable
        fields = ("name", "description", "score")

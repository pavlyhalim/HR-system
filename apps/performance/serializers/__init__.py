from rest_framework import serializers

from apps.performance.models import (
    BiasDetectionResult,
    CalibrationSession,
    FinalRating,
    GoalCascade,
    PerformanceFramework,
    PerformanceReview,
    ReviewCycle,
)


class PerformanceFrameworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceFramework
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class ReviewCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewCycle
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class GoalCascadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalCascade
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class PerformanceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceReview
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class BiasDetectionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiasDetectionResult
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class CalibrationSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalibrationSession
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class FinalRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalRating
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

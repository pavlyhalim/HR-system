from rest_framework import serializers

from apps.oma.models import (
    OMABenchmark,
    OMABenchmarkDataset,
    OMADomainScore,
    OMAGap,
    OMAMaturityLevel,
    OMANormalizedData,
    OMARisk,
    OMARoadmap,
    OMAStrategyExport,
    OMASurvey,
    OMASurveyQuestion,
    OMASurveyResponse,
    OMAValidationResult,
)


class OMASurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = OMASurvey
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class OMASurveyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OMASurveyQuestion
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class OMASurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OMASurveyResponse
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class OMANormalizedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OMANormalizedData
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class OMADomainScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = OMADomainScore
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class OMAValidationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = OMAValidationResult
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class OMAMaturityLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OMAMaturityLevel
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class OMAGapSerializer(serializers.ModelSerializer):
    class Meta:
        model = OMAGap
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class OMARiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = OMARisk
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class OMARoadmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = OMARoadmap
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class OMABenchmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = OMABenchmark
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class OMABenchmarkDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = OMABenchmarkDataset
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class OMAStrategyExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = OMAStrategyExport
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "exported_at")

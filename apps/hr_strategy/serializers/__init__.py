from rest_framework import serializers

from apps.hr_strategy.models import (
    HRStrategy,
    InitiativeDependency,
    StrategicInitiative,
    StrategicPillar,
    StrategyBenchmark,
    StrategyConfidenceLevel,
    StrategyExecutionLink,
    StrategyExplainability,
    StrategyKPI,
    StrategyReadinessScore,
    StrategyRiskAnalysis,
    StrategyRoadmap,
    StrategyVersion,
)


class HRStrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = HRStrategy
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class StrategyVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyVersion
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class StrategicPillarSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategicPillar
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class StrategicInitiativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategicInitiative
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class InitiativeDependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = InitiativeDependency
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class StrategyKPISerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyKPI
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class StrategyRoadmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyRoadmap
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class StrategyReadinessScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyReadinessScore
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class StrategyConfidenceLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyConfidenceLevel
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class StrategyBenchmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyBenchmark
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class StrategyExecutionLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyExecutionLink
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class StrategyExplainabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyExplainability
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class StrategyRiskAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyRiskAnalysis
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

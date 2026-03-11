from rest_framework import serializers

from apps.tna.models import (
    LearningPath,
    ManagerTNAInput,
    SkillGapAnalysis,
    TNACycle,
    TNAReport,
    TrainingPriority,
)


class TNACycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TNACycle
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class SkillGapAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillGapAnalysis
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class ManagerTNAInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerTNAInput
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class TrainingPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingPriority
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class LearningPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningPath
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class TNAReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TNAReport
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "generated_at")

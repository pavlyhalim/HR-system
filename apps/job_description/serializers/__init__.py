from rest_framework import serializers

from apps.job_description.models import (
    JDApprovalLog,
    JDBenchmarkResult,
    JDCompetency,
    JDConsumerReference,
    JobAnalysisInput,
    JobDescription,
    JobDescriptionVersion,
)


class JDCompetencySerializer(serializers.ModelSerializer):
    class Meta:
        model = JDCompetency
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class JDBenchmarkResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = JDBenchmarkResult
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class JDApprovalLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = JDApprovalLog
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class JDConsumerReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JDConsumerReference
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class JobDescriptionVersionSerializer(serializers.ModelSerializer):
    competencies = JDCompetencySerializer(many=True, read_only=True)

    class Meta:
        model = JobDescriptionVersion
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class JobDescriptionSerializer(serializers.ModelSerializer):
    current_version_detail = JobDescriptionVersionSerializer(source="current_version", read_only=True)

    class Meta:
        model = JobDescription
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "created_by", "approved_by", "approved_at")


class JobAnalysisInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAnalysisInput
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "created_by")

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class JDGenerateSerializer(serializers.Serializer):
    """Trigger JD generation from job analysis input."""
    job_analysis_id = serializers.UUIDField()


class JDSubmitApprovalSerializer(serializers.Serializer):
    """Submit a JD version for approval."""
    pass


class JDApproveRejectSerializer(serializers.Serializer):
    """Approve or reject a JD."""
    reason = serializers.CharField(required=False, allow_blank=True)

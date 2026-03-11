from rest_framework import serializers

from apps.employee_lifecycle.models import (
    ApprovalAction,
    ApprovalRequest,
    Contract,
    ContractSignature,
    ContractVersion,
    Employee,
    EmployeeLifecycleState,
    EmployeePersonalData,
    FinalSettlement,
    Offer,
    OfferTemplate,
    OffboardingRecord,
    OnboardingChecklist,
    OnboardingTask,
    ProbationRecord,
)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class EmployeeLifecycleStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLifecycleState
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "entered_at")


class OfferTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferTemplate
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "approved_at", "sent_at", "accepted_at")


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class ContractVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractVersion
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class ContractSignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractSignature
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class EmployeePersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePersonalData
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class OnboardingChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingChecklist
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class OnboardingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingTask
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "completed_at")


class ProbationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProbationRecord
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class OffboardingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = OffboardingRecord
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "completed_at")


class FinalSettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalSettlement
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "approved_at", "executed_at")


class ApprovalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalRequest
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class ApprovalActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalAction
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

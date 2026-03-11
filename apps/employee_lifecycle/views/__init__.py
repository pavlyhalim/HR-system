from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.permissions import IsHR, IsManager, IsEmployee
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
from apps.employee_lifecycle.serializers import (
    ApprovalActionSerializer,
    ApprovalRequestSerializer,
    ContractSerializer,
    ContractSignatureSerializer,
    ContractVersionSerializer,
    EmployeeLifecycleStateSerializer,
    EmployeePersonalDataSerializer,
    EmployeeSerializer,
    FinalSettlementSerializer,
    OfferSerializer,
    OfferTemplateSerializer,
    OffboardingRecordSerializer,
    OnboardingChecklistSerializer,
    OnboardingTaskSerializer,
    ProbationRecordSerializer,
)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.filter(is_active=True).select_related("user")
    serializer_class = EmployeeSerializer
    permission_classes = [IsHR]
    filterset_fields = ["employment_status", "department", "country_code"]
    search_fields = ["employee_number", "user__email", "user__first_name", "user__last_name"]

    @action(detail=True, methods=["get"], url_path="lifecycle")
    def lifecycle(self, request, pk=None):
        states = EmployeeLifecycleState.objects.filter(employee=self.get_object())
        return Response(EmployeeLifecycleStateSerializer(states, many=True).data)

    @action(detail=True, methods=["post"], url_path="transition")
    def transition(self, request, pk=None):
        employee = self.get_object()
        new_state = request.data.get("state")
        # Close previous state
        prev = EmployeeLifecycleState.objects.filter(employee=employee, exited_at__isnull=True).first()
        if prev:
            prev.exited_at = timezone.now()
            prev.save(update_fields=["exited_at"])
        # Create new state
        state = EmployeeLifecycleState.objects.create(employee=employee, state=new_state)
        employee.employment_status = new_state
        employee.save(update_fields=["employment_status", "updated_at"])
        return Response(EmployeeLifecycleStateSerializer(state).data)


class PreboardingViewSet(viewsets.ViewSet):
    permission_classes = [IsHR]

    @action(detail=False, methods=["post"], url_path="initiate/(?P<candidate_id>[^/.]+)")
    def initiate(self, request, candidate_id=None):
        employee = Employee.objects.create(
            candidate_id=candidate_id,
            employment_status=Employee.EmploymentStatus.PREBOARDING,
        )
        EmployeeLifecycleState.objects.create(employee=employee, state="preboarding")
        return Response(EmployeeSerializer(employee).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="(?P<employee_id>[^/.]+)/status")
    def preboarding_status(self, request, employee_id=None):
        employee = Employee.objects.get(pk=employee_id)
        return Response({"employment_status": employee.employment_status})

    @action(detail=False, methods=["post"], url_path="(?P<employee_id>[^/.]+)/complete")
    def complete(self, request, employee_id=None):
        employee = Employee.objects.get(pk=employee_id)
        employee.employment_status = Employee.EmploymentStatus.ACTIVE
        employee.save(update_fields=["employment_status", "updated_at"])
        return Response({"detail": "Preboarding completed."})


class OfferTemplateViewSet(viewsets.ModelViewSet):
    queryset = OfferTemplate.objects.filter(is_active=True)
    serializer_class = OfferTemplateSerializer
    permission_classes = [IsHR]


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.filter(is_active=True).select_related("employee")
    serializer_class = OfferSerializer
    permission_classes = [IsHR]
    filterset_fields = ["status", "employee"]

    @action(detail=True, methods=["post"], url_path="submit-approval")
    def submit_approval(self, request, pk=None):
        offer = self.get_object()
        if offer.status != Offer.Status.DRAFT:
            return Response({"detail": "Only draft offers can be submitted."}, status=status.HTTP_400_BAD_REQUEST)
        offer.status = Offer.Status.IN_APPROVAL
        offer.save(update_fields=["status", "updated_at"])
        ApprovalRequest.objects.create(
            entity_type="offer", entity_id=offer.id, requested_by=request.user,
        )
        return Response(OfferSerializer(offer).data)

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        offer = self.get_object()
        offer.status = Offer.Status.APPROVED
        offer.approved_by = request.user
        offer.approved_at = timezone.now()
        offer.save(update_fields=["status", "approved_by", "approved_at", "updated_at"])
        return Response(OfferSerializer(offer).data)

    @action(detail=True, methods=["post"], url_path="reject")
    def reject(self, request, pk=None):
        offer = self.get_object()
        offer.status = Offer.Status.REJECTED
        offer.rejection_reason = request.data.get("reason", "")
        offer.save(update_fields=["status", "rejection_reason", "updated_at"])
        return Response(OfferSerializer(offer).data)

    @action(detail=True, methods=["post"], url_path="send")
    def send_offer(self, request, pk=None):
        offer = self.get_object()
        if offer.status != Offer.Status.APPROVED:
            return Response({"detail": "Only approved offers can be sent."}, status=status.HTTP_400_BAD_REQUEST)
        offer.status = Offer.Status.SENT
        offer.sent_at = timezone.now()
        offer.save(update_fields=["status", "sent_at", "updated_at"])
        return Response(OfferSerializer(offer).data)


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.filter(is_active=True).select_related("employee")
    serializer_class = ContractSerializer
    permission_classes = [IsHR]
    filterset_fields = ["status", "contract_type", "employee"]

    @action(detail=True, methods=["post"], url_path="submit-approval")
    def submit_approval(self, request, pk=None):
        contract = self.get_object()
        contract.status = Contract.Status.IN_APPROVAL
        contract.save(update_fields=["status", "updated_at"])
        ApprovalRequest.objects.create(
            entity_type="contract", entity_id=contract.id, requested_by=request.user,
        )
        return Response(ContractSerializer(contract).data)

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        contract = self.get_object()
        contract.status = Contract.Status.APPROVED
        contract.save(update_fields=["status", "updated_at"])
        return Response(ContractSerializer(contract).data)

    @action(detail=True, methods=["post"], url_path="send-signature")
    def send_signature(self, request, pk=None):
        contract = self.get_object()
        if contract.status != Contract.Status.APPROVED:
            return Response({"detail": "Only approved contracts can be sent for signature."}, status=status.HTTP_400_BAD_REQUEST)
        contract.status = Contract.Status.SENT_FOR_SIGNATURE
        contract.save(update_fields=["status", "updated_at"])
        return Response(ContractSerializer(contract).data)

    @action(detail=True, methods=["post"], url_path="sign")
    def sign(self, request, pk=None):
        contract = self.get_object()
        if contract.status != Contract.Status.SENT_FOR_SIGNATURE:
            return Response({"detail": "Contract must be sent for signature first."}, status=status.HTTP_400_BAD_REQUEST)
        ContractSignature.objects.create(
            contract=contract,
            signed_by=request.user,
            signed_at=timezone.now(),
            signature_provider=request.data.get("provider", "internal"),
        )
        contract.status = Contract.Status.SIGNED
        contract.save(update_fields=["status", "updated_at"])
        return Response(ContractSerializer(contract).data)

    @action(detail=True, methods=["get"], url_path="versions")
    def versions(self, request, pk=None):
        versions = ContractVersion.objects.filter(contract=self.get_object())
        return Response(ContractVersionSerializer(versions, many=True).data)


class EmployeePersonalDataViewSet(viewsets.ModelViewSet):
    queryset = EmployeePersonalData.objects.all()
    serializer_class = EmployeePersonalDataSerializer
    permission_classes = [IsHR | IsEmployee]


class OnboardingViewSet(viewsets.ModelViewSet):
    queryset = OnboardingChecklist.objects.filter(is_active=True).select_related("employee")
    serializer_class = OnboardingChecklistSerializer
    permission_classes = [IsHR]

    @action(detail=False, methods=["post"], url_path="initiate/(?P<employee_id>[^/.]+)")
    def initiate(self, request, employee_id=None):
        employee = Employee.objects.get(pk=employee_id)
        checklist, created = OnboardingChecklist.objects.get_or_create(employee=employee)
        return Response(OnboardingChecklistSerializer(checklist).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="checklist")
    def checklist(self, request, pk=None):
        onboarding = self.get_object()
        tasks = OnboardingTask.objects.filter(checklist=onboarding)
        return Response(OnboardingTaskSerializer(tasks, many=True).data)

    @action(detail=True, methods=["post"], url_path="tasks/complete")
    def complete_task(self, request, pk=None):
        task_id = request.data.get("task_id")
        task = OnboardingTask.objects.get(pk=task_id, checklist=self.get_object())
        task.status = OnboardingTask.Status.COMPLETED
        task.completed_at = timezone.now()
        task.save(update_fields=["status", "completed_at", "updated_at"])
        # Update checklist progress
        checklist = task.checklist
        checklist.completed_tasks = checklist.tasks.filter(status=OnboardingTask.Status.COMPLETED).count()
        if checklist.completed_tasks >= checklist.total_tasks and checklist.total_tasks > 0:
            checklist.is_completed = True
            checklist.completed_at = timezone.now()
        checklist.save()
        return Response(OnboardingTaskSerializer(task).data)


class OnboardingTaskViewSet(viewsets.ModelViewSet):
    queryset = OnboardingTask.objects.all()
    serializer_class = OnboardingTaskSerializer
    permission_classes = [IsHR]
    filterset_fields = ["status", "task_type", "assigned_to_role"]


class ProbationViewSet(viewsets.ModelViewSet):
    queryset = ProbationRecord.objects.filter(is_active=True).select_related("employee")
    serializer_class = ProbationRecordSerializer
    permission_classes = [IsHR | IsManager]
    filterset_fields = ["status"]

    @action(detail=True, methods=["post"], url_path="review")
    def review(self, request, pk=None):
        record = self.get_object()
        record.manager_evaluation = request.data.get("evaluation", {})
        record.evaluation_notes = request.data.get("notes", "")
        record.status = ProbationRecord.Status.REVIEW_PENDING
        record.save(update_fields=["manager_evaluation", "evaluation_notes", "status", "updated_at"])
        return Response(ProbationRecordSerializer(record).data)

    @action(detail=True, methods=["post"], url_path="confirm")
    def confirm(self, request, pk=None):
        record = self.get_object()
        decision = request.data.get("decision", "confirmed")
        if decision == "confirmed":
            record.status = ProbationRecord.Status.CONFIRMED
        elif decision == "extended":
            record.status = ProbationRecord.Status.EXTENDED
            record.end_date = request.data.get("new_end_date", record.end_date)
        elif decision == "terminated":
            record.status = ProbationRecord.Status.TERMINATED
        record.decided_by = request.user
        record.decided_at = timezone.now()
        record.save()
        return Response(ProbationRecordSerializer(record).data)


class OffboardingViewSet(viewsets.ModelViewSet):
    queryset = OffboardingRecord.objects.filter(is_active=True).select_related("employee")
    serializer_class = OffboardingRecordSerializer
    permission_classes = [IsHR]
    filterset_fields = ["status", "exit_type"]

    @action(detail=False, methods=["post"], url_path="initiate/(?P<employee_id>[^/.]+)")
    def initiate(self, request, employee_id=None):
        employee = Employee.objects.get(pk=employee_id)
        record = OffboardingRecord.objects.create(
            employee=employee,
            exit_type=request.data.get("exit_type", OffboardingRecord.ExitType.VOLUNTARY),
            exit_reason=request.data.get("reason", ""),
            initiated_by=request.user,
        )
        employee.employment_status = Employee.EmploymentStatus.EXITING
        employee.save(update_fields=["employment_status", "updated_at"])
        return Response(OffboardingRecordSerializer(record).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="complete")
    def complete(self, request, pk=None):
        record = self.get_object()
        record.status = OffboardingRecord.Status.COMPLETED
        record.completed_at = timezone.now()
        record.save(update_fields=["status", "completed_at", "updated_at"])
        employee = record.employee
        employee.employment_status = Employee.EmploymentStatus.TERMINATED
        employee.termination_date = timezone.now().date()
        employee.save(update_fields=["employment_status", "termination_date", "updated_at"])
        return Response(OffboardingRecordSerializer(record).data)


class FinalSettlementViewSet(viewsets.ModelViewSet):
    queryset = FinalSettlement.objects.filter(is_active=True).select_related("employee")
    serializer_class = FinalSettlementSerializer
    permission_classes = [IsHR]
    filterset_fields = ["approval_status"]

    @action(detail=True, methods=["post"], url_path="submit-approval")
    def submit_approval(self, request, pk=None):
        settlement = self.get_object()
        settlement.approval_status = FinalSettlement.ApprovalStatus.SUBMITTED
        settlement.save(update_fields=["approval_status", "updated_at"])
        ApprovalRequest.objects.create(
            entity_type="settlement", entity_id=settlement.id, requested_by=request.user,
        )
        return Response(FinalSettlementSerializer(settlement).data)

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        settlement = self.get_object()
        settlement.approval_status = FinalSettlement.ApprovalStatus.APPROVED
        settlement.approved_by = request.user
        settlement.approved_at = timezone.now()
        settlement.save(update_fields=["approval_status", "approved_by", "approved_at", "updated_at"])
        return Response(FinalSettlementSerializer(settlement).data)


class ApprovalRequestViewSet(viewsets.ModelViewSet):
    queryset = ApprovalRequest.objects.all()
    serializer_class = ApprovalRequestSerializer
    permission_classes = [IsHR | IsManager]
    filterset_fields = ["entity_type", "status"]

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        approval = self.get_object()
        ApprovalAction.objects.create(
            approval_request=approval, action=ApprovalAction.ActionType.APPROVED,
            actor=request.user, reason=request.data.get("reason", ""),
            step_number=approval.current_step,
        )
        approval.current_step += 1
        if approval.current_step >= len(approval.approval_chain):
            approval.status = ApprovalRequest.Status.APPROVED
        approval.save()
        return Response(ApprovalRequestSerializer(approval).data)

    @action(detail=True, methods=["post"], url_path="reject")
    def reject(self, request, pk=None):
        approval = self.get_object()
        ApprovalAction.objects.create(
            approval_request=approval, action=ApprovalAction.ActionType.REJECTED,
            actor=request.user, reason=request.data.get("reason", ""),
            step_number=approval.current_step,
        )
        approval.status = ApprovalRequest.Status.REJECTED
        approval.save(update_fields=["status", "updated_at"])
        return Response(ApprovalRequestSerializer(approval).data)

    @action(detail=True, methods=["get"], url_path="history")
    def history(self, request, pk=None):
        actions = ApprovalAction.objects.filter(approval_request=self.get_object())
        return Response(ApprovalActionSerializer(actions, many=True).data)

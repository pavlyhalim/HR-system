from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.permissions import IsHR, IsManager
from apps.performance.models import (
    BiasDetectionResult,
    CalibrationSession,
    FinalRating,
    GoalCascade,
    PerformanceFramework,
    PerformanceReview,
    ReviewCycle,
)
from apps.performance.serializers import (
    BiasDetectionResultSerializer,
    CalibrationSessionSerializer,
    FinalRatingSerializer,
    GoalCascadeSerializer,
    PerformanceFrameworkSerializer,
    PerformanceReviewSerializer,
    ReviewCycleSerializer,
)


class PerformanceFrameworkViewSet(viewsets.ModelViewSet):
    queryset = PerformanceFramework.objects.filter(is_active=True)
    serializer_class = PerformanceFrameworkSerializer
    permission_classes = [IsHR]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ReviewCycleViewSet(viewsets.ModelViewSet):
    queryset = ReviewCycle.objects.filter(is_active=True)
    serializer_class = ReviewCycleSerializer
    permission_classes = [IsHR]
    filterset_fields = ["status", "framework"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"], url_path="launch")
    def launch(self, request, pk=None):
        cycle = self.get_object()
        cycle.status = ReviewCycle.Status.ACTIVE
        cycle.save(update_fields=["status", "updated_at"])
        return Response(ReviewCycleSerializer(cycle).data)


class GoalCascadeViewSet(viewsets.ModelViewSet):
    queryset = GoalCascade.objects.filter(is_active=True)
    serializer_class = GoalCascadeSerializer
    permission_classes = [IsHR | IsManager]
    filterset_fields = ["cycle"]


class PerformanceReviewViewSet(viewsets.ModelViewSet):
    queryset = PerformanceReview.objects.filter(is_active=True)
    serializer_class = PerformanceReviewSerializer
    permission_classes = [IsHR | IsManager]
    filterset_fields = ["cycle", "status"]

    @action(detail=True, methods=["post"], url_path="self-review")
    def self_review(self, request, pk=None):
        review = self.get_object()
        review.self_assessment = request.data.get("assessment", {})
        review.status = PerformanceReview.Status.SELF_REVIEW
        review.save(update_fields=["self_assessment", "status", "updated_at"])
        return Response(PerformanceReviewSerializer(review).data)

    @action(detail=True, methods=["post"], url_path="manager-review")
    def manager_review(self, request, pk=None):
        review = self.get_object()
        review.manager_assessment = request.data.get("assessment", {})
        review.reviewer = request.user
        review.status = PerformanceReview.Status.MANAGER_REVIEW
        review.submitted_at = timezone.now()
        review.save(update_fields=["manager_assessment", "reviewer", "status", "submitted_at", "updated_at"])
        return Response(PerformanceReviewSerializer(review).data)

    @action(detail=True, methods=["get"], url_path="bias-check")
    def bias_check(self, request, pk=None):
        results = BiasDetectionResult.objects.filter(review=self.get_object())
        return Response(BiasDetectionResultSerializer(results, many=True).data)


class CalibrationSessionViewSet(viewsets.ModelViewSet):
    queryset = CalibrationSession.objects.filter(is_active=True)
    serializer_class = CalibrationSessionSerializer
    permission_classes = [IsHR]
    filterset_fields = ["cycle", "status"]

    @action(detail=True, methods=["post"], url_path="complete")
    def complete(self, request, pk=None):
        session = self.get_object()
        session.status = CalibrationSession.Status.COMPLETED
        session.calibrated_by = request.user
        session.completed_at = timezone.now()
        session.save(update_fields=["status", "calibrated_by", "completed_at", "updated_at"])
        return Response(CalibrationSessionSerializer(session).data)


class FinalRatingViewSet(viewsets.ModelViewSet):
    queryset = FinalRating.objects.all()
    serializer_class = FinalRatingSerializer
    permission_classes = [IsHR]

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        rating = self.get_object()
        rating.approved_by = request.user
        rating.approved_at = timezone.now()
        rating.save(update_fields=["approved_by", "approved_at", "updated_at"])
        return Response(FinalRatingSerializer(rating).data)

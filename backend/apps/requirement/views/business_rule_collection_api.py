from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..selectors import business_rule_list
from ..serializers import (
    BusinessRuleCreateInputSerializer,
    BusinessRuleCreateOutputSerializer,
    BusinessRuleOutputSerializer,
)
from ..services import business_rule_create


class BusinessRuleCollectionApi(APIView):
    """List and create business rules in a project."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=BusinessRuleOutputSerializer(many=True),
        summary="List project business rules",
        tags=["Business rules"],
    )
    def get(self, request, project_id):
        """Return active business rules associated with the project."""

        business_rules = business_rule_list(project_id=str(project_id))
        output_serializer = BusinessRuleOutputSerializer(business_rules, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=BusinessRuleCreateInputSerializer,
        responses=BusinessRuleCreateOutputSerializer,
        summary="Create a project business rule",
        tags=["Business rules"],
    )
    def post(self, request, project_id):
        """Validate input and delegate business rule creation."""

        input_serializer = BusinessRuleCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        business_rule = business_rule_create(
            project_id=str(project_id),
            user_id=str(request.user.pk),
            rule=input_serializer.validated_data["rule"],
            requirement_ids=[
                str(requirement_id)
                for requirement_id in input_serializer.validated_data["requirement_ids"]
            ],
        )
        output_serializer = BusinessRuleCreateOutputSerializer(business_rule)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

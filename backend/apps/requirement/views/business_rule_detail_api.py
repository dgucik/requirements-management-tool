from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import (
    BusinessRuleUpdateInputSerializer,
    BusinessRuleUpdateOutputSerializer,
)
from ..services import business_rule_delete, business_rule_update


class BusinessRuleDetailApi(APIView):
    """Update or soft-delete an existing business rule."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=BusinessRuleUpdateInputSerializer,
        responses=BusinessRuleUpdateOutputSerializer,
        summary="Update a project business rule",
        tags=["Business rules"],
    )
    def patch(self, request, project_id, business_rule_id):
        """Validate the rule text and delegate the update."""

        input_serializer = BusinessRuleUpdateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        business_rule = business_rule_update(
            project_id=str(project_id),
            business_rule_id=str(business_rule_id),
            user_id=str(request.user.pk),
            rule=input_serializer.validated_data.get("rule"),
            requirement_ids=(
                [
                    str(requirement_id)
                    for requirement_id in input_serializer.validated_data[
                        "requirement_ids"
                    ]
                ]
                if "requirement_ids" in input_serializer.validated_data
                else None
            ),
        )
        output_serializer = BusinessRuleUpdateOutputSerializer(business_rule)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={status.HTTP_204_NO_CONTENT: None},
        summary="Delete a project business rule",
        tags=["Business rules"],
    )
    def delete(self, request, project_id, business_rule_id):
        """Soft-delete the selected business rule."""

        business_rule_delete(
            project_id=str(project_id),
            business_rule_id=str(business_rule_id),
            user_id=str(request.user.pk),
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.core.exceptions import PermissionDenied, ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler

from core.exceptions import (
    ApplicationError,
    BusinessRuleError,
    EntityNotFoundError,
)


def api_exception_handler(exc, context):
    """Translate application errors and normalize DRF error responses.

    Args:
        exc: Exception raised while handling the request.
        context: DRF context containing the view and request.

    Returns:
        A normalized DRF response or ``None`` for unhandled exceptions.
    """

    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))
    elif isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, EntityNotFoundError):
            status_code = 404
        elif isinstance(exc, BusinessRuleError):
            status_code = 400
        elif isinstance(exc, ApplicationError):
            status_code = 400
        else:
            return None

        return Response(
            {"message": exc.message, "extra": exc.extra},
            status=status_code,
        )

    if isinstance(exc, exceptions.ValidationError):
        response.data = {
            "message": "Validation error",
            "extra": {"fields": response.data.get("detail", response.data)},
        }
    else:
        response.data = {
            "message": response.data.get("detail", response.data),
            "extra": {},
        }

    return response

from typing import Any, Dict

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def format_error_response(message: str, code: str | None = None, details: Any | None = None, http_status: int = status.HTTP_400_BAD_REQUEST) -> Response:
    payload: Dict[str, Any] = {
        'error': {
            'message': message,
        }
    }
    if code:
        payload['error']['code'] = code
    if details is not None:
        payload['error']['details'] = details
    return Response(payload, status=http_status)


def custom_exception_handler(exc, context):
    """
    Wrap DRF/Django exceptions into a consistent error envelope.
    """
    response = exception_handler(exc, context)

    if response is None:
        # Non-DRF error; return generic 500
        return format_error_response(
            message='An unexpected error occurred.',
            code='server_error',
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # DRF provided a response; normalize structure
    details = response.data

    # Extract a human message where possible
    if isinstance(details, dict):
        message = details.get('detail') or 'Request could not be processed.'
    else:
        message = 'Request could not be processed.'

    return format_error_response(
        message=message,
        details=details,
        http_status=response.status_code,
    )



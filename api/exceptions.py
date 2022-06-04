from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    handlers = {
        'ValidationError': _handle_generic_error,
        'Http404': _handle_generic_error,
        'TypeError': _handle_generic_error
    }
    response = exception_handler(exc, context)
    exception_class = exc.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):
    response['data'] = {
        'error': 'There is an error'
    }
    return response
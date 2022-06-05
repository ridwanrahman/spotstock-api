from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    To handle errors in a customized way
    """
    handlers = {
        'ValidationError': _handle_generic_error,
        'Http404': _handle_generic_error,
        'TypeError': _handle_generic_error,
        'MethodNotAllowed': _handle_generic_error
    }
    response = exception_handler(exc, context)
    exception_class = exc.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    if response is None:
        return {'error': 'There has been an error'}


def _handle_generic_error(exc, context, response):
    response['data'] = {
        'error': 'There is an error'
    }
    return response

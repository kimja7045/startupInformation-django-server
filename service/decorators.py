import functools

from service.exceptions import ValidationError


def form_validation(serializer_class):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, request, *args, **kwargs):
            data = getattr(request, 'data', getattr(request, request.method))
            serializer = serializer_class(data=data)
            if not serializer.is_valid():
                raise ValidationError(dict(serializer.errors.items()))
            return func(self, request, serializer, *args, **kwargs)
        return wrapper
    return decorator


def required_fields(fields):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, request, *args, **kwargs):
            for k, values in fields.items():
                target = getattr(request, k)
                if not all([v in target for v in values]):
                    raise ValidationError({field: '필수 입력 항목입니다.' for field in set(values).difference(target)})
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator


def sms_verification(scope):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, request, *args, **kwargs):
            if request.session.get('sms_scope') != scope or not request.session.get('sms_verified'):
                raise ValidationError({'sms_verification': 'SMS 인증을 먼저 해주셔야 합니다.'})
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator

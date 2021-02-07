import sys
import functools


def takes(*types_args):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for value_, type_ in zip(args, types_args):
                if not isinstance(value_, type_):
                    raise TypeError
            return func(*args, **kwargs)
        return wrapper
    return decorator


exec(sys.stdin.read())

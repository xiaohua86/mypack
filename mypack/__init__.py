
__version__ = '0.1.0'

__all__ = ['logfile']


def logfile(*args, **kwargs):
    from .log import logfile as _logfile
    return _logfile(*args, **kwargs)

    
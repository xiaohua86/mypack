__all__ = ['steinhardt_op']

def steinhardt_op(*args, **kwargs):
    from .OP import steinhardt_op as _steinhardt_op
    return _steinhardt_op(*args, **kwargs)
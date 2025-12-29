__all__ = ['hist_kde']


def hist_kde(*args, **kwargs):
    from .hist_kde import hist_kde as _hist_kde
    return _hist_kde(*args, **kwargs)
"""
my custom shortcuts
"""
from django.core.exceptions import ObjectDoesNotExist


def get_or_none(classmodel, **kwargs):
    """like get_or_404, but returns None instead of raising an exception, if the record does not exists in db"""
    try:
        return classmodel.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None

from graphene_django import DjangoConnectionField
from graphene_django.utils import DJANGO_FILTER_INSTALLED

from graphene_django_actions.mixins import (
    PermissionConnectionFieldMixin,
    PermissionFilterConnectionFieldMixin,
)


class PermissionConnectionField(PermissionConnectionFieldMixin, DjangoConnectionField):
    pass


__all__ = ["PermissionConnectionField"]


if DJANGO_FILTER_INSTALLED:
    from graphene_django.filter import DjangoFilterConnectionField

    class PermissionFilterConnectionField(
        PermissionFilterConnectionFieldMixin, DjangoFilterConnectionField
    ):
        pass

    __all__.append("PermissionFilterConnectionField")

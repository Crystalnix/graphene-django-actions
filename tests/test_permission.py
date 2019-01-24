from graphene_django_actions.permissions import (
    Permission,
    AllowAny,
    DenyAny,
    AllowAuthenticated,
)


def test_name():
    name = "permission"
    permission = Permission(name)
    assert permission.name == name


def test_or_permission(granted_permission, denied_permission, user, model):
    or_permission = granted_permission | denied_permission
    assert or_permission.check(user, model)
    and_permission = granted_permission & denied_permission
    assert not and_permission.check(user, model)


def test_allow_any(user, model):
    allow_any = AllowAny()
    assert allow_any.check(user, model)


def test_deny_any(user, model):
    deny_any = DenyAny()
    assert not deny_any.check(user, model)

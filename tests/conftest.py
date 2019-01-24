import pytest

from graphene_django_actions.action import Action
from graphene_django_actions.permissions import Permission
from graphene_django_actions.registry import ActionRegistry


@pytest.fixture
def model_class():
    class TestModel:
        pass

    return TestModel


@pytest.fixture
def model(model_class):
    class Meta:
        model = model_class

    instance = model_class()
    instance._meta = Meta()
    return instance


@pytest.fixture
def action():
    return Action("action", register=False)


@pytest.fixture
def granted_permission(mocker):
    permission = Permission()
    check_mock = mocker.MagicMock()
    check_mock.return_value = True
    permission.check = check_mock
    return permission


@pytest.fixture
def denied_permission(mocker):
    permission = Permission()
    check_mock = mocker.MagicMock()
    check_mock.return_value = False
    permission.check = check_mock
    return permission


@pytest.fixture
def user(mocker):
    return mocker.MagicMock()


@pytest.fixture
def authenticated_user(mocker):
    user = mocker.MagicMock()
    user.is_authenticated = True
    return user


@pytest.fixture
def parent_object(mocker):
    return mocker.MagicMock()


@pytest.fixture
def action_registry():
    registry = ActionRegistry()
    registry.clear()
    yield registry
    registry.clear()


@pytest.fixture
def handle_has_permission(mocker):
    return mocker.patch(
        "graphene_django_actions.mixins.BasePermissionMixin.handle_has_permission"
    )


@pytest.fixture
def handle_no_permission(mocker):
    return mocker.patch(
        "graphene_django_actions.mixins.BasePermissionMixin.handle_no_permission"
    )


@pytest.fixture
def get_permission_target(mocker):
    return mocker.patch(
        "graphene_django_actions.mixins.BasePermissionMixin.get_permission_target"
    )


@pytest.fixture
def has_permission(mocker):
    return mocker.patch(
        "graphene_django_actions.mixins.BasePermissionMixin.has_permission"
    )


@pytest.fixture
def get_action(mocker):
    return mocker.patch("graphene_django_actions.mixins.BasePermissionMixin.get_action")


@pytest.fixture
def get_user(mocker):
    return mocker.patch("graphene_django_actions.mixins.BasePermissionMixin.get_user")


@pytest.fixture
def get_parent_object(mocker):
    return mocker.patch(
        "graphene_django_actions.mixins.BasePermissionMixin.get_parent_object"
    )


@pytest.fixture
def perform_action(mocker):
    return mocker.patch(
        "graphene_django_actions.mixins.BasePermissionMixin.perform_action"
    )

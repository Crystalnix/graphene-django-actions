import pytest
from django.core.exceptions import ImproperlyConfigured
from graphene_django_actions.mixins import BasePermissionMixin, PermissionNodeMixin


def test_get_action(action, mocker):
    class Test(BasePermissionMixin):
        pass

    with pytest.raises(ImproperlyConfigured):
        Test.get_action(None, None)

    Test.action = action
    assert Test.get_action(None, None) is action


def test_perform_granted_action(
    mocker,
    model,
    handle_has_permission,
    handle_no_permission,
    get_permission_target,
    has_permission,
):
    info = mocker.MagicMock()
    success = mocker.MagicMock()
    handle_has_permission.return_value = success
    get_permission_target.return_value = model

    has_permission.return_value = True

    action_result = BasePermissionMixin.perform_action(info)

    get_permission_target.assert_called()
    has_permission.assert_called()
    handle_no_permission.assert_not_called()
    handle_has_permission.assert_called()
    assert action_result is success


def test_perform_denied_action(
    mocker,
    model,
    handle_has_permission,
    handle_no_permission,
    get_permission_target,
    has_permission,
):
    info = mocker.MagicMock()
    error = mocker.MagicMock()
    handle_no_permission.return_value = error
    get_permission_target.return_value = model

    has_permission.return_value = False

    action_result = BasePermissionMixin.perform_action(info)

    get_permission_target.assert_called()
    has_permission.assert_called()
    handle_has_permission.assert_not_called()
    handle_no_permission.assert_called()
    assert action_result is error


def test_has_permission(get_user, mocker, model, get_action, get_parent_object):
    has_action_permission_result = mocker.MagicMock()
    info = mocker.MagicMock()
    action = mocker.MagicMock()
    action.has_permission.return_value = has_action_permission_result
    user = mocker.MagicMock()
    parent_object = mocker.MagicMock()
    get_action.return_value = action
    get_user.return_value = user
    get_parent_object.return_value = parent_object
    kwargs = {}

    assert (
        BasePermissionMixin.has_permission(model, info, **kwargs)
        is has_action_permission_result
    )

    get_action.assert_called_with(model, info, **kwargs)
    get_user.assert_called_with(info)
    get_parent_object.assert_called_with(model, info, **kwargs)
    action.has_permission.assert_called_with(user, model, parent_object, **kwargs)


def test_assert_get_node(perform_action, mocker):
    info = mocker.MagicMock()
    _id = 1
    action_result = mocker.MagicMock()
    perform_action.return_value = action_result

    assert PermissionNodeMixin.get_node(info, _id) is action_result

    perform_action.assert_called_with(info, **{"id": _id})

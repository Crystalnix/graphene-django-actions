from graphene_django_actions.action import Action
from graphene_django_actions.permissions import AllowAny, DenyAny


def test_action_eq():
    create = Action("create", register=False)
    create2 = Action("create", register=False)
    delete = Action("delete", register=False)

    assert create == create2
    assert create != delete
    assert create != object()


def test_add_permission(model_class, action):
    permission = AllowAny()
    permission2 = DenyAny()
    action.add_permission(model_class, permission)
    assert action.get_permissions(model_class) == [permission]

    action.add_permission(model_class, permission2)
    assert action.get_permissions(model_class) == [permission, permission2]


def test_set_permissions(model_class, action):
    permission = AllowAny()
    permissions = [permission]
    action.set_permissions(model_class, permissions)

    assert action.get_permissions(model_class) == permissions


def test_get_model_type(action, model, model_class):
    assert action.get_model_type(model_class) == model_class
    assert action.get_model_type(model) == model_class


def test_has_permission(
    action,
    user,
    parent_object,
    model_class,
    model,
    granted_permission,
    denied_permission,
):
    target = model

    assert not action.has_permission(user, target, parent_object=None)

    action.set_permissions(model_class, [denied_permission])
    assert not action.has_permission(user, target, parent_object=None)

    action.set_permissions(model_class, [granted_permission])
    assert action.has_permission(user, target, parent_object=None)
    granted_permission.check.assert_called_with(user, target)

    assert action.has_permission(user, target, parent_object=parent_object)
    granted_permission.check.assert_called_with(user, parent_object)


def test_registry(mocker):
    register_mock = mocker.patch(
        "graphene_django_actions.registry.ActionRegistry.register"
    )

    Action("action", register=False)
    register_mock.assert_not_called()

    action = Action("action", register=True)
    register_mock.assert_called_with(action)


def test_action_str():
    action_name = "test"
    action = Action(action_name, register=False)
    assert str(action) == action_name

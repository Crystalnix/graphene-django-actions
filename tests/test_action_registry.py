import pytest

from graphene_django_actions.action import Action
from graphene_django_actions.registry import ActionRegistry


def test_not_singleton_registry():
    first_instance = ActionRegistry()
    second_instance = ActionRegistry()

    assert first_instance is not second_instance


def test_register_different_actions(action_registry):
    actions = [Action("first", register=False), Action("second", register=False)]
    for action in actions:
        action_registry.register(action)
    assert len(actions) == len(action_registry.get_actions())


def test_register_same_actions(action_registry):
    action = Action("action", register=False)
    action_registry.register(action)
    with pytest.raises(ValueError):
        action_registry.register(action)

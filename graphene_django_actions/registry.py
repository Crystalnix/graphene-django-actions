class ActionRegistry:
    """Singleton registry for Action instances."""

    storage = {}

    def register(self, action):
        name = action.name
        if name in self.storage:
            raise ValueError(f"Action {name} is already registered in the registry")
        self.storage[name] = action

    def get_actions(self):
        return list(self.storage.values())

    def clear(self):
        self.storage.clear()


registry = ActionRegistry()


def get_action_registry():
    return registry

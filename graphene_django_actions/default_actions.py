from .action import Action

ViewAction = Action("View")
ChangeAction = Action("Change")
DeleteAction = Action("Delete")
CreateAction = Action("Create", on_parent=True)
ListAction = Action("List", on_parent=True)

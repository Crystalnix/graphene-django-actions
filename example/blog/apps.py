from datetime import timedelta

from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = "blog"

    def ready(self):
        self.init_comment_permissions()
        self.init_post_permissions()

    @staticmethod
    def init_comment_permissions():
        from .models import Comment
        from .permissions import AllowAuthor, AllowCommentPostAuthor, AllowPublished
        from graphene_django_actions.permissions import AllowAuthenticated, AllowAny
        from graphene_django_actions.default_actions import (
            CreateAction,
            DeleteAction,
            ChangeAction,
            ViewAction,
            ListAction,
        )

        allow_authenticated = AllowAuthenticated()
        allow_published = AllowPublished()
        create_permission = (
            allow_authenticated & allow_published
        )  # only authenticated users can comment on published posts
        CreateAction.add_permission(Comment, create_permission)

        allow_author = AllowAuthor()
        allow_comment_post_author = AllowCommentPostAuthor()
        delete_permission = (
            allow_author | allow_comment_post_author
        )  # only author of a comment or author of a post can delete
        DeleteAction.add_permission(Comment, delete_permission)

        ChangeAction.add_permission(
            Comment, allow_author
        )  # only author of a comment can change
        allow_any = AllowAny()
        ViewAction.add_permission(Comment, allow_any)
        ListAction.add_permission(Comment, allow_any)

    @staticmethod
    def init_post_permissions():
        from .models import Post
        from .permissions import AllowAuthor
        from graphene_django_actions.default_actions import (
            CreateAction,
            DeleteAction,
            ChangeAction,
            ViewAction,
            ListAction,
        )
        from graphene_django_actions.permissions import AllowAuthenticated, AllowAny
        from .permissions import AllowAge, AllowPublished

        allow_author = AllowAuthor()
        allow_authenticated = AllowAuthenticated()
        CreateAction.add_permission(Post, allow_authenticated)
        DeleteAction.add_permission(Post, allow_author)

        change_permission = allow_author & AllowAge(timedelta(days=1))
        ChangeAction.add_permission(Post, change_permission)

        allow_published = AllowPublished()
        ViewAction.add_permission(Post, allow_published)

        allow_any = AllowAny()
        ListAction.add_permission(Post, allow_any)

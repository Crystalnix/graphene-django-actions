from datetime import timedelta

from django.contrib.auth.models import User
from django.utils.timezone import now

from .utils import BaseGrapheneTestCase, assert_model_count_change
from graphene.relay.node import to_global_id
from model_mommy import mommy
from blog.models import Post


class BasePostTest(BaseGrapheneTestCase):
    def setUp(self):
        self.user = mommy.make(User)
        self.published_post = mommy.make(Post, is_published=True)
        self.not_published_post = mommy.make(Post, is_published=False)

    @staticmethod
    def get_post_id(post):
        return to_global_id("PostType", post.id)

    @staticmethod
    def get_old_post():
        return mommy.make(
            Post, is_published=True, created_at=now() - timedelta(days=1, seconds=1)
        )


class PostQueryTest(BasePostTest):
    def test_get_published_post(self):
        post = self.get_post(self.published_post)
        self.assertTrue(post)

    def test_get_not_published_post(self):
        post = self.get_post(self.not_published_post)
        self.assertIsNone(post)

    def test_unauthorized_permission_set(self):
        permission_set = self.get_permission_set(self.published_post)
        self.assertEqual(
            permission_set,
            {
                "view": True,
                "change": False,
                "delete": False,
                "createComment": False,
                "listComment": True,
            },
        )

    def test_authorized_permission_set(self):
        self.client.force_login(self.user)
        permission_set = self.get_permission_set(self.published_post)
        self.assertEqual(
            permission_set,
            {
                "view": True,
                "change": False,
                "delete": False,
                "createComment": True,
                "listComment": True,
            },
        )

    def test_author_permission_set(self):
        post = self.published_post
        author = post.author
        self.client.force_login(author)
        permission_set = self.get_permission_set(post)
        self.assertEqual(
            permission_set,
            {
                "view": True,
                "change": True,
                "delete": True,
                "createComment": True,
                "listComment": True,
            },
        )

    def test_author_permission_set_old_post(self):
        post = self.get_old_post()
        author = post.author
        self.client.force_login(author)
        permission_set = self.get_permission_set(post)
        self.assertEqual(
            permission_set,
            {
                "view": True,
                "change": False,
                "delete": True,
                "createComment": True,
                "listComment": True,
            },
        )

    def test_list_posts(self):
        query = """
            {
                posts {
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
        """
        data = self.send_graphql_request(query, {})
        self.assertTrue(data["posts"])

    def get_permission_set(self, post):
        permission_set = """
            permissionSet {
                view
                change
                delete
                createComment: create(type: "CommentType")
                listComment: list(type: "CommentType")
            }
        """
        post_data = self.get_post(post, permission_set)
        return post_data["permissionSet"]

    def get_post(self, post, subselection="id"):
        global_id = self.get_post_id(post)
        query = (
            """
            query getPost($id: ID!) {
                post(id: $id) {
                    %s
                }
            }
        """
            % subselection
        )
        variables = {"id": global_id}
        data = self.send_graphql_request(query, variables)
        return data["post"]


class PostMutationTest(BasePostTest):
    def test_unauthorized_create_post(self):
        with assert_model_count_change(Post, 0):
            mutation = self.create_post()
        self.assertTrue(mutation["permissionError"])

    def test_authorized_create_post(self):
        self.client.force_login(self.user)
        with assert_model_count_change(Post, 1):
            mutation = self.create_post()
        self.assertIsNone(mutation["permissionError"])

    def test_unauthorized_change_post(self):
        mutation = self.change_post(self.published_post)
        self.assertTrue(mutation["permissionError"])

    def test_authorized_change_post(self):
        self.client.force_login(self.user)
        mutation = self.change_post(self.published_post)
        self.assertTrue(mutation["permissionError"])

    def test_author_change_post(self):
        post = self.published_post
        self.client.force_login(post.author)
        mutation = self.change_post(post)
        self.assertIsNone(mutation["permissionError"])

    def test_author_change_old_post(self):
        post = self.get_old_post()
        self.client.force_login(post.author)
        mutation = self.change_post(post)
        self.assertTrue(mutation["permissionError"])

    def test_unauthorized_delete_post(self):
        with assert_model_count_change(Post, 0):
            mutation = self.delete_post(self.published_post)
        self.assertTrue(mutation["permissionError"])

    def test_authorized_delete_post(self):
        self.client.force_login(self.user)
        with assert_model_count_change(Post, 0):
            mutation = self.delete_post(self.published_post)
        self.assertTrue(mutation["permissionError"])

    def test_author_delete_post(self):
        post = self.published_post
        self.client.force_login(post.author)
        with assert_model_count_change(Post, -1):
            mutation = self.delete_post(post)
        self.assertIsNone(mutation["permissionError"])

    def create_post(self):
        query = """
            mutation createPost($input: CreatePostMutationInput!) {
                createPost(input: $input) {
                    id
                    permissionError {
                        message
                    }
                }
            }
        """
        variables = {"input": {"title": "Title", "body": "Body", "isPublished": True}}
        data = self.send_graphql_request(query, variables)
        return data["createPost"]

    def change_post(self, post):
        query = """
            mutation changePost($input: ChangePostMutationInput!) {
                changePost(input: $input) {
                    id
                    title
                    permissionError {
                        message
                    }
                }
            }
        """
        variables = {
            "input": {
                "id": str(post.id),
                "title": "Changed title",
                "body": "Changed body",
            }
        }
        data = self.send_graphql_request(query, variables)
        return data["changePost"]

    def delete_post(self, post):
        query = """
            mutation deletePost($input: DeletePostMutationInput!) {
                deletePost(input: $input) {
                    deleted
                    permissionError {
                        message
                    }
                }
            }
        """
        variables = {"input": {"id": str(post.id)}}
        data = self.send_graphql_request(query, variables)
        return data["deletePost"]

import graphene as graphene
import graphene_gae
from graphene_gae import NdbConnectionField

from models.post import Post
from models.user import User
from schemas.post import PostType


class UserType(graphene_gae.NdbObjectType):
    class Meta:
        model = User
        exclude_fields = ("password",)
        interfaces = (graphene.relay.Node,)

    posts = NdbConnectionField(PostType)

    def resolve_posts(self, info, **kwargs):
        return Post.query(Post.user_key == self.key)


class Query(graphene.ObjectType):
    user = graphene.Field(
        UserType,
        id=graphene.ID(description="The NDB ID of a User"), required=True)
    users = NdbConnectionField(
        UserType,
        description="Gets all users")

    def resolve_user(self, info, id, **kwargs):
        user = User.get_by_id(int(id))
        if not user:
            raise Exception("User not found")
        return user

    def resolve_users(self, info, **kwargs):
        return User.query()


class AddUser(graphene.relay.ClientIDMutation):
    class Input:
        username = graphene.String()
        password = graphene.String()
        user_type = graphene.String()

    user = graphene.Field(UserType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, username, password, user_type, **kwargs):
        user = User.add(username=username, password=password, user_type=user_type)
        return AddUser(user=user)


class Mutation(graphene.ObjectType):
    add_user = AddUser.Field(description="Adds user")

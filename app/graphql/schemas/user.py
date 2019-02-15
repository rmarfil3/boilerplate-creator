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
    users = graphene.List(
        UserType,
        description="Gets all users")

    def resolve_user(self, info, id, **kwargs):
        user = User.get_by_id(int(id))
        if not user:
            raise Exception("Gagu")
        return user

    def resolve_users(self, info, **kwargs):
        return User.query().fetch()


class AddUser(graphene.relay.ClientIDMutation):
    class Input:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        password = graphene.String()

    user = graphene.Field(UserType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, first_name, last_name, email, password, **kwargs):
        user = User()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.password = password
        user.put()

        return AddUser(user=user)


class Mutation(graphene.ObjectType):
    add_user = AddUser.Field(description="Adds user")

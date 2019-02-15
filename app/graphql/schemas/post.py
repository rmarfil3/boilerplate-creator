import graphene
import graphene_gae
from google.appengine.ext import ndb
from graphene_gae import NdbConnectionField

from models.post import Post
from models.user import User


class PostType(graphene_gae.NdbObjectType):
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    posts = NdbConnectionField(
        PostType,
        description="Gets all posts")

    def resolve_posts(self, info, **kwargs):
        return Post.query()


class AddPost(graphene.relay.ClientIDMutation):
    class Input:
        user_id = graphene.ID(required=True)
        title = graphene.String()
        content = graphene.String()

    post = graphene.Field(PostType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, user_id, title, content, **kwargs):
        post = Post()
        post.title = title
        post.content = content
        post.user_key = ndb.Key(User, int(user_id))
        post.put()

        return AddPost(post=post)


class Mutation(graphene.ObjectType):
    add_post = AddPost.Field(description="Adds post")

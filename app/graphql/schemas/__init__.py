import graphene as graphene

from schemas import user, post


class Query(post.Query, user.Query, graphene.ObjectType):
    pass


class Mutation(post.Mutation, user.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

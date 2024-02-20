import graphene

import employees.schema


class Query(employees.schema.Query, graphene.ObjectType):
    pass


class Mutation(employees.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

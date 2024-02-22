import graphene
from graphql_auth.schema import UserQuery
from graphql_auth import mutations

import employees.schema


class Query(UserQuery, employees.schema.Query, graphene.ObjectType):
    pass


class AuthMutation(graphene.ObjectType):
   register = mutations.Register.Field() #predefined settings to register user
   verify_account = mutations.VerifyAccount.Field() #used to verify account
   token_auth = mutations.ObtainJSONWebToken.Field() # get jwt to log in


class Mutation(AuthMutation, employees.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

import strawberry
from rooms import schema as rooms_schema

# typing은 코드에 주석을 추가할 수 있게 해줌


@strawberry.type
class Query(rooms_schema.Query): # Query가 rooms_schema.Query를 상속함
    pass

@strawberry.type
class Mutation:
    pass
    

schema = strawberry.Schema(query=Query,) # mutation=Mutation,)
import strawberry
import typing 

# typing은 코드에 주석을 추가할 수 있게 해줌

@strawberry.type
class Movie:
    pk:int
    title:str
    year:int
    rating:int

# strawberry를 사용하면 type annotation을 반드시 써야 함 -> strawberry가 API type을 알 수 있음

movies_db = [
    Movie(pk=1, title="Godfather", year=1990, rating=10),
]

def movies():
    return movies_db

def movie(movie_pk:int): # parameter로 method에 type과 함께 넣어주면 됨
    return movies_db[movie_pk - 1]

def add_movie(title:str, year:int, rating:int):
    new_movie = Movie(pk=len(movies_db) + 1,title=title, year=year, rating=rating)
    movies_db.append(new_movie)
    return new_movie

@strawberry.type
class Query: # Query class는 urls.py와 비슷
    movies: typing.List[Movie] = strawberry.field(resolver=movies)
    movie : Movie = strawberry.field(resolver=movie)

@strawberry.type
class Mutation:
    add_movie: Movie = strawberry.mutation(resolver=add_movie)
    

schema = strawberry.Schema(query=Query, mutation=Mutation,)
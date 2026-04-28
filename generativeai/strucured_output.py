from llm_config import llm 

from pydantic import BaseModel,Field


class Movie(BaseModel):
    title: str = Field(description="Title of the movie")
    year: int = Field(description="Year of the movie")
    director: str = Field(description="Director of the movie")
    rating: float = Field(description="Rating of the movie")

llm_with_schema=llm.with_structured_output(Movie)
response=llm_with_schema.invoke("Tell me about the movie The Godfather")
#print("with pydantic schema",response)
#print("without pydantic schema",llm.invoke("Tell me about the movie The Godfather"))


class Actor(BaseModel):
    name: str = Field(description="Name of the actor")
    role: str = Field(description="Role of the actor")

class MovieWithActors(BaseModel):
    title: str = Field(description="Title of the movie")
    year: int = Field(description="Year of the movie")
    director: str = Field(description="Director of the movie")
    rating: float = Field(description="Rating of the movie")
    actors: list[Actor] = Field(description="List of actors in the movie")

movie_detail=llm.with_structured_output(MovieWithActors)
print("with nested strucuted",movie_detail.invoke("Tell me about the movie The Godfather"))


from typing import TypedDict

class Actor(TypedDict):
    name: str
    role: str

class MovieWithActors(TypedDict):
    title: str
    year: int
    director: str
    rating: float
    actors: list[Actor]

typeddict_schema=llm.with_structured_output(MovieWithActors)
print("with typedict schema",typeddict_schema.invoke("Tell me about the movie The Godfather"))


# example with data classes
from dataclasses import dataclass

@dataclass
class Actor:
    name: str
    role: str

dataclass_schema=llm.with_structured_output(Actor)
print("with dataclass schema",dataclass_schema.invoke("Tell me about the movie The Godfather"))
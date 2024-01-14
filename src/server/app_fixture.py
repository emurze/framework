from fastapi import FastAPI
from pydantic import BaseModel

app_fixture = FastAPI(title="Twitter API")

users = [{"id": 1, "username": "Vlad"}]


class User(BaseModel):
    id: int
    username: str


@app_fixture.get("/users/{user_id}", response_model=list[User])
def get_user(user_id: int):
    return [user for user in users if user["id"] == user_id]

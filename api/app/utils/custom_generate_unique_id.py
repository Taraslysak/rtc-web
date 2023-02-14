from fastapi import APIRouter


def custom_generate_unique_id(route: APIRouter):
    return f"{route.tags[0]}-{route.name}"

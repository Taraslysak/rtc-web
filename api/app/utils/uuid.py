from uuid import uuid4


def gen_uid() -> str:
    return str(uuid4())

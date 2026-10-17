from pydantic import BaseModel, model_validator, field_validator, Field


class Result(BaseModel):
    number: int
    square: int
    delay: float
    time: float


class Response(BaseModel):
    """
    Так как ответы генерируются программой, то в валидации смысла нет
    """

    results: list[Result]
    total_time: float
    parallel_faster_than_sequential: bool

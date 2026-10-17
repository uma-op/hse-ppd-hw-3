from pydantic import BaseModel, model_validator, field_validator, Field


class Request(BaseModel):
    numbers: list[int] = Field(min_length=1)
    delays: list[float] = Field(min_length=1)

    @field_validator("delays", mode="after")
    @classmethod
    def validate_delays_are_positive(cls, delays: list[float]) -> list[float]:
        if any(delay < 0 for delay in delays):
            raise ValueError("Delays must be not negative")

        return delays

    @model_validator(mode="after")
    def validate_length_match(self):
        if len(self.numbers) != len(self.delays):
            raise ValueError("Count of numbers and delays must be equal")

        return self

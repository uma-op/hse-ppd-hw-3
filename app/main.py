import asyncio
import time

from fastapi import FastAPI
from models.request import Request
from models.response import Response, Result

app = FastAPI()


async def square_routine(number: int, delay: float) -> tuple[int, float]:
    start = time.monotonic()
    await asyncio.sleep(delay)
    result = number * number
    end = time.monotonic()
    return result, end - start


@app.post("/calculate/")
async def calculate(request: Request):
    tasks = []
    for number, delay in zip(request.numbers, request.delays):
        tasks.append(asyncio.create_task(square_routine(number, delay)))

    start = time.monotonic()
    results = await asyncio.gather(*tasks)
    end = time.monotonic()

    prepared_results = []
    sequential_execution_time = 0.0
    for number, delay, (square, elapsed) in zip(
        request.numbers, request.delays, results
    ):
        prepared_results.append(
            Result(
                number=number,
                square=square,
                delay=delay,
                time=elapsed,
            )
        )
        sequential_execution_time += delay
    total_elapsed = end - start

    return Response(
        results=prepared_results,
        total_time=total_elapsed,
        parallel_faster_than_sequential=total_elapsed < sequential_execution_time,
    )

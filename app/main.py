import asyncio
import time

from fastapi import FastAPI
from app.models.request import Request
from app.models.response import Response, Result

app = FastAPI()


async def square_routine(number: int, delay: float) -> tuple[int, float]:
    start = time.perf_counter()
    await asyncio.sleep(delay)
    result = number * number
    end = time.perf_counter()
    return result, end - start


@app.post("/calculate/")
async def calculate(request: Request):
    tasks = []
    for number, delay in zip(request.numbers, request.delays):
        tasks.append(asyncio.create_task(square_routine(number, delay)))

    start = time.perf_counter()
    results = await asyncio.gather(*tasks)
    end = time.perf_counter()

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

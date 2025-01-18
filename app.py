import asyncio
import time
from typing import Awaitable, Iterable, TypeVar

from fastapi import FastAPI

T = TypeVar("T")

SECONDS_TO_SLEEP = 5


async def gather_with_concurrency(
    n: int, coroutines: Iterable[Awaitable[T]]
) -> list[T]:
    # inspired by https://stackoverflow.com/a/61478547/2392535
    semaphore = asyncio.Semaphore(n)

    async def semaphore_coro(coro):
        async with semaphore:
            return await coro

    return await asyncio.gather(*(semaphore_coro(c) for c in coroutines))


async def slow_async_task(i: int) -> int:
    await asyncio.sleep(SECONDS_TO_SLEEP)
    return i


def slow_sync_task(i: int) -> int:
    time.sleep(SECONDS_TO_SLEEP)
    return i


app = FastAPI()


@app.get("/sync_baseline")
def sync_baseline():
    i = slow_sync_task(1)
    j = slow_sync_task(2)
    k = slow_sync_task(3)
    return {"message": f"Sync tasks completed with {i}, {j}, {k}"}


@app.get("/async_independent")
async def async_independent():
    i = await slow_async_task(1)
    j = await slow_async_task(2)
    k = await slow_async_task(3)
    return {"message": f"Async tasks completed with {i}, {j}, {k}"}


@app.get("/async_dependent")
async def async_dependent():
    i = await slow_async_task(1)
    j = await slow_async_task(i)
    k = await slow_async_task(j)
    return {"message": f"Async tasks completed with {i}, {j}, {k}"}


@app.get("/async_concurrent")
async def async_concurrent():
    res = await gather_with_concurrency(3, [slow_async_task(i) for i in range(3)])
    return {"message": f"Async tasks completed with {res}"}

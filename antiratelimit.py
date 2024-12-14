import asyncio
from typing import Any, Callable, Optional
from dataclasses import dataclass, field
import heapq


@dataclass(order=True)
class internaltask:
    prio: int
    id: str = field(compare=False)
    run: Callable[[], asyncio.Future] = field(compare=False)
    tries: int = field(default=0, compare=False)
    done: Optional[Callable[[Any], None]] = field(default=None, compare=False)
    fail: Optional[Callable[[Exception], None]] = field(default=None, compare=False)


class antiratelimit:
    def __init__(self, max_req: int, time: int, slots: int = 1, retry: int = 3):
        self.max_req = max_req
        self.time = time / 1000
        self.slots = slots
        self.retry = retry
        self.queue = []
        self.active = 0
        self.used = 0
        self.lock = asyncio.Lock()
        asyncio.create_task(self.reset())

    async def reset(self):
        while True:
            await asyncio.sleep(self.time)
            async with self.lock:
                self.used = 0
            await self.work()

    async def add(self, task_id: str, run: Callable[[], asyncio.Future], prio: int = 0) -> Any:
        loop = asyncio.get_event_loop()

        def done(value):
            fut.set_result(value)

        def fail(err):
            fut.set_exception(err)

        fut = loop.create_future()
        job = internaltask(prio=prio, id=task_id, run=run, tries=0, done=done, fail=fail)

        async with self.lock:
            heapq.heappush(self.queue, job)

        await self.work()
        return await fut

    async def work(self):
        async with self.lock:
            while self.queue and self.active < self.slots and self.used < self.max_req:
                job = heapq.heappop(self.queue)
                self.active += 1
                self.used += 1

                asyncio.create_task(self.run_job(job))

    async def run_job(self, job: internaltask):
        try:
            res = await job.run()
            job.done(res)
        except Exception as e:
            if job.tries < self.retry:
                job.tries += 1
                async with self.lock:
                    heapq.heappush(self.queue, job)
            else:
                job.fail(e)
        finally:
            async with self.lock:
                self.active -= 1
            await self.work()

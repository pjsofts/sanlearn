import asyncio

from sanic.response import json

from app import app

pq = asyncio.PriorityQueue(maxsize=10)


@app.route("/max10")
async def test(request):
    number = int(request.args.get("number", 0))
    print(number)
    if not pq.full():
        pq.put_nowait((number,))
    else:
        min = await pq.get()
        if number > min[0]:
            await pq.put((number,))
        else:
            await pq.put(min)
    return json({"max10": str([number[0] for number in pq._queue])})

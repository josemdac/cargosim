#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import datetime
import random
import websockets
from main import main
import json
import functools

async def simulate(websocket, path):
    data = json.loads(await websocket.recv())
    #print(data)
    if data['command'] == 'simulate':
        args = data['args']
        fut = await websocket.send('Started simulation')
        fn = functools.partial(main, args)
        result = await asyncio.get_event_loop().run_in_executor(None, fn)
        await websocket.send(json.dumps(result))


start_server = websockets.serve(simulate, "127.0.0.1", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
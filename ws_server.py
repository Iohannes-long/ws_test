import argparse
import signal
import asyncio
import websockets
import json
import threading

_app_exit = False
def _quit(signum, frame):
    global _app_exit
    _app_exit =True
    print('waiting to close')
    
_config = {
    "data": [],
    "index_data": 0,
    'wait_ms': None,
    'be_json': False,
    "be_loop": False,
    "be_echo": False
}
            
async def _send(websocket, message):
    try:
        await websocket.send(message)
    except websockets.ConnectionClosed:
        pass  

_CONNECTIONS = set()
async def _handler(websocket):
    _CONNECTIONS.add(websocket)
    print('new client connected')  
    if _config['be_echo']:
        async for msg in websocket:
            await _send(websocket, msg)
            print(msg)   
            
async def _message_all():
    global _config
    global _app_exit
    while not _app_exit:
        wait = _config['wait_ms']
        if wait is None:
            wait = 1
        wait = wait/1000.0
        await asyncio.sleep(wait)
        if _config['index_data'] >= len(_config['data']):
            if  _config['be_loop']:
                _config['index_data'] = 0
            else:
                break
        msg = _config['data'][_config['index_data']]
        if _config['be_json']:
            msg = json.dumps(msg)
        # print(msg)
        for websocket in _CONNECTIONS:
            asyncio.create_task(_send(websocket, msg))
        _config['index_data'] = _config['index_data'] + 1 
    _CONNECTIONS.clear()
    print('exit app')
    

async def main(url, data, file, split_flag, wait_ms, be_json, be_loop, be_echo):
    global _app_exit
    global _config
    _config['wait_ms'] = wait_ms
    _config['be_json'] = be_json
    _config['be_loop'] = be_loop
    _config['be_echo'] = be_echo
    
    if data is not None:
        if split_flag is not None:
            _config['data'] = data.split(split_flag)
        else:
            _config['data'] = [data]
    elif file is not None:
        pf = open(file, "r")
        data = pf.read()
        if be_json:
            _config['data'] = json.loads(data)
        else:
            if split_flag is not None:
                _config['data'] = data.split(split_flag)
            else:
                _config['data'] = [data]
    # print(_config['data'])
    url = url.replace('ws://', '')
    index = url.find(':')
    port = 80
    if index >= 0:
        port = url[index+1:]
        url = url[:index]
        index = port.find('/')
        if index >= 0:
            port = port[:index]
            url = url + port[index:]
    async with websockets.serve(_handler, url, port):
        await _message_all()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, _quit)
    signal.signal(signal.SIGTERM, _quit)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', dest='url', type=str, default='ws://127.0.0.1', help='ws://x.x.x.x[:y]/z')
    parser.add_argument('-d', dest='data', type=str, default=None, help='the data to send')
    parser.add_argument('-f', dest='file', type=str, default=None, help='the file to send')
    parser.add_argument('-s', dest='split', type=str, default=None, help='split flag with two data')
    parser.add_argument('-w', dest='wait', type=float, default=1000, help='ms wait after send data')
    parser.add_argument('-j', dest='json', type=int, default=1, help='the file is json')
    parser.add_argument('-e', dest='echo', type=int, default=1, help='echo client data')
    parser.add_argument('-l', dest='loop', type=int, default=1, help='loop to send data')
    args = parser.parse_args()
    be_json = True if args.json == 1 else False
    be_loop = True if args.loop == 1 else False
    be_echo = True if args.echo == 1 else False
    asyncio.run(main(args.url, args.data, args.file, args.split, args.wait, be_json, be_loop, be_echo))
    
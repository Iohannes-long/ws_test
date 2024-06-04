import websocket
import rel
import argparse
import sys


_config = {
    'url': None,
    'file': None,
    'split': None,
    'be_json': True,
    'be_first': True,
    'qty': -1,
}

def _my_print(pf, data, be_first, split_flag, be_json):
    if pf is not None:
        if be_first:
            if be_json:
                pf.write(f'[')
            else:
                pass
        else:
            if be_json:
                pf.write(f',\r\n')
            else:
                pf.write(split_flag)
        pf.write(data)
        pf.flush()
    else:
        print(data)
        
def _my_print_end(pf, be_json):
    if pf is None:
        return
    if be_json:
        pf.write(f']')

def on_message(ws, data):
    global _config
    _my_print(_config['file'], data, _config['be_first'], _config['split'], _config['be_json'])
    if _config['qty'] is not None and _config['qty'] > 0:
        print(_config['qty'])
        _config['qty'] -= 1
        if _config['qty'] == 0:
            ws.close()
            on_close(ws, None, None)
    else:
        pass
    if _config['be_first']:
        _config['be_first'] = False

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    global _config
    _my_print_end(_config['file'], _config['be_json'])
    print("### closed ###")
    sys.exit(0)

def on_open(ws):
    print("Opened connection")
    
def main(url, file, split, be_json, qty):    
    global _config
    _config['url'] = url
    _config['file'] = file
    _config['split'] = split
    _config['be_json'] = be_json
    _config['qty'] = qty
    
    if file is not None and file != '':
         pf = open(file, "w")
         _config['file'] = pf
    
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(url,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)
    rel.signal(2, rel.abort)
    rel.dispatch()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', dest='url', type=str, default='http://127.0.0.1', help='ws://x.x.x.x[:y]/z')
    parser.add_argument('-f', dest='file', type=str, default=None, help='the file to send')
    parser.add_argument('-s', dest='split', type=str, default=None, help='split flag with two data')
    parser.add_argument('-j', dest='json', type=int, default=1, help='the file is json')
    parser.add_argument('-n', dest='num', type=int, default=None, help='the num of receive server data times')
    args = parser.parse_args()
    be_json = True if args.json == 1 else False
    main(args.url, args.file, args.split, be_json, args.num)
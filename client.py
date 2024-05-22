import argparse
import signal
import json
from websockets.sync.client import connect

_app_exit = False
def _quit(signum, frame):
    global _app_exit
    _app_exit =True
    print('waiting to close')
    
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
    else:
        print(data)
        
def _my_print_end(pf, be_json):
    if be_json:
        pf.write(f']')

def main(url, outfile, num, split_flag, be_json):
    global _app_exit
    
    qty = -1
    if num is not None:
        qty = num
    pf = None
    if outfile is not None:
        pf = open(outfile, "w")
    with connect(url) as session:
        print(f'has connected {url}')
        be_first = True
        while not _app_exit and qty != 0:
            data = session.recv()
            if be_json:
                parsed_data = json.loads(data)
                data = json.dumps(parsed_data, indent=4, sort_keys=False)            
            _my_print(pf, data, be_first, split_flag, be_json)
            if qty > 0:
                qty -= 1
            be_first = False
    if pf is not None:
        _my_print_end(pf, be_json)
        pf.close()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, _quit)
    signal.signal(signal.SIGTERM, _quit)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', dest='url', type=str, default='ws://127.0.0.1', help='ws://x.x.x.x[:y]/z')
    parser.add_argument('-f', dest='outfile', type=str, default=None, help='file name output data to')
    parser.add_argument('-n', dest='num', type=int, default=None, help='the num of receive server data times')
    parser.add_argument('-s', dest='split', type=str, default='@@@', help='split flag of two data')
    parser.add_argument('-j', dest='json', type=int, default=1, help='data is json or not')
    args = parser.parse_args()
    be_json = True if args.json == 1 else False
    main(args.url, args.outfile, args.num, args.split, be_json)
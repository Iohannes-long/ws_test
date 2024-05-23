import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
    
_config = {
    "method": 'GET',
    "data": None,
    'be_json': False
}
            
class Resquest(BaseHTTPRequestHandler):    
    def _send_msg(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json;text/plain;text/html;application/octet-stream')            
        self.end_headers()
        msg = _config['data']
        if msg is None:
            msg = 'None'
        self.wfile.write(msg.encode('utf-8'))
    
    def do_GET(self):
        global _config
        # print(_config)
        if _config['method'].lower() == 'get':
            self._send_msg()
        else:
            self.send_response(200)            
        
    def do_POST(self):
        global _config
        if _config['method'].lower() == 'post':
            self._send_msg()
        else:
            self.send_response(200)
    

def main(url, method, data, file):
    global _config
    _config['method'] = method
    
    if data is not None:
        _config['data'] = data
    elif file is not None:
        pf = open(file, "r")
        data = pf.read()
        _config['data'] = data            
    # print(_config['data'])
    url = url.replace('http://', '')
    index = url.find(':')
    port = 80
    if index >= 0:
        port = url[index+1:]
        url = url[:index]
        index = port.find('/')
        if index >= 0:
            port = port[:index]
            url = url + port[index:]
    with HTTPServer((url, int(port)), Resquest) as httpd:
        print('app start')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.shutdown()
    print('app exit')

if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', dest='url', type=str, default='http://127.0.0.1', help='ws://x.x.x.x[:y]/z')
    parser.add_argument('-m', dest='method', type=str, default='GET', help='GET or POST')
    parser.add_argument('-d', dest='data', type=str, default=None, help='the data to send')
    parser.add_argument('-f', dest='file', type=str, default=None, help='the file to send')
    args = parser.parse_args()
    main(args.url, args.method, args.data, args.file)
    
# ws_test

## to test server
``` shell
python .\client.py
```

### receive json data from server
``` shell
python .\client.py -u ws://127.0.0.1:8888/my_data
```
- -u default is ws://127.0.0.1

### receive json data
``` shell
python .\client.py -j 1
```
- -j default is 1 (json data)

### receive data to file and data split with flag
``` shell
python .\client.py -f 1.txt -j 0 -s @@@
```
- -s will be ignored if -j 1
- -s default is @@@

### receive data to json file
``` shell
python .\client.py -f 1.json
```
- -s will be ignored if -j 1

### receive 3 data from server
``` shell
python .\client.py -n 3 -j 0
```
- -n default value is None (reveive data allways)

## to test server
``` shell
python .\server.py -d 'hellow world'
```

### publish data
``` shell
python .\server.py -p 8888 -d 'hellow world'
```
- -p default value is 80

### publish data in loop with 1000 ms onece
``` shell
python .\server.py -d 'hellow world' -l 1 -w 1000
```
- -l default value is 1 (loop publish data)
- -w default value is 1000 (1 sec)

### publish data with split flag

``` shell
python .\server.py -d 'hellow world@@@jack is here@@@come baby' -s @@@  -w 1000
```
- -s default value is None (str as one data)
- -w default value is 1000 (1 sec)

### publish file with split flag
``` shell
python .\server.py -f '1.txt' -s @@@
```
- -f will be ignore if -d is set

### publish json file

``` shell
python .\server.py -f '1.json' -j 1
```
- -j default value 1 (json file)
- -s will be ignore if -j 1
- -f will be ignore if -d is set

### publish json data

``` shell
python .\server.py -d "{'a':1,'b:2'}"
```
- -j default value 1 (json format)
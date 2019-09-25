## Requirements
- Python3 
- Paho

use this to install 

``` 
pip3 install paho-mqtt python-etcd 
```

## How to Run
1. Open terminal and execute this command

```
mosquito_sub -t /
```

##### mosquitto_sub create a host to listen other devices in network

2. Open another terminal and execute this

```
python3 interface.py
```

##### this command show the inteface to controle all devices

3. On another terminal run any of the other files 

##### the other files simulate network devices that communicate with the broker

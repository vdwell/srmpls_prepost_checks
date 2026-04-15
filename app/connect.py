#!/usr/bin/python3


from netmiko import ConnectHandler
from netmiko.base_connection import BaseConnection
import pprint
import logging

logger = logging.getLogger(__name__)



def connect_to_devices(mydict:dict[str,dict[str,str]], csv_content:list[list[str]]):

    result: list[list[BaseConnection, str, str, str, str]] = [] # connection_object, mgmt_ip, hostname, device_type, loopback_ip

    username: str = mydict['parameters']['username']
    password: str = mydict['parameters']['password']

    for index, device_data in enumerate(csv_content):
        worklist: list[BaseConnection, str, str, str] = []
        if index == 0:
            continue
        else:
            device_type: str = device_data[2]
            mgmt_ip: str = device_data[0]
            device_name: str  = device_data[1]
            loopback_ip: str = device_data[3]

            device: dict[str,str] = {'device_type': device_type, 
                                    'host': mgmt_ip, 
                                    'username': username, 
                                    'password': password,
                                    }

            net_connect_object: BaseConnection = ConnectHandler(**device)
            worklist.append(net_connect_object) # list item #0
            worklist.append(mgmt_ip) # list item #1
            worklist.append(device_name) # list item #2
            worklist.append(device_type) # list item #3
            worklist.append(loopback_ip) # list item #4
            result.append(worklist)

    return result



def disconnect_from_devices(connections: list[BaseConnection, str, str, str]):

    for connection in connections:
        try:
            connection[0].disconnect()
            logger.info(f"Disconnected from {connection[1]}")
        except Exception as e:
            logger.warning(f"Error disconnecting from {connection[1]}: {e}")

if __name__ == "__main__":
    pass
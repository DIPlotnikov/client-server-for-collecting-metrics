#!/usr/bin/python3
# -*- coding: utf-8 -*-

# The client part of the application for collecting metrics from the user's computer. In this case, the metrics are:
# memory state, CPU load, and more.
# Includes several commands:
# get (request data) - returns previously saved information from the server.
# Enables the get (*) option, which returns all the information stored on the server.
# put () - the method accepts as parameters: the name of the metric,
# a numeric value, and an optional named timestamp parameter.
# If the user called the put method without the timestamp argument, the client automatically substitutes
# the timestamp value

# D.Plotnikov 2021


import socket
import time


class Client:


    def __init__(self, HOST, PORT, timeout=None):
        """Client for sending metrics to the server."""
        self.HOST = HOST
        self.PORT = PORT
        try:
            self.con = socket.socket()
            self.con.connect((self.HOST, self.PORT))
            self.con.settimeout(timeout)
        except:
            raise ClientSocketError("error create connection", socket.error)

    def _reading(self):
        """function for reading the server response"""
        data = b""
        try:
            data += self.con.recv(1024)
        except:
            raise ClientSocketError("error create connection", socket.error)
        data = data.decode()
        status, response = data.split("\n", 1)
        if status == "ok":
            return response
        else:
            raise ClientSocketError("error recv data", socket.error)

    def put(self, key, value, nowtime=int(time.time()+2)):
        """function for sending user metrics to the server"""
        try:
            self.con.sendall(f"put {key} {value} {nowtime}\n".encode())
        except:
            raise ClientProtocolError("error send data", socket.error)
        print(self._reading())

    def get(self, key):
        """function for getting information from the server"""
        try:
            self.con.sendall(f"get {key}\n".encode())
        except:
            raise ClientSocketError("error send data", socket.error)
        raw_data = self._reading()
        data = {}
        if raw_data == "":
            return data

        raw_data = raw_data.split("\n")
        try:
            for elem in raw_data:
                if elem != "":
                    elem = elem.split()
                    key = elem[0]
                    value = elem[1]
                    timestamp = elem[2]
                    if key not in data:
                        data[key] = []
                    data[key].append((int(timestamp), float(value)))
                    data[key].sort()
        except:
            raise ClientError()
        else:
            return data


    def close(self):
        self.con.close()

 # exceptions
class ClientError(Exception):
    pass


class ClientSocketError(ClientError):
    pass


class ClientProtocolError(ClientError):
    pass

if __name__ == "__main__":
    client = Client("127.0.0.1", 8888, timeout=5)
    client.put("test", 0.5, nowtime=1)
    client.put("test", 2.0, nowtime=2)
    client.put("test", 0.5, nowtime=3)
    client.put("load", 3, nowtime=4)
    client.put("load", 4, nowtime=5)
    print(client.get("*"))

    client.close()

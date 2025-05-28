#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program to test for the udp_server.py to emulate the sending of 
data as a MoleNet board.
 
@author: Asanga Udugama (adu@comnets.uni-bremen.de)
@date:   2025-04-03
"""

import socket
import random
import time
import argparse


# Start the server
def start_udptester():
    
    ## parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--sendaddress', help='IP address to send to',
                        required=False, default='127.0.0.1')
    parser.add_argument('-p', '--sendport', type=int, help='UDP Port to send to',
                        required=False, default=9999)
    args = parser.parse_args()


    ## initialization
    random.seed(128)

    # setup socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # send data in a loop
    seq = 0
    while True:
        hum = round(random.uniform(50, 60), 2)
        temp = round(random.uniform(20, 23), 2)
        msg = '12345678 ; ' + str(seq) + ' ; ' + str(hum) + ' ; ' + str(temp)
        byt = msg.encode()
        sock.sendto(byt, (args.sendaddress, args.sendport))
        time.sleep(5)
        seq = seq + 1


if __name__ == "__main__":
    start_udptester()
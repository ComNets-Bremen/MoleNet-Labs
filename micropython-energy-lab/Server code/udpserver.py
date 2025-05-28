#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Collect UDP data received from any program (specifically the MoleNet setup) 
from the students of the IoT Course Arduino Lab. Data is collected
as folows.

- dumps received data as lines on terminal
- dumps received data as lines to a file (created with data as prefix)
 
@author: Asanga Udugama (adu@comnets.uni-bremen.de)
@date:   Sun Jul 30 12:11:39 2023

"""
import socket
import datetime
import os
import argparse
import time


# Start the server
def start_udpreceiver():
    
    ## parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bindaddress', help='IP address to bind to',
                        required=False, default='127.0.0.1')
    parser.add_argument('-p', '--bindport', type=int, help='UDP Port to bind to',
                        required=False, default=9999)
    args = parser.parse_args()

    ## create fresh output file to dump data
    filename = './udp-' + datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S') + '-data.txt'
    fp = open(filename, 'w')

    # setup socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.bindaddress, args.bindport))

    # console message
    print('UDP: Starting server...')
    print('UDP: Details: ')
    print('UDP:   Socket ' + args.bindaddress + ':' + str(args.bindport))
    print('UDP:   File ' + filename)

    # loop to receive and dump data
    while True:
        failed = False
        try:
            data, addr = sock.recvfrom(1024)
            try:
                msg = data.decode()
                writestr = 'UDP: ' + datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + ' - ' + addr[0] + ' - ' + msg + '\n'
            except:
                writestr = 'UDP: ' + datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + ' - ' + addr[0] + '\n'
                failed = True
        except:
            writestr = 'UDP: ' + datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + ' - ' + 'Error in the read data (who\'s the culprit)' + '\n'
            failed = True

        # write to terminal
        print(writestr, end='')
    
        # write to file
        fp.write(writestr)
        fp.flush()
        os.fsync(fp)
    
        # if there was an exception, wait before receiving again
        if failed:
            time.sleep(2)

if __name__ == "__main__":
    start_udpreceiver()
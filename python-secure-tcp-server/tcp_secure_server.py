#******************************************************************************
# File Name:   tcp_secure_server.py
#
# Description: A simple secure TCP server for demonstrating TCP usage.
# 
#******************************************************************************
# (c) 2019-2020, Cypress Semiconductor Corporation. All rights reserved.
#******************************************************************************
# This software, including source code, documentation and related materials
# ("Software"), is owned by Cypress Semiconductor Corporation or one of its
# subsidiaries ("Cypress") and is protected by and subject to worldwide patent
# protection (United States and foreign), United States copyright laws and
# international treaty provisions. Therefore, you may use this Software only
# as provided in the license agreement accompanying the software package from
# which you obtained this Software ("EULA").
#
# If no EULA applies, Cypress hereby grants you a personal, non-exclusive,
# non-transferable license to copy, modify, and compile the Software source
# code solely for use in connection with Cypress's integrated circuit products.
# Any reproduction, modification, translation, compilation, or representation
# of this Software except as specified above is prohibited without the express
# written permission of Cypress.
#
# Disclaimer: THIS SOFTWARE IS PROVIDED AS-IS, WITH NO WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, NONINFRINGEMENT, IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. Cypress
# reserves the right to make changes to the Software without notice. Cypress
# does not assume any liability arising out of the application or use of the
# Software or any product or circuit described in the Software. Cypress does
# not authorize its products for use in any products where a malfunction or
# failure of the Cypress product may reasonably be expected to result in
# significant property damage, injury or death ("High Risk Product"). By
# including Cypress's product in a High Risk Product, the manufacturer of such
# system or application assumes all risk of such use and in doing so agrees to
# indemnify Cypress against all liability.
#******************************************************************************/

#!/usr/bin/python

import socket, ssl
import optparse
import time
import sys


def echo_server(host, port):
    print("==========================")
    print("TCP Secure Server")
    print("==========================")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    try:
        s.bind((host, port))
        s.listen(1)
    except socket.error as msg:
        print("ERROR: ", msg)
        s.close()
        s = None

    if s is None:
        sys.exit(1)

    while 1:
        print("Listening on: %s:%d"%(host, port))
        data_len = 0
        try:
            conn, addr = s.accept()
            connstream = ssl.wrap_socket(conn,
                                 server_side=True,
                                 certfile="server.crt",
                                 keyfile="server.key", ca_certs='root_ca.crt', cert_reqs=ssl.CERT_REQUIRED)
        except KeyboardInterrupt:
            print("Closing Connection")
            s.close()
            s = None
            sys.exit(1)

        print('Incoming connection accepted: ', addr)

        try:
            while 1:
                data = input("Enter your option: '1' to turn ON LED, 0 to trun OFF LED and Press the 'Enter' key: ")
                connstream.write(data.encode())
                data = connstream.read(4096)
                if not data: break
                print("Acknowledgement from TCP Client:", data.decode('utf-8'))
                print("")
                
        except KeyboardInterrupt:
            print("Closing Connection")
            s.close()
            s = None
            sys.exit(1)

        conn.close()

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("-p", "--port", dest="port", type="int", default=50007, help="Port to listen on [default: %default].")
    parser.add_option("--hostname", dest="hostname", default="", help="Hostname to listen on.")

    (options, args) = parser.parse_args()

    echo_server(options.hostname, options.port)

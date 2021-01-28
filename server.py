import socketserver, os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        request = self.data.split()
        request_method = request[0].decode('utf-8')
        request_path = request[1].decode('utf-8')
        location = "http://127.0.0.1:8080" + request_path + "/\n\n"

        if (request_method != "GET"):
            stat_code = "HTTP/1.1 405 Method Not Allowed\nContent Type: text/html"
            self.request.sendall(bytearray(stat_code, 'utf-8'))
            return
        
        current_directory = os.path.abspath(os.getcwd()+'/www')
        full_path = current_directory + request_path
        location = "http://127.0.0.1:8080" + request_path + "/\n\n"
        
        if (os.path.isfile(full_path)):
            if full_path.endswith(".html"):
                mime_type = "text/html"
                content = open(full_path, 'r').read()
                stat_code = ("HTTP/1.1 200 OK\nContent-Type:" +mime_type+"\nConnection: closed\n\n"+content)
                self.request.sendall(bytearray(stat_code, 'utf-8'))
                    
            elif full_path.endswith(".css"):
                mime_type = "text/css"
                content = open(full_path, 'r').read()
                stat_code = ("HTTP/1.1 200 OK\nContent-Type:" +mime_type+"\nConnection: closed\n\n"+content)
                self.request.sendall(bytearray(stat_code, 'utf-8'))
                    
            else:
                mime_type = "text/html"
                stat_code = ("HTTP/1.1 404 Not Found\nContent-Type:" + mime_type + "\nConnection: closed\n\n")
                self.request.sendall(bytearray(stat_code, 'utf-8'))

        elif (os.path.isdir(full_path)):
            if full_path.endswith("/"):
                full_path += "index.html"
                mime_type = "text/html"
                content = open(full_path, 'r').read()
                stat_code = ("HTTP/1.1 200 OK\nContent-Type:" +mime_type+"\nConnection: closed\n\n"+content)
                self.request.sendall(bytearray(stat_code, 'utf-8'))

            else:
                full_path = request_path + "/"
                stat_code = ("HTTP/1.1 301 Moved Permanently\nLocation:"+location)
                self.request.sendall(bytearray(stat_code, 'utf-8'))
                
        else:
            mime_type = "text/html"
            stat_code = ("HTTP/1.1 404 Not Found\nContent Type:" +mime_type+"\nConnection: closed\n\n")
            self.request.sendall(bytearray(stat_code, 'utf-8'))
            return
                
            

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

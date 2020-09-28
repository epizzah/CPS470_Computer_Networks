import haynesAS1URLParser
import haynesAS1socket
import haynesAS1request
import time
import sys
from queue import Queue

import haynesAS1statuscode


def main():
    Q = Queue()
    print("number of urls:", Q.qsize())
    ps = haynesAS1URLParser.URLParser()    # create an url parser object
    r = haynesAS1request.Request()         # create a request builder object
    ws = haynesAS1socket.TCPsocket()       # create a tcp socket object
    s = haynesAS1statuscode.StatusCode()   # create a status code
    try:
        with open("URL-input-100.txt") as file:
            for line in file:
                Q.put(line)
    except IOError:
        print('No such file')
        exit(1)
    count = 0
    size = 0
    hostTable = set()
    while not Q.empty():
        count = count + 1
        print(count)
        url = Q.get()
        host, port, path, query = ps.parse(url)
        print("URL:  " + url)
        print("Parsing URL... host " + str(host) + ", port " + str(port) + ", request")
        # check host uniqueness

        hostTable.add(host)
        print("Check for IP uniqueness...")
        if size < len(hostTable):
            print("passed")
            size = size + 1
        else:
            print("fail")
            continue

        print("Doing DNS...")
        tic = time.perf_counter()
        ip = ws.getIP(host)
        if ip == None:
            continue
        toc = time.perf_counter()
        print(f"Done in {toc - tic:0.4f} ms, found " + ip)

        print("Connecting on robots...")
        msg = r.headRequest(host)
        # send header request for robots // for politeness
        ws.createSocket()
        ws.connect(ip, port)
        if ws.sock == None:
            # failed to connect
            continue
        tic = time.perf_counter()
        ws.send(msg)
        toc = time.perf_counter()
        print(f"Done in {toc - tic:0.4f} ms")

        print("Loading...")
        tic = time.perf_counter()
        data = ws.receive()  # receive a reply from the server
        toc = time.perf_counter()
        print(f"done in {toc - tic:0.4f} ms with " + str(len(data)) + " bytes")

        # process the reply to see if it contains 200 OK, use find
        print("Verifying header")
        status = s.CheckStatus(data)
        if status == 'OK':  # if 200, no get request
            # not allowed to send tcp (politeness :)
            print("status code 200")
            ws.close()
        else:
            print("Status Code: " + status)
            request = r.getRequest(host, path, query)
            print("Request: ", request)
            ws.crawl(host, port, request)  # host: str, port: int, request: str

# call main() method
if __name__ == "__main__":
    main()

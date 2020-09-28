class Request:
    def __init__(self):
        self.request = ''  # a string
        self.agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'

    def getRequest(self, host, path, query):
        """Build an HTTP GET request"""
        #self.request = 'GET ' + path + query + ' HTTP/1.0' + '\nHost: ' + host + '\nConnection : close\n\n'
        self.request = 'GET ' + path + query + ' HTTP/1.0' + '\nHost: ' + host + '\n' + self.agent + '\n\n'
        return self.request

    def headRequest(self, host):
        """Build a HEAD request, to check if host has "robots.txt" file """
        self.request = 'HEAD /robots.txt HTTP/1.0\n' + 'Host: ' + host + '\n' + self.agent + '\n\n'
        return self.request

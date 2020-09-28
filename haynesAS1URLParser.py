# urlparser.py

class URLParser:
    def __init__(self):
        print ("create an object of URLParser")

    def parse(self, string):
        self.query = ''   # default query is an empty string
        self.port = '80'  # default 80 for http
        self.host = ''
        self.path = '/'

        index = string.find('\n')
        if index != -1:
            # index = where '\n' is located
            #string = string[index:]  # remove line break
            string = string.replace("\n", "")
        # remove 'http://'
        index = string.find('://')
        if index != -1:
            string = string[index + 3:]

        # remove fragment from url
        index = string.find('#')
        if index != -1:
            string = string[:index]

        # remove user:pass@ if exists
        index = string.find('@')
        if index != -1:  # if it is found string
            string[index:]  # strip fragment

        # find the query
        index = string.find('?')
        if index != -1:
            self.query = string[index:]
            string = string[:index]

        # host[:port][/path]
        # find the path
        index = string.find('/')
        if index != -1:
            self.path = string[index:]
            string = string[:index]

        # host[:port]
        index = string.find(':')
        if index != -1:  # if port found
            self.port = string[index + 1:]
            string = string[:index]

        # host
        self.host = string


        return self.host, int(self.port), self.path, self.query

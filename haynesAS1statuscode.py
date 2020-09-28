class StatusCode:
    # list our instance variables
    # constructor
    def __init__(self):
        self.d = dict([
            ('200', 'OK'),
            ('301', 'Moved Permanently'),
            ('302', 'Found (Previously Moved Temporarily)'),
            ('400', 'Bad Request'),
            ('401', 'Unauthorized'),
            ('403', 'Forbidden'),
            ('404', 'Not Found'),
            ('408', 'Request Timeout'),
            ('timeout', 'timeout'),
            ('unknown', 'unknown')
            ])

    def CheckStatus(self, data):
        if len(data) == 0:
            return self.d['timeout']

        if data.decode('utf-8').find('200') != -1:
            return self.d['200']
        if data.decode('utf-8').find('301') != -1:
            return self.d['301']
        if data.decode('utf-8').find('302') != -1:
            return self.d['302']
        if data.decode('utf-8').find('400') != -1:
            return self.d['400']
        if data.decode('utf-8').find('401') != -1:
            return self.d['401']
        if data.decode('utf-8').find('403') != -1:
            return self.d['403']
        if data.decode('utf-8').find('404') != -1:
            return self.d['404']
        if data.decode('utf-8').find('408') != -1:
            return self.d['408']
        else:
            return self.d['unknown']
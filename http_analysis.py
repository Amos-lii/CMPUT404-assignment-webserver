# return status code
import time


class StatusCode(object):
    Ok="HTTP/1.1 200 OK\r\n"
    NotFound="HTTP/1.1 404 Not Found\r\n"
    Redirect="HTTP/1.1 301\r\n"
    NotAllowedMethod="HTTP/1.1 405 \r\n"

#The type of content
class ContentType(object):
    HTML="text/html"
    CSS="text/css"


#handle the request

class HandleRequest(object):

    def __init__(self):
        self.method=None
        self.filename=None
        self.request_version=None
        self.status=None
        self.contentType=None
        self.date=None
        self.body=None
        self.connectionlenght=None

    def read_file(self,filename):
        f=open(filename,'rb')
        Body=f.read()
        f.close()
        self.body=Body

    def extract_data(self,data):
        dataList = data.splitlines()
        if len(dataList) > 0:
            requestHeaderLines = dataList[0]
            requestHeaderList = requestHeaderLines.decode().split(' ')
            self.filename = requestHeaderList[1]
            print(self.filename)
            self.method = requestHeaderList[0]
            self.request_version = requestHeaderList[2]


    def handleResponse(self, data):
        self.extract_data(data)
        print(data)
        if self.method.lower() != "get":
            self.date = time.asctime()
            self.status = StatusCode.NotAllowedMethod
            response = self.status + "Date: " + self.date + '\r\n'
            return response
        else:
            if self.filename == '/':
                self.filename = './www/index.html'
                self.status = StatusCode.Ok
            elif '.' not in self.filename and self.filename[-1]!='/':
                self.filename = './www' + self.filename + '/index.html'
                self.status = StatusCode.Redirect

            elif '.' not in self.filename:
                self.filename = "./www"+self.filename+"index.html"
            else:
                self.filename='./www'+self.filename

            if ".css" in self.filename or '.html' in self.filename:

                try:
                    self.read_file(self.filename)

                except:
                    self.status=StatusCode.NotFound
                    self.date=time.asctime()
                    response=self.status+"Date: "+self.date+'\r\n'+"Connection:close\r\n"
                    return response
                else:
                    if '.html' in self.filename:
                        self.contentType=ContentType.HTML
                    elif '.css' in self.filename:
                        self.contentType=ContentType.CSS
                    if self.status==None:
                        self.status=StatusCode.Ok
            else:
                self.status = StatusCode.NotFound
                self.date = time.asctime()
                response = self.status + "Date: " + self.date + '\r\n'+"Connection:close\r\n"
                return response
            self.date = time.asctime()
            self.connectionlenght=len(self.body)
            response = self.status+"Date: "+self.date+'\r\n'+"Content-Length: "+str(self.connectionlenght)+'\r\n'+"content-type: "+self.contentType+'\r\n\r\n'+self.body.decode()
            return response






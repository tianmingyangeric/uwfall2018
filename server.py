from wsgiref.simple_server import make_server
from application import application

if __name__ == '__main__':
    httpd = make_server('localhost', 8080, application)
    print("SERVER RUN ON 8080")
    httpd.serve_forever()
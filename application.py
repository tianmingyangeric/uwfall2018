from urllib.parse import parse_qs
import decision_tree


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
#   method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    d = parse_qs(environ['QUERY_STRING'])
    user = d.get('user', [''])
    result="This is a test for back end server"
    if (user[0] == '0'):
        result = "user1"
    if (user[0] == '1'):
        a, b, c = decision_tree.run_dt()
        result = a + b + c
    return [result.encode()]
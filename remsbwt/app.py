import falcon
import json

# import all services
from services import info, queue

def get_app():
    api = application = falcon.API()

    mapper = {}
    inf = info.Info()
    tqr = queue.TaskQueueRouter(mapper)


    api.add_route('/info', inf)
    api.add_route('/queue/{token}', tqr)


    return api








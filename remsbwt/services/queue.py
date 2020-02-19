import falcon
import json
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import uuid

from services.info import get_target

class TaskQueueRouter(object):

    def __init__(self, tqueue):
        self.tqueue = tqueue

    def on_get(self, req, resp, token):

        try:
            inf = self.tqueue.taskmap[token]
            resp.body = json.dumps(inf, ensure_ascii=False)
        except KeyError:
            resp.body = falcon.HTTPBadRequest(
                "Token Not Found",
                "Tasks must be submitted to the queue before querying status."
            ).to_json()
            resp.status = falcon.HTTP_404

    def on_post(self, req, resp):
        b = json.loads(req.bounded_stream.read(), encoding='utf-8')
        tasks = b["tasks"]
        targets = []
        for t in tasks:
            targets.append(t["target"])
            t["status"] = "SUBMITTED"
            t["result"] = None
            t["error"]  = None
        validate_target(targets)
        try:
            self.tqueue.submit(tasks)
            resp.status = HTTP_200
        except e:
            resp.status = falcon.HTTP_503
        resp.body = json.dumps(tasks)


    def validate_target(target):
        if target != info.get_target():
            raise falcon.HTTPError(falcon.HTTP_422, "Invalid Targets",
                                   f'{len(ivts)} Invalid targets. Please see /info for valid targets')

class TaskQueue(object):

    def __init__(self, target, maxw=-1, db=None):
        # If no constraint specified, select good balance
        if maxw == -1:
            maxw = multiprocessing.cpu_count() * 2 + 1

        self.pool = ThreadPoolExecutor(max_workers = maxw)
        self.taskmap = {}
        self.db = db
        self.target = target

    def submit(tasks):
        token = new_token()
        self.taskmap[token] = m = tasks
        for i, task in enumerate(m):
            ar = [token, i, task]
            self.pool.submit(ex_func, *ar)

    def ex_func(self, token, n, task):
        try:
            f = getattr(self.target, task["func"])
            self.taskmap[token][n]["status"] = "RUNNING"
            result = f(*task["args"], **task["kwargs"])
            self.taskmap[token][n]["status"] = "FINISHED"
            self.taskmap[token][n]["result"] = result
        except Exception as e:
            self.taskmap[token][n]["status"] = "FAILED"
            self.taskmap[token][n]["result"] = e.__str__()

def new_token():
    return uuid.SafeUUID()








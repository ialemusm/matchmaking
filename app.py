from flask import Flask, request
import redis
from rq import Queue

import time

app = Flask(__name__)

r = redis.Redis()
q = Queue(connection=r)

def background_task(n):

    """ Function that returns len(n) and simulates a delay """

    print("Task running")

    print(len(n))
    print("Task complete")

    return len(n)

@app.route("/task")
def index():

    if request.args.get("n"):

        job = q.enqueue_call(func=background_task,
               args=('http://nvie.com',),
               timeout=30)

        q_len = len(q)

        print(q_len)
        return f"Task ({job.id}) added to queue at {job.enqueued_at}"

    return "No value for count provided"


if __name__ == "__main__":
    app.run()
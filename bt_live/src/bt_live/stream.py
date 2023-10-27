import json

from bt_live.ros_node import SingletonBtLiveNode

from django.http import StreamingHttpResponse


def response_generator(node):
    while True:
        data = node.spin_once()
        if data:
            print(data)
            yield json.dumps(data)
        yield '\n'


def msg(_):
    node = SingletonBtLiveNode()
    return StreamingHttpResponse(
        response_generator(node),
        content_type='text/event-stream')

import asyncio
import functools
import json

from bt_live.ros_node import SingletonBtLiveNode

from django.http import StreamingHttpResponse

# node = None
coroutine = None


# def get_node():
#     global node
#     if node is None:
        
#     return node


def get_coroutine(coroutine_function, *args, **kwargs):
    global coroutine
    if coroutine is None:
        coroutine = coroutine_function(*args, **kwargs)
    return coroutine


def stream(coroutine_function):
    @functools.wraps(coroutine_function)
    def wrapper(*args, **kwargs):
        coroutine = get_coroutine(coroutine_function, *args, **kwargs)
        try:
            while True:
                yield asyncio.run(coroutine.__anext__())
        except StopAsyncIteration:
            pass
        except ValueError:
            print('ValueError')
            pass
    return wrapper


@stream
async def chunks(node):
    while True:
        data = node.spin_once()
        if data:
            yield json.dumps(data)
        await asyncio.sleep(.01)


async def msg(request):
    node = SingletonBtLiveNode()
    return StreamingHttpResponse(chunks(node))

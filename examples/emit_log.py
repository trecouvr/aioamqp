#!/usr/bin/env python
"""
    Rabbitmq.com pub/sub example

    https://www.rabbitmq.com/tutorials/tutorial-three-python.html

"""

import asyncio
import aioamqp

import sys


@asyncio.coroutine
def exchange_routing():
    try:
        protocol = yield from aioamqp.connect('localhost', 5672)
    except aioamqp.AmqpClosedConnection:
        print("closed connections")
        return

    channel = yield from protocol.channel()
    exchange_name = 'logs'
    message = ' '.join(sys.argv[1:]) or "info: Hello World!"

    yield from channel.exchange(exchange_name, 'fanout')
    yield from asyncio.sleep(2)

    yield from channel.publish(message, exchange_name=exchange_name, routing_key='')
    print(" [x] Sent %r" % (message,))

    yield from asyncio.sleep(1)
    yield from asyncio.wait_for(protocol.client_close(), timeout=10)


asyncio.get_event_loop().run_until_complete(exchange_routing())

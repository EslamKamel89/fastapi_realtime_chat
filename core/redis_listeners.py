import asyncio

from redis.asyncio import Redis

from core.ws_registery import active_connections


async def chat_messages_redis_listener(redis: Redis):
    pubsub = redis.pubsub()
    await pubsub.subscribe("chat_messages")
    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = message["data"]

                for connections in active_connections.values():
                    for conn in connections:
                        await conn.send_text(data)
    except asyncio.CancelledError:
        raise
    finally:
        await pubsub.unsubscribe("chat_messages")
        await pubsub.close()

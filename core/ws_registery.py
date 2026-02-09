from fastapi import FastAPI, WebSocket, WebSocketDisconnect

active_connections: set[WebSocket] = set()


def register_ws(app: FastAPI) -> None:
    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        active_connections.add(websocket)
        try:
            while True:
                message = await websocket.receive_text()
                for conn in active_connections:
                    await conn.send_text(message)
        except WebSocketDisconnect as e:
            active_connections.remove(websocket)

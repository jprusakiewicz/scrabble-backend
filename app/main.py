import logging
from datetime import datetime, timedelta
from typing import Optional

import uvicorn
from fastapi import FastAPI, WebSocket
from starlette.responses import JSONResponse
from starlette.websockets import WebSocketDisconnect
from websockets.exceptions import ConnectionClosedOK

from app.connection_manager import ConnectionManager
from app.server_errors import GameIsStarted, PlayerIdAlreadyInUse, NoRoomWithThisId, RoomIdAlreadyInUse, ToManyPlayers

app = FastAPI()

manager = ConnectionManager()


@app.get("/")
async def get():
    return {"status": "ok"}


@app.get("/stats")
async def get_stats(room_id: Optional[str] = None):
    if room_id:
        try:
            return manager.get_room_stats(room_id)
        except NoRoomWithThisId:
            return JSONResponse(
                status_code=403,
                content={"detail": f"No room with this id: {room_id}"}
            )
    return manager.get_overall_stats()


@app.post("/room/new/{room_id}")
async def new_room(room_id: str):
    try:
        await manager.create_new_room(room_id)
        return JSONResponse(
            status_code=200,
            content={"detail": "success"}
        )
    except RoomIdAlreadyInUse:
        logging.info(f"Theres already a room with this id: {room_id}")
        return JSONResponse(
            status_code=403,
            content={"detail": "Theres already a room with this id: {room_id}"}
        )


@app.post("/room/new/{room_id}/{number_players}")
async def new_room(room_id: str, number_players: int):
    try:
        await manager.create_new_room(room_id, number_players)
        return JSONResponse(
            status_code=200,
            content={"detail": "success"}
        )
    except RoomIdAlreadyInUse:
        logging.info(f"Theres already a room with this id: {room_id}")
        return JSONResponse(
            status_code=403,
            content={"detail": "Theres already a room with this id: {room_id}"}
        )
    except ToManyPlayers:
        return JSONResponse(
            status_code=403,
            content={"detail": "Max number of players is 4!"}
        )


@app.delete("/room/{room_id}")
async def end_game(room_id: str):
    try:
        await manager.delete_room(room_id)
        return JSONResponse(
            status_code=200,
            content={"detail": "success"}
        )
    except NoRoomWithThisId:
        logging.info(f"Theres no room with this id: {room_id}")
        return JSONResponse(
            status_code=403,
            content={"detail": f"Theres no room with this id: {room_id}"}
        )


@app.post("/game/end/{room_id}")
async def end_game(room_id: str):
    await manager.end_game(room_id)
    return JSONResponse(
        status_code=200,
        content={"detail": "success"}
    )


@app.post("/game/end_all_games")
async def end_game():
    await manager.end_all_games()
    return JSONResponse(
        status_code=200,
        content={"detail": "success"}
    )


@app.post("/game/start/{room_id}")
async def start_game(room_id: str):
    await manager.start_game(room_id)
    return JSONResponse(
        status_code=200,
        content={"detail": "success"}
    )


@app.post("/game/restart/{room_id}")
async def restart_game(room_id: str):
    await manager.restart_game(room_id)
    return JSONResponse(
        status_code=200,
        content={"detail": "success"}
    )


@app.post("/game/kick_player/{room_id}/{player_id}")
async def kick_player(room_id: str, player_id: str):
    await manager.kick_player(room_id, player_id)
    return JSONResponse(
        status_code=200,
        content={"detail": "success"}
    )


@app.websocket("/ws/{room_id}/{client_id}/{nick}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, client_id: str, nick: str):
    try:
        await manager.connect(websocket, room_id, client_id, nick=nick)
        logging.info(f"new client connected with id: {client_id}")

        try:
            while True:
                message = await websocket.receive()
                logging.info(message)
                await manager.handle_ws_message(message, room_id, client_id)

        except RuntimeError as e:
            logging.info(e.__class__.__name__)
            logging.info(e)

        except Exception as e:
            logging.info(e)
            logging.info(e.__class__.__name__)
            logging.info("disconnected")
            await manager.disconnect(websocket)
            await manager.broadcast(room_id)

    except GameIsStarted:
        logging.info(f"Theres already game started")
        await websocket.close()

    except PlayerIdAlreadyInUse:
        logging.info(f"Theres already connection with this client id {client_id}")
        await websocket.close()

    except NoRoomWithThisId:
        logging.info(f"Theres no room with this id: {room_id}")
        await websocket.close()

    except ConnectionClosedOK:
        await manager.kick_player(room_id, client_id)
        logging.info(f"ConnectionClosedOK {client_id}")
        await manager.broadcast(room_id)

    except Exception as e:
        logging.info(e)
        logging.info("disconnected!")


@app.websocket("/test/{room_id}/{client_id}/{nick}")
async def websocket_endpoint(websocket: WebSocket):
    time = datetime.now() + timedelta(0, 25)
    json_to_send = dict(is_game_on=False)
    json_to_send = dict(is_game_on=True, nicks={"1": {'nick': "kuba", "has_turn": True, "score": 4},
                                                "2": {'nick': "Michał", "has_turn": False, "score": 22},
                                                "3": {'nick': "Maciek", "has_turn": False, "score": 2137},
                                                "4": {'nick': "Łukasz", "has_turn": False, "score": 5555}},
                        board=[{'x': 7, 'y': 5, 'letter': 'K'}, {'x': 7, 'y': 6, 'letter': 'L'},
                               {'x': 7, 'y': 7, 'letter': 'U'}, {'x': 7, 'y': 8, 'letter': 'S'},
                               {'x': 7, 'y': 9, 'letter': 'K'}, {'x': 7, 'y': 10, 'letter': 'A'}],
                        player_hand=['A', 'P', 'H', 'K', 'L', 'Q', 'P'], timestamp=time.isoformat(), whos_turn="1",
                        is_my_turn=True)
    try:
        while True:
            ws = websocket
            await ws.accept()

            await websocket.send_json(json_to_send)
            message = await websocket.receive()

    except WebSocketDisconnect:
        logging.info("disconnected")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, workers=1)

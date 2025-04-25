from flask_socketio import join_room, emit
from .socketio import socketio
from app import db
from app.models import Player, Room


@socketio.on("connect")
def handle_connect():
    print("✅ Client connected!")


@socketio.on("disconnect")
def handle_disconnect():
    print("❌ Client disconnected!")


@socketio.on("join_room")
def handle_join(data):
    room_number = data.get("room_number")
    name = data.get("name")
    role = data.get("role")

    if not room_number or not name or not role:
        emit("error", {"message": "room_number, name, and role are required"})
        return

    print(f"🔵 Join request: room={room_number}, name={name}, role={role}")

    room = Room.query.filter_by(room_number=str(room_number)).first()

    if not room:
        emit("error", {"message": f"Room {room_number} does not exist"})
        return

    existing_player = Player.query.filter_by(room_id=room.id, name=name).first()
    if not existing_player:
        new_player = Player(name=name, role=role, room_id=room.id)
        db.session.add(new_player)
        db.session.commit()

    join_room(room_number)
    print(f"📌 Client joined room {room_number}")

    players_in_room = Player.query.filter_by(room_id=room.id).all()

    emit(
        "room_update",
        {"players": [f"{player.name} ({player.role})" for player in players_in_room]},
        room=room_number,
    )


@socketio.on("player_move")
def handle_move(data):
    room_number = data.get("room_number")
    move = data.get("move")

    if not room_number or not move:
        emit("error", {"message": "room_number and move are required"})
        return

    emit("update", move, room=room_number)


@socketio.on("factor_update")
def handle_factor_update(data):
    room_number = data.get("roomNumber")
    key = data.get("key")
    score = data.get("score")
    reason = data.get("reason")

    if not room_number or key is None or score is None:
        emit("error", {"message": "Missing required factor_update fields"})
        return

    print(f"📊 Factor update in room {room_number}: {key} = {score}, reason: {reason}")

    emit(
        "factor_updated",
        {
            "key": key,
            "score": score,
            "reason": reason,
        },
        room=str(room_number),
    )


@socketio.on("player_submitted")
def handle_player_submitted(data):
    print(f"🔄 Received player_submitted event: {data}")

    room_number = data.get("room_id")
    if not room_number:
        emit("error", {"message": "Missing room_id in player_submitted event"})
        return

    try:
        room = Room.query.filter_by(room_number=str(room_number)).first()
        if not room:
            emit("error", {"message": f"Room {room_number} not found"})
            return

        players_in_room = Player.query.filter_by(room_id=room.id).all()

        emit(
            "room_update",
            {
                "players": [
                    f"{player.name} ({player.role})" for player in players_in_room
                ]
            },
            room=room_number,
        )

    except Exception as e:
        print(f"❌ Error processing player_submitted event: {e}")
        emit("error", {"message": "Failed to process player_submitted"})

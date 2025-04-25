from flask import Blueprint, request, jsonify
from app import db
from app.models import Room, Player
from sqlalchemy.exc import IntegrityError
from app.socketio import socketio

room_bp = Blueprint("room", __name__, url_prefix="/api/rooms")


@room_bp.route("/<room_number>", methods=["POST"])
def create_or_join_room(room_number):
    data = request.get_json()

    if "name" not in data or "role" not in data:
        return jsonify({"error": "Name and role are required"}), 400

    name = data["name"]
    role = data["role"]

    if role not in ["BusDev", "Risk"]:
        return jsonify({"error": "Role must be either 'BusDev' or 'Risk'"}), 400

    room = Room.query.filter_by(room_number=str(room_number)).first()

    try:
        if room:
            if len(room.players) >= 2:
                return jsonify({"error": "Room is full"}), 400

            if any(player.role == role for player in room.players):
                return (
                    jsonify(
                        {"error": f"The role '{role}' is already taken in this room."}
                    ),
                    400,
                )

            new_player = Player(name=name, role=role, room_id=room.id)
            db.session.add(new_player)
            db.session.commit()

            print(f"✅ Player {name} added to room {room_number}")

            socketio.emit(
                "room_update",
                {
                    "room_number": room_number,
                    "players": [
                        {"id": player.id, "name": player.name, "role": player.role}
                        for player in room.players
                    ],
                },
                room=room_number,
            )

            return (
                jsonify(
                    {
                        "message": "Joined the room successfully",
                        "room_number": room_number,
                        "players": [
                            {"id": player.id, "name": player.name, "role": player.role}
                            for player in room.players
                        ],
                    }
                ),
                200,
            )

        else:
            new_room = Room(room_number=room_number)
            db.session.add(new_room)
            db.session.commit()

            new_player = Player(name=name, role=role, room_id=new_room.id)
            db.session.add(new_player)
            db.session.commit()

            print(f"🏠 Room {room_number} created, player {name} joined")

            socketio.emit(
                "room_update",
                {
                    "room_number": room_number,
                    "players": [
                        {
                            "id": new_player.id,
                            "name": new_player.name,
                            "role": new_player.role,
                        }
                    ],
                },
                room=room_number,
            )

            return (
                jsonify(
                    {
                        "message": "Room created and player joined successfully",
                        "room_number": room_number,
                        "players": [
                            {
                                "id": new_player.id,
                                "name": new_player.name,
                                "role": new_player.role,
                            }
                        ],
                    }
                ),
                201,
            )

    except IntegrityError as e:
        db.session.rollback()
        return (
            jsonify(
                {"error": "A database integrity error occurred", "details": str(e)}
            ),
            500,
        )


@room_bp.route("/<room_number>", methods=["GET"])
def get_room(room_number):
    room = Room.query.filter_by(room_number=str(room_number)).first()

    if not room:
        print(f"⚠️ Room {room_number} not found!")
        return jsonify({"error": "Room not found"}), 404

    players_data = [
        {
            "id": player.id,
            "name": player.name,
            "role": player.role,
            "factors": {
                "brand": {
                    "score": player.brand_market_score,
                    "reason": player.brand_market_reason,
                    "status": player.brand_market_status,
                },
                "tech": {
                    "score": player.tech_infra_score,
                    "reason": player.tech_infra_reason,
                    "status": player.tech_infra_status,
                },
            },
        }
        for player in room.players
    ]

    return jsonify({"room_number": room.room_number, "players": players_data}), 200

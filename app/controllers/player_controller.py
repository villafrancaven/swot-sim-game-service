from flask import Blueprint, request, jsonify
from app import db
from app.models import Player
from app.socketio import socketio

player_bp = Blueprint("player", __name__, url_prefix="/api/players")


@player_bp.route("/<int:player_id>/responses", methods=["POST"])
def submit_responses(player_id):
    data = request.get_json()

    player = Player.query.get(player_id)
    if not player:
        return jsonify({"error": "Player not found"}), 404

    try:
        player.brand_market_score = data.get("brand_market_score")
        player.brand_market_reason = data.get("brand_market_reason")
        player.brand_market_status = data.get(
            "brand_market_status", player.brand_market_status
        )  # Update status

        player.tech_infra_score = data.get("tech_infra_score")
        player.tech_infra_reason = data.get("tech_infra_reason")
        player.tech_infra_status = data.get(
            "tech_infra_status", player.tech_infra_status
        )  # Update status

        db.session.commit()

        socketio.emit(
            "player_submitted",
            {
                "player_id": player.id,
                "room_id": player.room_id,
                "brand_market_score": player.brand_market_score,
                "brand_market_reason": player.brand_market_reason,
                "brand_market_status": player.brand_market_status,
                "tech_infra_score": player.tech_infra_score,
                "tech_infra_reason": player.tech_infra_reason,
                "tech_infra_status": player.tech_infra_status,
            },
            room=str(player.room.room_number),
        )

        print(f"✅ Player {player.name} EMIT?!")

        return jsonify({"message": "Responses saved successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "error": "Failed to save responses",
                    "details": str(e),
                }
            ),
            500,
        )

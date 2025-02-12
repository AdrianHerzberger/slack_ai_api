from flask import Blueprint, jsonify, request
from ..storage.channel_message_data_manager import ChannelMessageDataManager
from ..utils.pagination_offset import PaginationOffset
from ..models.channel_message_model import ChannelMessage
from ..configuartions.channel_message_serializer import ChannelMessageSerializer
from flask_jwt_extended import jwt_required, get_jwt_identity
import pprint

channel_message_routes = Blueprint("channel_message_routes", __name__)
channel_message_manager = ChannelMessageDataManager()


@channel_message_routes.route("/create_message_channel/<channel_id>", methods=["POST"])
async def create_message_channel(channel_id):
    data = request.get_json()
    sender_id = data.get("sender_id")
    content = data.get("content")
    
    if channel_id is None:
        raise Exception(f"Channel did not exist, can't proceed to create message")

    try:
        new_message = await channel_message_manager.create_message(channel_id, sender_id, content)

        if new_message:
            return jsonify({
                "message": "Message created successfully",
                "message_id": new_message.id
            }), 201
        else:
            return jsonify({"error": "Failed to create message"}), 404

    except Exception as e:
        print(f"Error creating message for channel: {e}")
        return jsonify({"error": "Server error"}), 500


@channel_message_routes.route("/delete_channel_message/<channel_message_id>", methods=["DELETE"])
@jwt_required()
async def delete_channel_message(channel_message_id):
    try:
        user_auth = get_jwt_identity()
        if not user_auth:
            return jsonify({"error": "User authentication not valid!"}), 401
        deleted_message = await channel_message_manager.delete_channel_message(channel_message_id)
        if deleted_message:
            return jsonify({"success": "Channel message deleted successfully"}), 200
        else:  
            return jsonify({"error": "Channel message not found"}), 404
    except Exception as e:
        print(f"Error deleting channel message data: {e}")
        return jsonify({"error": "Failed to delete channel message data"}), 500


@channel_message_routes.route("/update_channel_message/<channel_message_id>", methods=["PATCH"])
@jwt_required()
async def update_channel_message(channel_message_id):
    data = request.get_json()
    message_content_update = data.get("update_content")

    try:
        user_auth = get_jwt_identity()
        if not user_auth:
            return jsonify({"error": "User authentication not valid!"}), 401
        update_message = await channel_message_manager.update_channel_message(channel_message_id, message_content_update)
        if update_message:
            return jsonify({"success": "Channel message updated successfully"})
        else:
             return jsonify({"error": "Channel message not found"}), 404
    except Exception as e:
        print(f"Error updating channel message data: {e}")
        return jsonify({"error": "Failed to update channel message data"}), 500


@channel_message_routes.route("/get_channel_messages/<channel_id>/", methods=["GET"])
async def get_channel_messages(channel_id):
    try: 
        channel_messages = await channel_message_manager.get_channel_messages_by_id(channel_id)
        if not channel_messages:
            return jsonify({"error": "Channel messages not found"}), 404

        page_number = int(request.args.get("page_number", 2))
        page_size = int(request.args.get("page_size", 10))

        paginator = PaginationOffset(page_number=page_number, page_size=page_size)

        context = {}

        paginated_channel_response = paginator(ChannelMessage, channel_messages, ChannelMessageSerializer, context)

        if paginated_channel_response:
            return jsonify(paginated_channel_response), 200
    
        elif channel_messages:
            channel_message_list = []
            for message in channel_messages:
                channel_message_data = {
                    "message_id": message.id,
                    "channel_id": message.channel_id,
                    "sender_id": message.sender_id,
                    "content": message.content,
                    "message_time": message.timestamp
                }

                channel_message_list.append(channel_message_data)
            return jsonify(channel_message_list), 200
        else:
            return jsonify({"error": "Channel message data not found"}), 404
    except Exception as e:
        print(f"Error getting channel message data: {e}")
        return jsonify({"error": "Failed to get channel message data"}), 500        


@channel_message_routes.route("/get_all_channel_messages/", methods=["GET"])
async def get_all_channel_messages():
    try:
        channel_messages = await channel_message_manager.get_all_channel_messages()
        if not channel_messages:
            return jsonify({"error": "Channel messages not found"}), 404

        page_number = int(request.args.get("page_number", 2))
        page_size = int(request.args.get("page_size", 10))

        paginator = PaginationOffset(page_number=page_number, page_size=page_size)

        context = {}

        paginated_channel_messages_response = paginator(ChannelMessage, channel_messages, ChannelMessageSerializer, context)

        if paginated_channel_messages_response:
            return jsonify(paginated_channel_messages_response), 200
        elif channel_messages:
            channel_message_list = []
            for message in channel_messages:
                channel_message_data = {
                    "message_id": message.id,
                    "channel_id": message.channel_id,
                    "sender_id": message.sender_id,
                    "content": message.content,
                    "message_time": message.timestamp
                }
                channel_message_list.append(channel_message_data)
            return jsonify(channel_message_list), 200
        else:
            return jsonify({"error": "Channel message data not found"}), 404
    except Exception as e:
        print(f"Error getting channel message data: {e}")
        return jsonify({"error": "Failed to get channel message data"}), 500
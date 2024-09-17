# bot/chat_routes.py

from auth.models import Message, Product
from flask import Blueprint, request, render_template, jsonify
from flask_login import login_required, current_user
from scraper.scraper import scrape_all_sites
from recommender import (
    collaborative_filtering,
    format_recommendations,
)
from sqlalchemy.orm import joinedload
from extensions import db


chat_bp = Blueprint("chat_bp", __name__)


@chat_bp.route("/chat", methods=["POST", "GET"])
@login_required
def chat():
    if request.method == "GET":
        messages = Message.query.filter_by(sender_id=current_user.id).options(
            joinedload(Message.products)
        )
        return render_template("chat.html", messages=messages)
    data = request.get_json()
    user_message = data.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    message = Message(
        sender_id=current_user.id,
        text=user_message,
        response_text="Here's what I found. Recommended products that fit your search...",
    )
    db.session.add(message)
    db.session.commit()
    # Find and create product
    result = scrape_all_sites(user_message)
    for product in result:
        product_obj = Product(message_id=message.id, **product)
        db.session.add(product_obj)
    db.session.commit()
    return jsonify(
        {
            "message": {
                "text": message.text,
                "response_text": message.response_text,
                "created_at": str(message.created_at),
            },
            "products": result,
        }
    )


@chat_bp.route("/recommendations", methods=["GET"])
@login_required
def recommendations():
    # Provide collaborative filtering or content-based filtering recommendations
    recommended_products = collaborative_filtering(
        current_user.id
    )  # content_based_filtering
    formatted_recommendations = format_recommendations(recommended_products)

    return render_template(
        "recommendations.html", recommendations=formatted_recommendations
    )

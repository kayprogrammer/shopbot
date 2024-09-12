# recommender/recommender.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.sql import func
from auth.models import Message, User, Product
import numpy as np


# Collaborative Filtering
def collaborative_filtering(user_id):
    # Find other users with search history
    similar_users = User.query.join(Message).filter(Message.sender_id != user_id).all()

    # Collect products that similar users have interacted with
    recommended_products = []
    for user in similar_users:
        user_searches = Message.query.filter_by(sender_id=user.id).all()

        for search in user_searches:
            product_ids = search.results  # Ensure this is a list of product IDs
            if isinstance(product_ids, list):
                products = Product.query.filter(Product.id.in_(product_ids)).all()
                recommended_products.extend(products)

    # Filter duplicates and return top 5 unique products
    unique_products = list(
        {product.id: product for product in recommended_products}.values()
    )
    return unique_products[:5]


# Content-Based Filtering
def content_based_filtering(user_id):
    user_history = Message.query.filter_by(user_id=user_id).all()

    if not user_history:
        return []

    queries = [history.query for history in user_history]
    vectorizer = TfidfVectorizer(stop_words="english")
    all_products = Product.query.all()

    if not all_products:
        return []

    all_titles = [product.title for product in all_products]
    vectors = vectorizer.fit_transform(queries + all_titles)

    user_vector = vectors[: len(queries)]
    product_vectors = vectors[len(queries) :]
    similarity_scores = cosine_similarity(user_vector, product_vectors)
    avg_similarity_scores = np.mean(similarity_scores, axis=0)

    top_indices = avg_similarity_scores.argsort()[-5:][::-1]
    top_products = [all_products[i] for i in top_indices]

    return top_products


# Helper function to format recommendations
def format_recommendations(recommendations):
    if not recommendations:
        return "No recommendations available at this time."

    formatted_results = "Top Recommendations:\n"
    for product in recommendations:
        formatted_results += f"Product: {product.title}\nPrice: {product.price}\nRating: {product.rating}\nLink: {product.link}\n\n"

    return formatted_results

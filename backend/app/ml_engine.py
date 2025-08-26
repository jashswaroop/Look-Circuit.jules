
import pandas as pd
from .models import UserInteraction, WardrobeItem, User
from . import db
from sklearn.metrics.pairwise import cosine_similarity

def get_user_item_matrix():
    """
    Fetches user interaction data and creates a user-item matrix.

    Returns:
        DataFrame: A pandas DataFrame where rows are user IDs, columns are
                   wardrobe item IDs, and values are 1 if the user has saved
                   the item, 0 otherwise. Returns an empty DataFrame if no
                   interactions are found.
    """
    # Query the database for all 'save' interactions
    interactions = db.session.query(UserInteraction.user_id, UserInteraction.wardrobe_item_id)
    interactions = interactions.filter_by(interaction_type='save').all()

    if not interactions:
        return pd.DataFrame()

    # Create a DataFrame from the interactions
    df = pd.DataFrame(interactions, columns=['user_id', 'wardrobe_item_id'])

    # Add a 'rating' column, for now it's just 1 for a 'save'
    df['rating'] = 1

    # Create the user-item matrix using pivot_table
    user_item_matrix = df.pivot_table(
        index='user_id',
        columns='wardrobe_item_id',
        values='rating'
    ).fillna(0)

    return user_item_matrix

def get_item_based_recommendations(user_id, num_recs=5):
    """
    Generates item-based collaborative filtering recommendations for a user.
    """
    user_item_matrix = get_user_item_matrix()

    if user_item_matrix.empty or user_id not in user_item_matrix.index:
        return []

    # Calculate item-item similarity using cosine similarity
    # We transpose the matrix to calculate similarity between items (columns)
    item_similarity_df = pd.DataFrame(
        cosine_similarity(user_item_matrix.T),
        index=user_item_matrix.columns,
        columns=user_item_matrix.columns
    )

    # Get items the user has already saved
    saved_items = user_item_matrix.loc[user_id]
    saved_item_ids = saved_items[saved_items > 0].index.tolist()

    if not saved_item_ids:
        return []

    # Get the last item the user saved to find similar items
    # A more advanced approach would consider all saved items
    last_saved_item_id = saved_item_ids[-1]

    # Get similarity scores for the last saved item, sort them, and drop the item itself
    similar_scores = item_similarity_df[last_saved_item_id].sort_values(ascending=False)
    similar_scores = similar_scores.drop(last_saved_item_id)

    # Filter out items the user has already saved
    unsaved_similar_items = similar_scores[~similar_scores.index.isin(saved_item_ids)]

    # Get the top N recommendations
    top_items = unsaved_similar_items.head(num_recs).index.tolist()

    # Query the database to get the full WardrobeItem objects
    recommendations = WardrobeItem.query.filter(WardrobeItem.id.in_(top_items)).all()

    return recommendations

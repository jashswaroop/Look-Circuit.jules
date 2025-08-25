import json
import os

def load_recommendation_data():
    """Loads the recommendation data from the JSON file."""
    # Correct path assuming the script is run from the root of the `backend` directory
    # or the app context is configured correctly.
    filepath = os.path.join(os.path.dirname(__file__), 'recommendation_data.json')
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: recommendation_data.json not found at {filepath}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from recommendation_data.json")
        return {}

def generate_recommendations(user_profile):
    """
    Generates fashion recommendations based on a user's profile.

    Args:
        user_profile (dict): A dictionary containing user information,
                             including 'body_shape'.

    Returns:
        dict: A dictionary containing recommendations for the user.
    """
    data = load_recommendation_data()
    body_shape = user_profile.get('body_shape')

    if not data or 'body_shapes' not in data:
        return {"error": "Recommendation data is missing or corrupt."}

    if not body_shape or body_shape not in data['body_shapes']:
        return {"error": f"No recommendations available for body shape: {body_shape}. Please complete your profile."}

    recommendations = data['body_shapes'][body_shape]

    return recommendations

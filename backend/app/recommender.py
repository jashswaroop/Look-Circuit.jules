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

def generate_recommendations(user):
    """
    Generates fashion recommendations based on a user's full profile.

    Args:
        user (User): The user object containing all profile and style guide data.

    Returns:
        dict: A dictionary containing recommendations for the user.
    """
    data = load_recommendation_data()
    body_shape = user.body_shape

    if not data or 'body_shapes' not in data:
        return {"error": "Recommendation data is missing or corrupt."}

    if not body_shape or body_shape not in data['body_shapes']:
        return {"error": f"No recommendations available for body shape: '{body_shape}'. Please complete your profile."}

    base_recommendations = data['body_shapes'][body_shape]
    style_guide = json.loads(user.style_guide_data) if user.style_guide_data else {}

    # Create a deep copy to modify
    import copy
    final_recommendations = copy.deepcopy(base_recommendations)

    # --- Filter by Style & Risk Tolerance ---
    risk_tolerance = style_guide.get('fashion_risk_tolerance', 'moderate')

    allowed_styles = ['classic']
    if risk_tolerance == 'moderate':
        allowed_styles.append('trendy')
    elif risk_tolerance == 'adventurous':
        allowed_styles.extend(['trendy', 'adventurous'])

    for category, recs in final_recommendations.get('recommendations', {}).items():
        filtered_dos = []
        for item_data in recs.get('do', []):
            # Check if the item is a dict with style_tags
            if isinstance(item_data, dict):
                # If any of the item's tags are in the allowed styles, keep it
                if any(tag in allowed_styles for tag in item_data.get('style_tags', [])):
                    filtered_dos.append(item_data['item'])
            else: # It's an old-style string item, keep it by default
                filtered_dos.append(item_data)
        recs['do'] = filtered_dos

    # --- Enhance with Color Preferences ---
    preferred_colors = style_guide.get('preferred_colors', '').split(',')
    preferred_color = preferred_colors[0].strip() if preferred_colors else ""

    if preferred_color:
        for category, recs in final_recommendations.get('recommendations', {}).items():
            for i, item_text in enumerate(recs.get('do', [])):
                recs['do'][i] = f"{item_text} (consider in {preferred_color})"

    return final_recommendations

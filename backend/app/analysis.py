import cv2
import numpy as np

# --- Face Shape Detection Logic ---

def detect_face_shape(image_path):
    """Detect face shape using advanced facial analysis with multiple methods"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            print(f"Could not load image: {image_path}")
            return "Unknown"

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_data = detect_face_with_multiple_methods(img, gray)

        if face_data is None:
            print("No face detected in image")
            return "Unknown"

        x, y, w, h = face_data
        face_shape = classify_face_shape_from_geometry(w, h)
        return face_shape

    except Exception as e:
        print(f"Error in face shape detection: {e}")
        return "Unknown"

def detect_face_with_multiple_methods(img, gray):
    """Try multiple face detection methods for better accuracy"""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    detection_params = [
        {'scaleFactor': 1.1, 'minNeighbors': 5, 'minSize': (80, 80)},
        {'scaleFactor': 1.2, 'minNeighbors': 4, 'minSize': (60, 60)},
        {'scaleFactor': 1.3, 'minNeighbors': 3, 'minSize': (40, 40)},
    ]

    for params in detection_params:
        faces = face_cascade.detectMultiScale(gray, **params)
        if len(faces) > 0:
            return max(faces, key=lambda rect: rect[2] * rect[3]) # Return largest face

    return None

def classify_face_shape_from_geometry(w, h):
    """
    Simplified classification based on the width-to-height ratio of the face.
    This is a simplified version of the logic from the reference repo.
    A more complex implementation can be added later if needed.
    """
    if h == 0: return "Unknown"
    ratio = w / h

    if ratio > 0.95 and ratio < 1.05:
        return "Round"
    elif ratio > 1.05:
        return "Square"
    elif ratio < 0.85:
        return "Oval"
    else:
        return "Heart"

# --- Skin Tone Analysis Logic ---

def analyze_skin_tone(image_path):
    """Analyze skin tone from image"""
    try:
        img = cv2.imread(image_path)
        if img is None: return "Unknown"

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) == 0:
            return "Unknown"

        x, y, w, h = faces[0]
        # Select a smaller, central region of the face to avoid hair/shadows
        face_center_x, face_center_y = x + w // 2, y + h // 2
        roi_w, roi_h = w // 4, h // 4
        roi_x, roi_y = face_center_x - roi_w // 2, face_center_y - roi_h // 2

        face_roi = img_rgb[roi_y : roi_y + roi_h, roi_x : roi_x + roi_w]

        if face_roi.size == 0: return "Unknown"

        avg_color = np.mean(face_roi.reshape(-1, 3), axis=0)
        r, g, b = avg_color

        # Simple skin tone classification based on average RGB
        if r > 200 and g > 180 and b > 170:
            return "Fair"
        elif r > 160 and g > 120 and b > 100:
            return "Medium"
        elif r > 120 and g > 80 and b > 60:
            return "Olive"
        else:
            return "Deep"

    except Exception as e:
        print(f"Error in skin tone analysis: {e}")
        return "Unknown"

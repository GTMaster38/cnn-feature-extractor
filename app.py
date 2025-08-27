# CNN Feature Extractor - Production Flask App
# This app visualizes the core operations of a Convolutional Neural Network layer

import base64
import io
import numpy as np
from flask import Flask, render_template, request
from PIL import Image
from scipy import signal

# Initialize the Flask application
app = Flask(__name__)

# Production configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

# --- Define the Convolution Filters ---
# These filters demonstrate different feature detection capabilities
FILTERS = {
    "Identity": np.array([
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]),
    "Sharpen": np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ]),
    "Edge Detect": np.array([
        [0, 1, 0],
        [1, -4, 1],
        [0, 1, 0]
    ]),
    "Strong Edge Detect": np.array([
        [-1, -1, -1],
        [-1, 8, -1],
        [-1, -1, -1]
    ]),
    "Sobel Top": np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ]),
    "Box Blur": np.array([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]) / 9.0
}

# --- Helper Functions for Image Processing ---

def array_to_base64(arr):
    """Converts a NumPy array into a Base64 encoded image string."""
    try:
        # Normalize the array to be in the 0-255 range for image display
        if arr.max() > 0:
            arr = (arr - arr.min()) / (arr.max() - arr.min()) * 255
        img = Image.fromarray(arr.astype(np.uint8))
        
        # Save image to a memory buffer
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        
        # Encode buffer to Base64 and return as a string
        return base64.b64encode(buffer.getvalue()).decode("utf-8")
    except Exception as e:
        print(f"Error converting array to base64: {e}")
        return None

def base64_to_array(b64_string):
    """Converts a Base64 encoded image string back into a NumPy array."""
    try:
        img_data = base64.b64decode(b64_string)
        img = Image.open(io.BytesIO(img_data)).convert('L')  # Convert to grayscale
        return np.array(img)
    except Exception as e:
        print(f"Error converting base64 to array: {e}")
        return None

def max_pool_2x2(image_array):
    """Performs a 2x2 max pooling operation with a stride of 2."""
    try:
        # Get the dimensions of the input array
        rows, cols = image_array.shape
        
        # Prepare the output array, which will be half the size
        output_rows, output_cols = rows // 2, cols // 2
        pooled_array = np.zeros((output_rows, output_cols))

        # Iterate over the image in 2x2 blocks
        for r in range(output_rows):
            for c in range(output_cols):
                # Define the 2x2 window
                window = image_array[r*2:r*2+2, c*2:c*2+2]
                # Find the maximum value in the window and assign it to the output
                pooled_array[r, c] = np.max(window)
                
        return pooled_array
    except Exception as e:
        print(f"Error in max pooling: {e}")
        return None

# --- Flask Routes ---

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main route that handles all requests to the application.
    - GET: Renders the initial page
    - POST: Processes user actions (upload, convolve, relu, pool)
    """
    
    # Initialize variables to None
    original_b64 = None
    convolved_b64 = None
    relued_b64 = None
    pooled_b64 = None
    error_message = None
    
    try:
        # If the form was submitted (i.e., a button was clicked)
        if request.method == "POST":
            action = request.form.get("action")
            
            # --- Action: Upload or Convolve ---
            if action == "convolve":
                file = request.files.get("image_upload")
                # If a new file was uploaded, use it. Otherwise, use the hidden field.
                if file and file.filename != '':
                    # Validate file type
                    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                        error_message = "Please upload a valid image file (PNG, JPG, JPEG, GIF, BMP)"
                    else:
                        img = Image.open(file.stream).convert('L')  # Convert to grayscale
                        original_array = np.array(img)
                        original_b64 = array_to_base64(original_array)
                else:
                    original_b64 = request.form.get("original_b64")
                    if original_b64:
                        original_array = base64_to_array(original_b64)
                    else:
                        error_message = "Please upload an image first"

                if original_b64 and not error_message:
                    # Apply convolution
                    filter_name = request.form.get("filter_select")
                    selected_filter = FILTERS.get(filter_name, FILTERS["Identity"])
                    convolved_array = signal.convolve2d(original_array, selected_filter, mode='same', boundary='symm')
                    convolved_b64 = array_to_base64(convolved_array)

            # --- Action: Apply ReLU ---
            elif action == "relu":
                # Get the state of the previous steps from hidden form fields
                original_b64 = request.form.get("original_b64")
                convolved_b64 = request.form.get("convolved_b64")
                
                if convolved_b64:
                    # Apply ReLU to the convolved image
                    convolved_array = base64_to_array(convolved_b64)
                    if convolved_array is not None:
                        relued_array = np.maximum(0, convolved_array)  # ReLU operation
                        relued_b64 = array_to_base64(relued_array)
                    else:
                        error_message = "Error processing convolved image"
                else:
                    error_message = "Please apply convolution first"
                    
            # --- Action: Apply Max Pooling ---
            elif action == "pool":
                # Get the state of the previous steps from hidden form fields
                original_b64 = request.form.get("original_b64")
                convolved_b64 = request.form.get("convolved_b64")
                relued_b64 = request.form.get("relued_b64")
                
                if relued_b64:
                    # Apply Max Pooling to the ReLU'd image
                    relued_array = base64_to_array(relued_b64)
                    if relued_array is not None:
                        pooled_array = max_pool_2x2(relued_array)
                        if pooled_array is not None:
                            pooled_b64 = array_to_base64(pooled_array)
                        else:
                            error_message = "Error in max pooling operation"
                    else:
                        error_message = "Error processing ReLU image"
                else:
                    error_message = "Please apply ReLU first"

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(f"Error in index route: {e}")

    # Render the HTML page, passing in the image data for display
    return render_template("index.html", 
                           filters=FILTERS.keys(),
                           original_b64=original_b64,
                           convolved_b64=convolved_b64,
                           relued_b64=relued_b64,
                           pooled_b64=pooled_b64,
                           error_message=error_message)

@app.route("/health")
def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return {"status": "healthy", "service": "CNN Feature Extractor"}

# Error handlers
@app.errorhandler(413)
def too_large(e):
    return "File too large. Please upload an image smaller than 16MB.", 413

@app.errorhandler(500)
def internal_error(e):
    return "Internal server error. Please try again.", 500

if __name__ == "__main__":
    # For development
    app.run(debug=False, host='0.0.0.0', port=5000)
else:
    # For production (WSGI)
    pass

# This is the main Python file for your Flask application.
# It handles the web server, image processing, and communication with the HTML front-end.

import base64
import io
import numpy as np
from flask import Flask, render_template, request
from PIL import Image
from scipy import signal

# Initialize the Flask application
app = Flask(__name__)

# --- Define the Convolution Filters ---
# These are the same filters discussed in the MIT lecture slides.
# They are represented as NumPy arrays.
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
    # Normalize the array to be in the 0-255 range for image display
    if arr.max() > 0:
        arr = (arr - arr.min()) / (arr.max() - arr.min()) * 255
    img = Image.fromarray(arr.astype(np.uint8))
    
    # Save image to a memory buffer
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    
    # Encode buffer to Base64 and return as a string
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def base64_to_array(b64_string):
    """Converts a Base64 encoded image string back into a NumPy array."""
    img_data = base64.b64decode(b64_string)
    img = Image.open(io.BytesIO(img_data)).convert('L') # Convert to grayscale
    return np.array(img)

def max_pool_2x2(image_array):
    """Performs a 2x2 max pooling operation with a stride of 2."""
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

# --- Flask Routes ---

@app.route("/", methods=["GET", "POST"])
def index():
    """
    This function handles all requests to the main page.
    - GET: Renders the initial empty page.
    - POST: Processes the user's actions (upload, convolve, relu, pool).
    """
    
    # Initialize variables to None
    original_b64 = None
    convolved_b64 = None
    relued_b64 = None
    pooled_b64 = None
    
    # If the form was submitted (i.e., a button was clicked)
    if request.method == "POST":
        action = request.form.get("action")
        
        # --- Action: Upload or Convolve ---
        # This block runs if the user uploads a new image or applies a new filter
        if action == "convolve":
            file = request.files.get("image_upload")
            # If a new file was uploaded, use it. Otherwise, use the hidden field.
            if file and file.filename != '':
                img = Image.open(file.stream).convert('L') # Convert to grayscale
                original_array = np.array(img)
                original_b64 = array_to_base64(original_array)
            else:
                original_b64 = request.form.get("original_b64")
                original_array = base64_to_array(original_b64)

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
            
            # Apply ReLU to the convolved image
            convolved_array = base64_to_array(convolved_b64)
            relued_array = np.maximum(0, convolved_array) # ReLU operation
            relued_b64 = array_to_base64(relued_array)
            
        # --- Action: Apply Max Pooling ---
        elif action == "pool":
            # Get the state of the previous steps from hidden form fields
            original_b64 = request.form.get("original_b64")
            convolved_b64 = request.form.get("convolved_b64")
            relued_b64 = request.form.get("relued_b64")
            
            # Apply Max Pooling to the ReLU'd image
            relued_array = base64_to_array(relued_b64)
            pooled_array = max_pool_2x2(relued_array)
            pooled_b64 = array_to_base64(pooled_array)

    # Render the HTML page, passing in the image data for display
    return render_template("index.html", 
                           filters=FILTERS.keys(),
                           original_b64=original_b64,
                           convolved_b64=convolved_b64,
                           relued_b64=relued_b64,
                           pooled_b64=pooled_b64)

# This line allows you to run the app directly from the command line
if __name__ == "__main__":
    app.run(debug=True)
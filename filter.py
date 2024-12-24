import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# Function to apply skin smoothing
def skin_smoothing(frame):
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define skin color range
    lower_skin = np.array([0, 48, 80], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # Create a mask to isolate skin color
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Apply Gaussian blur to smooth skin
    blurred = cv2.GaussianBlur(frame, (15, 15), 0)

    # Combine original frame with blurred skin
    smoothed = cv2.bitwise_and(blurred, blurred, mask=mask)
    
    return smoothed

# Function to apply skin blurring
def skin_blurring(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to skin regions
    blurred_skin = cv2.GaussianBlur(frame, (15, 15), 0)

    return blurred_skin

# Function to apply skin reshaping
def skin_reshaping(frame):
    # Apply skin reshaping techniques (e.g., morphological operations)
    # Example: Dilate skin regions
    kernel = np.ones((5, 5), np.uint8)
    dilated_skin = cv2.dilate(frame, kernel, iterations=1)

    return dilated_skin

# Function to capture video from webcam and apply effects
def capture_video():
    cap = cv2.VideoCapture(0)
    
    # Create a Tkinter window
    root = tk.Tk()
    root.title("Skin Filter Application")
    
    # Create a label to display video feed
    label = tk.Label(root)
    label.pack()
    
    # Create buttons for selecting different effects
    def apply_smoothing():
        nonlocal current_effect
        current_effect = skin_smoothing
        
    def apply_blurring():
        nonlocal current_effect
        current_effect = skin_blurring
    
    def apply_reshaping():
        nonlocal current_effect
        current_effect = skin_reshaping
    
    smoothing_btn = tk.Button(root, text="Smoothing", command=apply_smoothing)
    smoothing_btn.pack(side="left")
    
    blurring_btn = tk.Button(root, text="Blurring", command=apply_blurring)
    blurring_btn.pack(side="left")
    
    reshaping_btn = tk.Button(root, text="Reshaping", command=apply_reshaping)
    reshaping_btn.pack(side="left")
    
    current_effect = skin_smoothing

    def update_frame():
        ret, frame = cap.read()
        if ret:
            # Apply selected effect
            processed_frame = current_effect(frame)
            
            # Convert frame to ImageTk format
            img = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            
            # Update label with the new frame
            label.imgtk = imgtk
            label.configure(image=imgtk)
        
        root.after(10, update_frame)

    # Start the frame update loop
    root.after(0, update_frame)
    
    # Run the Tkinter event loop
    root.mainloop()
    
    cap.release()
    cv2.destroyAllWindows()

# Call the function to start capturing video
capture_video()

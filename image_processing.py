import cv2
import numpy as np
import matplotlib.pyplot as plt

def display_image(image, title="Image"):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis("off")
    plt.show()

def extract_color_values(image, contours):
    # Convert the image to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Initialize a list to store color values for each segment
    segment_colors = []

    for i, contour in enumerate(contours):
        # Create a mask for the current contour
        mask = np.zeros_like(hsv)
        cv2.drawContours(mask, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
        
        # Apply the mask to the HSV image
        segment_hsv = cv2.bitwise_and(hsv, mask)

        # Calculate the average color value in the segment
        avg_color = cv2.mean(segment_hsv)

        # Append the average color to the list
        segment_colors.append(avg_color)

        # Display the segment with the average color value
        display_image(cv2.cvtColor(segment_hsv, cv2.COLOR_HSV2RGB), f"Segment {i + 1} - Color: {avg_color}")

    return segment_colors

def analyze_strip(image_path):
    # Read the original image
    original_image = cv2.imread(image_path)

    # Check if the image is loaded successfully
    if original_image is None:
        print(f"Error: Unable to load the image from {image_path}")
        return

    # Display the original image
    display_image(original_image, "Original Image")

    # Dilation, Expansion, etc. (as in your code)
    # ...

    # Find contours in the masked image
    contours, _ = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original image
    cv2.drawContours(original_image, contours, -1, (0, 255, 0), 2)
    display_image(original_image, "Contour Detection")

    # Extract color values from each segment
    segment_colors = extract_color_values(original_image, contours)

    # Print the color values for each segment
    for i, color in enumerate(segment_colors):
        print(f"Segment {i + 1} - Color: {color}")

# Replace 'your_image_path.jpg' with the path to your test strip image
# analyze_strip('/home/r2dc/watersense/paperstrip.jpg')

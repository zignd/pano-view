import cv2
import numpy as np

def concatenate_webcams(output_file):
    # Open the first webcam
    cap1 = cv2.VideoCapture(0)  # Device ID for the first webcam
    # Open the second webcam
    cap2 = cv2.VideoCapture(2)  # Device ID for the second webcam
    
    if not cap1.isOpened() or not cap2.isOpened():
        print("Failed to open one or both webcams")
        return

    # Get properties from the webcams
    width1 = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height1 = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width2 = int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
    height2 = int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps1 = cap1.get(cv2.CAP_PROP_FPS)
    fps2 = cap2.get(cv2.CAP_PROP_FPS)

    # Use the minimum height for both videos to keep a uniform size
    min_height = min(height1, height2)
    new_width1 = int(width1 * (min_height / height1))
    new_width2 = int(width2 * (min_height / height2))

    # Total width is the sum of adjusted widths plus separator width
    separator_width = 10  # Width of the red line separator
    total_width = new_width1 + new_width2 + separator_width

    # Set up the output video settings
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, min(fps1, fps2), (total_width, min_height))
    
    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 or not ret2:
            print("Error reading from one or both webcams")
            break
        
        # Resize frames to the new dimensions
        frame1 = cv2.resize(frame1, (new_width1, min_height)) if ret1 else np.zeros((min_height, new_width1, 3), dtype=np.uint8)
        frame2 = cv2.resize(frame2, (new_width2, min_height)) if ret2 else np.zeros((min_height, new_width2, 3), dtype=np.uint8)

        # Create a red line separator
        separator = np.zeros((min_height, separator_width, 3), dtype=np.uint8)
        separator[:] = (0, 0, 255)  # BGR for red color
        
        # Concatenate frames with the separator
        final_frame = cv2.hconcat([frame1, separator, frame2])

        # Write the combined frame to the output and display it
        out.write(final_frame)
        cv2.imshow("Webcam Feed", final_frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap1.release()
    cap2.release()
    out.release()
    cv2.destroyAllWindows()

# Output file path
output = 'live_concatenated_video.mp4'

# Concatenate live webcam feeds
concatenate_webcams(output)

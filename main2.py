import cv2

def concatenate_videos(video_file1, video_file2, output_file):
    # Open the first video
    cap1 = cv2.VideoCapture(video_file1)
    # Open the second video
    cap2 = cv2.VideoCapture(video_file2)
    
    # Check if the first video is opened successfully
    if not cap1.isOpened():
        print(f"Failed to open {video_file1}")
        return
    # Check if the second video is opened successfully
    if not cap2.isOpened():
        print(f"Failed to open {video_file2}")
        return
    
    # Get properties from the first video
    frame_width = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap1.get(cv2.CAP_PROP_FPS)
    
    # Define codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec used
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))
    
    # Function to process video capture
    def process_video(cap):
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Resize frame to match dimensions if necessary
            resized_frame = cv2.resize(frame, (frame_width, frame_height))
            out.write(resized_frame)
    
    # Process each video
    process_video(cap1)
    process_video(cap2)
    
    # Release resources
    cap1.release()
    cap2.release()
    out.release()
    cv2.destroyAllWindows()

# Specify file paths
video1 = 'video1.mp4'
video2 = 'video2.mp4'
output = 'concatenated_video.mp4'

# Concatenate videos
concatenate_videos(video1, video2, output)

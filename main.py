from moviepy.editor import VideoFileClip, concatenate_videoclips

# Load the video files
video1 = VideoFileClip("video1.mp4")
video2 = VideoFileClip("video2.mp4")

# Concatenate the video clips
final_clip = concatenate_videoclips([video1, video2])

# Write the result to a new file
final_clip.write_videofile("final_video.mp4", codec='libx264')
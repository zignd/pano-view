import numpy as np
import cv2
import os

# TODO: implement something to automatically find the best configuration
os.environ['KIVY_METRICS_DENSITY'] = '2'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
from kivy.clock import Clock

class CameraView(Image):
    def __init__(self, **kwargs):
        super(CameraView, self).__init__(**kwargs)
        
        front_camera_index = 0
        back_camera_index = 4
        output_file_path = 'output.avi'

        self.capture_front = cv2.VideoCapture(front_camera_index)
        if not self.capture_front.isOpened():
            raise Exception("Cannot open front camera")

        self.capture_back = cv2.VideoCapture(back_camera_index)
        if not self.capture_back.isOpened():
            raise Exception("Cannot open back camera")
        
        # Get properties from the webcams
        width1 = int(self.capture_front.get(cv2.CAP_PROP_FRAME_WIDTH))
        print('>>> width1', width1)
        height1 = int(self.capture_front.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print('>>> height1', height1)
        width2 = int(self.capture_back.get(cv2.CAP_PROP_FRAME_WIDTH))
        print('>>> width2', width2)
        height2 = int(self.capture_back.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print('>>> height2', height2)
        fps1 = self.capture_front.get(cv2.CAP_PROP_FPS)
        fps2 = self.capture_back.get(cv2.CAP_PROP_FPS)

        # Use the minimum height for both videos to keep a uniform size
        self.min_height = min(height1, height2)
        print('>>> min_height', self.min_height)
        self.new_width1 = int(width1 * (self.min_height / height1))
        print('>>> new_width1', self.new_width1)
        self.new_width2 = int(width2 * (self.min_height / height2))
        print('>>> new_width2', self.new_width2)

        # Total width is the sum of adjusted widths plus separator width
        self.separator_width = 10  # Width of the red line separator
        total_width = self.new_width1 + self.new_width2 + self.separator_width

        # Set up the output video settings
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(output_file_path, self.fourcc, min(fps1, fps2), (total_width, self.min_height))

        Clock.schedule_interval(self.update, 1.0 / 30)  # update at 30Hz

    def update(self, dt):
        ret1, frame1 = self.capture_front.read()
        ret2, frame2 = self.capture_back.read()

        if not ret1 or not ret2:
            raise Exception("Failed to read from one or both cameras")

        # Resize frames to the new dimensions
        frame1 = cv2.resize(frame1, (self.new_width1, self.min_height)) if ret1 else np.zeros((self.min_height, self.new_width1, 3), dtype=np.uint8)
        frame2 = cv2.resize(frame2, (self.new_width2, self.min_height)) if ret2 else np.zeros((self.min_height, self.new_width2, 3), dtype=np.uint8)

        # Create a red line separator
        separator = np.zeros((self.min_height, self.separator_width, 3), dtype=np.uint8)
        separator[:] = (0, 0, 255)  # BGR for red color
        
        # Concatenate frames with the separator
        final_frame = cv2.hconcat([frame1, separator, frame2])

        # Write the combined frame to the output and display it
        self.out.write(final_frame)

        # Convert it to texture
        buf = cv2.flip(final_frame, 0).tobytes()
        texture = Texture.create(size=(final_frame.shape[1], final_frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = texture

    def on_stop(self):
        # When everything done, release the capture and writer
        self.capture_back.release()
        self.out.release()

class PanoViewApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical')
        camera_view = CameraView()
        main_layout.add_widget(camera_view)

        bottom_buttons_layout = BoxLayout(orientation='horizontal')
        bottom_buttons_layout.add_widget(Button(text='Dashcam'))
        bottom_buttons_layout.add_widget(Button(text='Surround View'))
        bottom_buttons_layout.add_widget(Button(text='Rear View'))
        bottom_buttons_layout.add_widget(Button(text='Side Views'))
        main_layout.add_widget(bottom_buttons_layout)

        # layout = GridLayout(cols=2)
        # layout.add_widget(Button(text='Start Recording'))
        # layout.add_widget(Button(text='Stop Recording'))
        # layout.add_widget(Label(text='Hello, World!'))
        # layout.add_widget(CameraView())
        return main_layout

    def on_stop(self):
        pass

if __name__ == '__main__':
    PanoViewApp().run()
import cv2

def test_cameras():
    index = 2
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            arr.append(index)
            cap.release()
        index += 1
    return arr

available_cameras = test_cameras()
print("Available cameras:", available_cameras)

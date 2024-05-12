import cv2

def test_cameras():
    index = 0
    i = 0
    arr = []
    while True:
        i += 1
        if i > 10:
            break
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            index += 1
            continue
        else:
            arr.append(index)
            index += 1
            cap.release()
    return arr

available_cameras = test_cameras()
print("Available cameras:", available_cameras)

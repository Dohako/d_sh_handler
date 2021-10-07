import cv2

def take_photo(cam_number:int=0, name:str="/home/pi/unnamed.jpg") -> str:
    print('Trying take photo')
    cap = cv2.VideoCapture(cam_number)
    ret,frame = cap.read()
    # cv2.imshow('img1', frame)
    try:
        cv2.imwrite(name, frame)
    except cv2.error:
        raise KeyError("Presumably, no such camera on device")
    cv2.destroyAllWindows()
    cap.release()
    return name
import cv2

def take_photo(cam_number:int, name:str="/home/pi/unnamed.jpg") -> str:
    print('Trying take photo')
    cap = cv2.VideoCapture(cam_number)
    ret,frame = cap.read()
    # cv2.imshow('img1', frame)
    cv2.imwrite(name, frame)
    cv2.destroyAllWindows()
    cap.release()
    return name
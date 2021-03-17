import cv2
import numpy as np


class VideoHandler():
    def __init__(self,video_file_name_wout_avi, record_time=200, record_qty=1, camera=0):
        self.screen_size = (640,480)
        self.record_time = record_time
        self.record_qty = record_qty
        self.video_file_name = video_file_name_wout_avi
        self.camera = camera

    def run(self):
        for i in range(self.record_qty):
            cap = cv2.VideoCapture(0)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(f'{self.video_file_name}_{i}.avi',
                                  fourcc, 20.0, self.screen_size)

            while self.record_time > 0:
                self.record_time -= 1
                ret, frame = cap.read()
                # cv2.imshow('test',frame)
                # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                if ret is True:
                    # frame = cv2.flip(frame, 0)
                    out.write(frame)
            cv2.destroyAllWindows()
            out.release()
            cap.release()


if __name__ == '__main__':
    a = VideoHandler('test')
    a.run()


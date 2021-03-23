import cv2
import numpy as np
import loguru


class VideoHandler():
    def __init__(self,video_file_name_wout_avi, record_time=200, record_qty=1, camera=0):
        if os.name != 'nt':
            loguru.logger.add('/home/pi/d_sh_handler/log.log')
        else:
            loguru.logger.add('log.log')
        self.screen_size = (640,480)
        self.record_time = record_time
        self.record_qty = record_qty
        self.video_file_name = video_file_name_wout_avi
        self.camera = camera

    @loguru.logger.catch()
    def run(self):
        loguru.logger.info("Start")
        loguru.logger.info(f"cam={self.camera}, video_name={self.video_file_name}")
        for i in range(self.record_qty):
            cap = cv2.VideoCapture(self.camera)
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
        loguru.logger.info("Ended")


if __name__ == '__main__':
    a = VideoHandler('test')
    a.run()


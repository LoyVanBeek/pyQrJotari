#! /usr/bin/env python
import zbar
import cv2

# video_capture = cv2.VideoCapture(0)
#
# scanner = zbar.ImageScanner()
#
# while True:
#     try:
#         ret, img = video_capture.read()
#         gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
#         image = zbar.Image(gray.shape[1], gray.shape[0], 'Y800', gray.tobytes())
#
#         if scanner.scan(image):
#             print([symbol.data for symbol in image])
#             for symbol in image:  # type: zbar.Symbol
#                 # print symbol.location
#                 for start, end in zip(symbol.location, symbol.location[:-1]):
#                     cv2.line(img=img, pt1=start, pt2=end, color=(255, 255, 0), thickness=1, lineType=cv2.LINE_8)
#                     print start, end
#                 # cv2.line(img, symbol.location[:-1], symbol.location[0], color=(0, 255, 0))
#
#         cv2.imshow('image', img)
#         cv2.waitKey(10)
#     except KeyboardInterrupt:
#         break


class CvInterface(object):
    def __init__(self, device=0, data_callback=None, video_callback=None):
        self.callback = data_callback
        self.video_callback = video_callback
        self.scanner = zbar.ImageScanner()
        self.device = device
        self.video_capture = None

    def start(self):
        self.video_capture = cv2.VideoCapture(self.device)

    def force_stop(self):
        pass

    def wait_stop(self):
        pass

    def run(self):
        while True:
            try:
                ret, img = self.video_capture.read()
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                image = zbar.Image(gray.shape[1], gray.shape[0], 'Y800', gray.tobytes())

                if self.scanner.scan(image):
                    for symbol in image:  # type: zbar.Symbol
                        cv2.line(img=img, pt1=symbol.location[0], pt2=symbol.location[1], color=(0, 255, 0), thickness=3, lineType=cv2.LINE_8)
                        cv2.line(img=img, pt1=symbol.location[1], pt2=symbol.location[2], color=(0, 255, 0), thickness=3, lineType=cv2.LINE_8)
                        cv2.line(img=img, pt1=symbol.location[2], pt2=symbol.location[3], color=(0, 255, 0), thickness=3, lineType=cv2.LINE_8)
                        cv2.line(img=img, pt1=symbol.location[3], pt2=symbol.location[0], color=(0, 255, 0), thickness=3, lineType=cv2.LINE_8)

                        code = symbol.data.replace("http://www.scoutingboxtel.nl/qr.asp?groep=", "")
                        if self.callback:
                            try:
                                self.callback(code)
                            except Exception as e:
                                print e
                        break

                self.video_callback(img)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except Exception, e:
                print "Trying to read did not work: ", e
                self.wait_stop()
                break


def dummy_callback(data):
    print "CB: ", data.capitalize()

def video_callback(image):
    cv2.imshow('image', image)
    cv2.waitKey(10)

def main():
    zbar = CvInterface(data_callback=dummy_callback, video_callback=video_callback)
    zbar.start()

    '''
    while True:
        try:
            pass
        except KeyboardInterrupt:
            break
    zbar.stop()
    '''
    zbar.run()
    zbar.wait_stop()


if __name__ == "__main__":
    main()

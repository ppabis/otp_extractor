from qreader import QReader
import cv2

def read_qr(file):
    qreader = QReader()
    image = cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2RGB)
    decoded_urls = qreader.detect_and_decode(image=image)
    return decoded_urls
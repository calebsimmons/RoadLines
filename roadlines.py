import numpy as np
from PIL import ImageGrab
import cv2
import time

from directkeys import PressKey, W, A, S, D

def roi(img, vertices):
    # create a blank mask
    mask = np.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, vertices, 255)
    # only show area that is in the mask
    masked = cv2.bitwise_and(img, mask)
    return masked

def draw_lines(img, lines):
    for line in lines:
        coords = line[0]
        cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)    

def process_img(image):
    original_image = image
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    processed_img = cv2.GaussianBlur(processed_img, (5,5), 0)
    
    vertices = np.array([[10,500],[10,300],[300,200],[500,200],[800,300],[800,500],
                         ], np.int32)    
    #processed_img = roi(processed_img, [vertices])

    # more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html      
    lines = cv2.HoughLinesP(
        processed_img, # edges      
        1,             # rho 
        np.pi/180,     # theta
        180,           # max length
        np.array([]),
        50,           # min length 
        5              # gap 
    )
    
    try:
        draw_lines(processed_img, lines)
    except TypeError:
        pass         

    return processed_img

def main():

    # Countdown to get ready
    for i in list(range(4)[::-1]):
        print(i+1)
        time.sleep(1)

    print("press 'q' to quit")    

    while(True):
        # 800x600 windowed mode
        screen =  np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))
        #print('loop took {} seconds'.format(time.time()-last_time))
        #last_time = time.time()
        new_screen = process_img(screen)
        cv2.imshow('window', new_screen)
        #cv2.imshow('window2',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    main()

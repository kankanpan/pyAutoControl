import pyautogui
import cv2
import numpy as np
import base64
import io

def findTarget(img_path):
    init_point = pyautogui.locateOnScreen( './img/' + img_path)
    print(init_point)
    location = [init_point[0] + 20, init_point[1] + 100]

    return location

def findTargetCv(img_path, init_scale=1, good_match_rate=0.3, min_match=10):
    ss = pilToCv(pyautogui.screenshot())
    image = cv2.imread( './img/' + img_path)
    if init_scale != 1:
        image = cv2.resize(image, dsize=None, fx=init_scale , fy=init_scale)

    #if image.shape[0] < 300 or image.shape[1] < 300:
    #    image = cv2.resize(image, dsize=None, fx=2, fy=2)

    # result = cv2.matchTemplate(ss, image, cv2.TM_CCORR_NORMED)
    # minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)

    # Judg = judgeMatching(maxVal)
    # print(Judg)

    type = cv2.AKAZE_create()
    kp_01, des_01 = type.detectAndCompute(ss, None)
    kp_02, des_02 = type.detectAndCompute(image, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.match(des_01, des_02)
    matches = sorted(matches, key = lambda x:x.distance)
    good = matches[:int(len(matches) * good_match_rate)]

    if len(good) < min_match:
        return False

    src_pts = np.float32([kp_02[g.trainIdx].pt for g in good[:2]])
    dst_pts = np.float32([kp_01[g.queryIdx].pt for g in good[:2]])

    s = (dst_pts[0][0] - dst_pts[1][0])/(src_pts[0][0] - src_pts[1][0]) *init_scale
    x = dst_pts[0][0] - src_pts[0][0] *s
    y = dst_pts[0][1] - src_pts[0][1] *s

    print(x,y,s)

    #mutch_image_src = cv2.drawMatches(ss, kp_01, image, kp_02, good[:4], None, flags=2)

    #cv2.imshow('image', mutch_image_src)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return [x, y, s]

def judgeColor(location):
    ss = pilToCv(pyautogui.screenshot( region=(location[0]-4, location[1]-4, 8, 8 )))
    imgBoxHsv = cv2.cvtColor(ss,cv2.COLOR_BGR2HSV)
    v = imgBoxHsv.T[2].flatten().mean()
    print("Value: %.2f" % (v))
    return v < 160

def judgeMatching(num):
    if 0.99 < num:
        return True
    else:
        return False

def pilToCv(image):
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:
        pass
    elif new_image.shape[2] == 3:
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image

def findBlackRect(rect, s=0.5):
    ss = pilToCv(pyautogui.screenshot(region=(rect[0], rect[1], rect[2]-rect[0], rect[3]-rect[1])))
    # image = cv2.imread( './img/' + img_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.cvtColor(ss, cv2.COLOR_RGB2GRAY)
    (thresh, im_bw) = cv2.threshold(image,4,255,cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(im_bw,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 200000*s and area < 1000000*s:
            x,y,w,h = cv2.boundingRect(cnt)
            # image = cv2.rectangle(image,(x,y),(x+w,y+h),(120,120,120),4)

    # cv2.imshow('image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return [x,y,x+w,y+h]

def SS(h=0, w=0, x=0, y=0):
    if h and w and x and y:
        return pilToCv(pyautogui.screenshot(region=(x, y, w, h)))
    else:
        return pilToCv(pyautogui.screenshot())

def NdarrayToBase64(dst):
    result, dst_data = cv2.imencode('.jpg', dst)
    dst_base64 = base64.b64encode(dst_data)
    return dst_base64

def findDef(ss1, check = False):
    ss2 = pilToCv(pyautogui.screenshot())
    ss1 = cv2.cvtColor(ss1, cv2.COLOR_RGB2GRAY)
    ss2 = cv2.cvtColor(ss2, cv2.COLOR_RGB2GRAY)
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
    fgmask = fgbg.apply(ss1)
    fgmask = fgbg.apply(ss2)
    contours, hierarchy = cv2.findContours(fgmask ,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 10000:
            x,y,w,h = cv2.boundingRect(cnt)
            print("area", area)
            image = cv2.rectangle(ss2,(x,y),(x+w,y+h),(120,120,120),4)

    if check == 1:
        cv2.imshow('image', ss2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return [x,y,x+w,y+h]

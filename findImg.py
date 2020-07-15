import pyautogui
import cv2
import numpy as np

def findTarget(img_path):
    init_point = pyautogui.locateOnScreen( './img/' + img_path)
    print(init_point)
    location = [init_point[0] + 20, init_point[1] + 100]

    return location

def findTargetCv(img_path, good_match_rate=0.30, min_match=10):
    ss = pilToCv(pyautogui.screenshot())
    image = cv2.imread( './img/' + img_path)

    #image = cv2.resize(image, dsize=None, fx=2, fx=2)

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

    src_pts = np.float32([kp_02[m.trainIdx].pt for m in good])
    dst_pts = np.float32([kp_01[m.queryIdx].pt for m in good])
    Mx, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC)

    mutch_image_src = cv2.drawMatches(ss, kp_01, image, kp_02, matches[:10], None, flags=2)

    height = mutch_image_src.shape[0]
    width = mutch_image_src.shape[1]
    top_left = (int(Mx[0][2] +0.5), int(Mx[1][2] +0.5)); #tx,ty
    bottom_right = (top_left[0] + width, top_left[1] + height)

    cv2.rectangle(mutch_image_src,top_left, bottom_right, (255, 0, 0), 10)
    cv2.imshow('image', mutch_image_src)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return  Mx, np.int32(mask)


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
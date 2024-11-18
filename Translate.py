# 透视变换

import cv2 
import cv2.typing as cvT
import numpy as np
from Base import MyControl

def preProcess(img: cvT.MatLike, Name: str = "preProcessImg")-> cvT.MatLike:
    """对图像进行预处
        1. 转化为灰度图
        2. 二值化 分界为125
        3. 高斯模糊
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,thres = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY)
    MyControl.showImg(thres, "Thres"+'_'+Name)
    blur = cv2.GaussianBlur(thres, (5, 5), 0)
    MyControl.showImg(blur, "Blur"+'_'+Name)
    return blur

def findContourExternal(img: cvT.MatLike, Name: str = "findContoursImg")-> cvT.MatLike:
    """
        找到图像的轮廓
        img: preProcess后的图像
        Name: 图像名称
        return: cvT.MatLike 轮廓
    """
    canny = cv2.Canny(img, 30, 150)
    MyControl.showImg(canny, "Canny"+'_'+Name)
    contour, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if MyControl.debug:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(img, contour, -1, (0, 255, 0), 3)
        MyControl.showImg(img, "Contours"+'_'+Name)
    return contour



def getTranslatePoints(img: cvT.MatLike, contour, Name: str = "getTranslatePoints"):
    """
        获取透视变换的四个点
        img: 图像
        contour: 轮廓
        Name: 图像名称

        return: pts1, pts2
        pts1: 原图的四个点
        pts2: 变换后的四个点
    """
    epsilon = 0.1 * cv2.arcLength(contour[0], True)
    approx:cvT.MatLike = cv2.approxPolyDP(contour[0], epsilon, True)

    if len(approx) != 4:
        raise ValueError("Can not find the rectangle")

    if MyControl.debug:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(img, [approx], -1, (0, 255, 0), 3)
        MyControl.showImg(img, "Approx"+'_'+Name)
    
    approx = approx.reshape(4, 2)

    pts1 = np.float32(approx)
    pts2 = np.zeros((4, 2), np.float32)
    s = pts1.sum(axis=1)
    tl = pts1[np.argmin(s)]
    br = pts1[np.argmax(s)]
    diff = np.diff(pts1, axis=1)
    tr = pts1[np.argmin(diff)]
    bl = pts1[np.argmax(diff)]
    width = max(int(np.sqrt(((br[0] - bl[0]) ** 2 + (br[1] - bl[1]) ** 2))),\
                int(np.sqrt(((tr[0] - tl[0]) ** 2 + (tr[1] - tl[1]) ** 2))))
    height = max(int(np.sqrt(((tr[0] - br[0]) ** 2 + (tr[1] - br[1]) ** 2))),\
                int(np.sqrt(((tl[0] - bl[0]) ** 2 + (tl[1] - bl[1]) ** 2))))
    pts2[0] = [0, 0]
    pts2[1] = [0, height - 1]
    pts2[2] = [width - 1, height - 1]
    pts2[3] = [width-1, 0]
    
    return pts1, pts2

def translate(img:cvT.MatLike, Name="Translate")-> cvT.MatLike:
    """
        透视变换
        img : 图像
        Name: 图像名称
        return: dst
        
    """

    imgs = cv2.resize(img, (MyControl.BaseSize[0]//2, MyControl.BaseSize[1]//2))

    preImg = preProcess(imgs, Name)
    contours = findContourExternal(preImg, Name)
    pts1,pts2 = getTranslatePoints(preImg, contours, Name)
    pts1 = np.float32(pts1)
    pts1 *= 2
    pts2 = np.float32(pts2)
    pts2 *= 2
    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(img, M, (int(pts2[2][0]), int(pts2[2][1])))
    MyControl.showImg(dst, "dst"+'_'+Name)
    return dst

if __name__ == "__main__":
    img = MyControl.readImg("./test.jpg")
    translate(img)
    MyControl.waitKey()
'''
    step1: pre

    该文件是处理学生条形码的,支持两种模式:
    1. 通过pyzbar库识别条形码 解码出来学号
    2. 通过pyteseract库识别条形码, 获取学号
'''

from Base import MyControl
import cv2
import cv2.typing as cvT

def getStudentNumber(img:cvT.MatLike,Name:str="StudentNumber"):
    """
        通过pyzbar库识别条形码 解码出来学号
    """
    data = ""
    if MyControl.Config.StudentNumberParseMode == "pyzbar":
        from pyzbar import pyzbar
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        barcodes = pyzbar.decode(gray)
        for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")
            data += barcodeData
    elif MyControl.Config.StudentNumberParseMode == "pyteseract":
        import pytesseract as ocr
        import re
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        data = ocr.image_to_string(gray)
        data = re.findall(r"\d{10}",data)
        if len(data) == 0:
            return None
        data = data[0]
    return data
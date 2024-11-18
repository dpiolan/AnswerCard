from DebugBase import ImgControl
import Config as conf
import cv2
import cv2.typing as cvT
import json

class MyControl:
    Config = conf
    debug = conf.Debug
    useJSON = conf.UseJSONTemplate
    Template:dict = None
    ShowWidth = 700
    BaseSize = conf.BaseSize

    

    @classmethod
    def showImg(cls,img: cvT.MatLike, title: str = "Image"):
        if cls.debug:
            img = cv2.resize(img, (cls.ShowWidth, int(cls.ShowWidth * img.shape[0] / img.shape[1])))
            cv2.imshow(title,img)
        else:
            pass
    @classmethod
    def showImgWithControl(cls,img: cvT.MatLike, title: str = "Image",parse:bool = True)->None:
        if cls.debug:
            ic = ImgControl(img,title)
            ic.wait()
            if not cls.useJSON:
                if parse:
                    cls.Template = ic.parse(cls.Config.Template)
        else:
            pass
    @classmethod
    def waitKey(cls):
        if cls.debug:
            cv2.waitKey(0)
        else:
            pass
    @classmethod
    def destroyAllWindows(cls):
        if cls.debug:
            cv2.destroyAllWindows()
        else:
            pass

    @classmethod
    def readImg(cls,path:str)-> cvT.MatLike:
        """
            path: 图片路径
            return: 图片 已经resize为BaseSize
        """
        img = cv2.imread(path)
        img = cv2.resize(img, cls.BaseSize)
        return img

    @classmethod
    def readJSON(cls,path:str)->dict:
        """
            读取JSON文件
            path: JSON文件路径 decode("utf-8")
        """
        with open(path, "r", encoding="utf-8") as f:
            return json.loads(f.read())

    @classmethod
    def getTemplate(cls)->dict:
        if cls.Template is None:
            if cls.useJSON:
                cls.Template = cls.readJSON(cls.Config.JSONPath)
            else:
                return None
        return cls.Template
    
    @classmethod
    def writeImg(cls,img:cvT.MatLike,path:str):
        cv2.imwrite(path,img)

    @classmethod
    def writeJSON(cls,data:dict,path:str):
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(data,ensure_ascii=False,indent=4))
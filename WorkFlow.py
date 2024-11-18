
"""
step1:
    - translate -> imgTrans

step2:
    - UseJSON?
        - Y:
            - readJSON -> tem
        - N:
            - Debug? 
                -Y: 
                    - showImgWithControl -> tem
                    - parse
                -N: 
                    - readDemoJSON -> tem
    -> tem

step3:
    - GetStudentNumber()...

step4:
    - clip -> preSelect[[[...]]...]

step5:
    - GetQuestions(Tem) -> Questions{"Name": == , "Select": [[[x1,y1],[x2,y2],[x3,y3],[x4,y4]]],...}

step6:
    - GetAnswers(Questions, preSelect) 

"""
from Base import MyControl
import cv2
import cv2.typing as cvT
import numpy as np
from Translate import translate
from StuNumParse import getStudentNumber
import Questions

class BigQuestion:
    def __init__(self,imgs:list[cvT.MatLike],name:str,workFlow):
        self.imgs = imgs
        self.name = name
        self.workFlow = workFlow
        



class WorkFlow:
    def __init__(self,img:cvT.MatLike,name:str="test") -> None:
        self.img = translate(img,name)
        self.img = cv2.resize(self.img, MyControl.Config.BaseSize)
        self.name = name
        self.Template:dict = None
        self.__initTemplate()
        self.clips = self.clip()
        self.studentNum = self.GetStudentNumber()
        self.answers = self.GetAnswers()

    def __initTemplate(self):
        if MyControl.useJSON:
            self.Template = MyControl.getTemplate()
        else:
            if self.Template is None:
                if MyControl.debug:
                    MyControl.showImgWithControl(self.img, self.name,True)
                    self.Template = MyControl.getTemplate()
                else:
                    raise ValueError("Can not get the template")
                
    def clip(self):
        ret = {}
        for(Name,Select) in self.Template.items():
            ret[Name] = []
            for i in Select:
                x1,y1 = i[0]
                x2,y2 = i[1]
                im = self.img[int(y1):int(y2),int(x1):int(x2)]
                ret[Name].append(im)
                MyControl.showImg(im,Name+"_Clip")
        return ret
    
    def GetAnswers(self):
        answers = []
        for name,imgs in self.clips.items():
            if "Question" in name:
                for img in imgs:
                    answers.extend(Questions.MakeClipQuestionsAndGetAnswers(img,name))

        return answers

    def GetStudentNumber(self):
        return getStudentNumber(self.clips["BarCode"][0],self.name)
        
    def writeToExcel(self):
        pass




if __name__ == "__main__":
    img = MyControl.readImg("test-cp.jpg")
    wf = WorkFlow(img)
    MyControl.writeJSON(wf.Template,"test.json")
    for(Name,Select) in wf.clips.items():
        for i in range(len(Select)):
            MyControl.writeImg(Select[i],Name+f"_{i}.jpg")
    wf.GetStudentNumber()
    print(wf.answers)
    print(wf.studentNum)
        
    

    
    
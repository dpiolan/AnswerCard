'''
    这个文件用于存放问题的类和识别, 具体为获取各个题目的选项位置和答案位置
'''
import cv2
import cv2.typing as cvT
from Base import MyControl
import numpy as np

if MyControl.debug:
    from matplotlib import pyplot as plt

def preProcess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _,im = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return im

def MakeGradeX(img:cvT.MatLike,pre=True):
    # width = 200
    if pre:
        img = preProcess(img)
    mat:cvT.MatLike = cv2.resize(img,(200,int(img.shape[0]/img.shape[1]*200)))
    mat_ = cv2.bitwise_and(mat,1)
    
    ret = np.ndarray(mat_.shape[1],dtype=np.int16)
    for i in range(mat_.shape[1]):
        ret[i] = np.sum(mat_[:,i])
    s = np.max(ret)
    ret = s - ret
    struc = np.array([1,2,4,2,1])
    ret = np.convolve(ret,struc,mode="same")
    return ret


def MakeGradeY(img:cvT.MatLike,pre=True):
    #height = 200
    if pre: img = preProcess(img)
    mat:cvT.MatLike = cv2.resize(img,(int(img.shape[1]/img.shape[0]*200),200))
    
    MyControl.showImg(mat,"GradeY")
    
    mat_ = cv2.bitwise_and(mat,1)
    
    ret = np.ndarray(mat_.shape[0],dtype=np.int16)
    for i in range(mat_.shape[0]):
        ret[i] = np.sum(mat_[i,:])
    s = np.max(ret)
    ret = s - ret
    return ret


def MakeGradeD1(tup:np.ndarray):
    ret = np.ndarray(tup.shape[0]-1,dtype=np.int16)
    for i in range(tup.shape[0]-1):
        ret[i] = tup[i+1] - tup[i]
    return ret

def MakeAreaWithZero(tup:np.ndarray):
    ret = np.zeros(len(tup))
    points = [] 
    s = 0
    e = 0
    lock = False
    for i in range(len(tup)):
        if tup[i] != 0 and not lock:
            s = i
            lock = True
        if tup[i] == 0 and lock:
            e = i
            lock = False
            k = int(np.sum(tup[s:e]))
            ret[s:e] = np.array([k]*(e-s))
            temp = (s,e,k)
            points.append(temp)
    return ret,points



def MakeSelectsAndAnswer(img:cvT.MatLike,name:str="Question")->tuple[list,int]:
    im = preProcess(img)
    for i in range(5):
        im = cv2.erode(im,np.ones((5,5),np.uint8))
        im = cv2.dilate(im,np.ones((5,5),np.uint8))
    MyControl.showImg(im,name)
    MyControl.waitKey()
    s = MakeGradeX(im,False)
    s = np.where(s>np.average(s)*0.3,s,0)
    
    struc = np.array([ 1,2,4,2,1])
    s = np.convolve(s,struc,mode="same")
    # plt.plot(s)
    # plt.show()
    k,p = MakeAreaWithZero(s)
    # plt.plot(k)
    # plt.show()
    ret = []
    for x1,x2,area in p:
        if area>100:
            x1 = int(x1/200*img.shape[1])
            x2 = int(x2/200*img.shape[1])
            ret.append((x1,x2,area))
    print(ret)
    areas = [i[2] for i in ret if i[2]>100]
    areas = np.array(areas)
    k = np.where(areas==np.max(areas))[0][0]
    if len(areas) != 5:
        if k==0:
            k = 1
        else:
            a = np.where(s==np.max(s))[0][0]
            preConf = np.array(MyControl.Config.PreSupposePos)
            preConf = preConf/MyControl.Config.BaseSize[0]*200
            for i in range(len(preConf)):
                if preConf[i][0]<a<preConf[i][1]:
                    k = i+1
                    break
                else:
                    k = 0
    print(name+":\t",k)
    return ret,k

def MakeClipQuestionsAndGetAnswers(img:cvT.MatLike,name:str="MakeClipQuestions")->list[tuple[list,int]]:
    img = cv2.resize(img,MyControl.BaseSize)
    # img = preProcess(img)
    for i in range(3):
        img = cv2.erode(img,np.ones((5,5),np.uint8))
        img = cv2.dilate(img,np.ones((5,5),np.uint8))
    MyControl.showImg(img,name)
    ptm = MakeGradeY(img)
    struc = np.array([1,2,8,2,1])
    ptm = np.convolve(ptm,struc,mode="same")
    k = np.average(ptm)
    ptm = np.where(ptm>k,1,0)
    ptm = MakeGradeD1(ptm)
    plt.plot(ptm)
    plt.show()
    
    a = np.array( np.where(ptm==1),dtype=np.float32)
    b = np.array( np.where(ptm==-1),dtype=np.float32)
    a = a/200 * img.shape[0]
    b = b/200 * img.shape[0]

    ret = []
    for k in range(a.shape[1]):
        ret.append(MakeSelectsAndAnswer(img[int(a[0,k]):int(b[0,k])],name+"_"+str(k)))

    return ret


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    s = []
    MakeClipQuestionsAndGetAnswers(MyControl.readImg("Question_2_1.jpg"))

# 该文件为主要的透视变换

import cv2

import cv2.typing as cvT

import matplotlib.pyplot as plt
import Config

class ImgControl:
    #该类是用于调试的, 进行图像的显示和保存与交互
    def __init__(self,img: cvT.MatLike, title: str = "Image"):
        self.img = img
        self.title = title
        self.fig = plt.figure(title)
        self.chick = False

        # 选取的区域
        self.start = [0,0]
        self.end = [0,0]

        self.ax = self.fig.add_subplot(111)
        self.ax.imshow(self.img)
        self.ax.set_title(title)

        self.savePoints = []

        self.cid_zoom = self.fig.canvas.mpl_connect('button_press_event', self.on_zoom)
        self.cid_release = self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_key = self.fig.canvas.mpl_connect('key_press_event', self.on_key)

    def on_zoom(self, event):
        if event.inaxes != self.ax:
            return
        # 获取放大镜放大的坐标
        self.start = [event.xdata, event.ydata]

    def on_release(self, event):
        if event.inaxes != self.ax:
            return
        # 获取放大镜放大的坐标
        self.end = [event.xdata, event.ydata]
        print(f"Zoom end coordinates: {self.end}")

    def on_key(self, event):
        if event.key == "enter":
            self.savePoints.append([self.start, self.end])
            print(f"Save points: {self.savePoints[-1]}")
        elif event.key == "backspace":
            print(f"Pop points: {self.savePoints[-1]}")
            self.savePoints.pop()

        elif event.key == "q":
            plt.close()

    def parse(self,template:list[dict])->dict:
        ret = {}
        for i in template:
            ret[i["Name"]] = []

            for k in range(i["count"]):
                ret[i["Name"]].append(self.savePoints.pop(0))
        return ret

    def wait(self):
        plt.show()
        

if __name__ == "__main__":
    img = cv2.imread("test.jpg")
    imgControl = ImgControl(img, "Test")
    imgControl.wait()
    pas = imgControl.parse(Config.Template)
    print(pas)
import cv2
import matplotlib.pyplot as plt
import numpy as np

# recognizerRed = cv2.face.LBPHFaceRecognizer_create()
# recognizerRed.read('CascadeClassifierModel/Red_Chess.yml')  # 导入红色棋子yml文件，是经过色阶调整后的
# recognizerBlack = cv2.face.LBPHFaceRecognizer_create()
# recognizerBlack.read('CascadeClassifierModel/Black_Chess.yml')  # 导入黑色棋子yml文件
font = cv2.FONT_HERSHEY_SIMPLEX  # 显示的字体类型

chess = ('No', 'jian', 'Che', 'ma', 'xia', 'shi', 'pao', 'zu', 'suai', 'che', 'ma', 'xia', 'shi', 'pao', 'bin',
         'Uk')  # 用于标记的文本

chessID = []
chess_x = []
chess_y = []

lower_red = np.array([156, 43, 46])  # 红色阈值下界
higher_red = np.array([180, 255, 255])  # 红色阈值上界

# 获取摄像头要指定名字如0是电脑默认摄像头，1USB的摄像头，如果获取视频指定文件路径即可
vc = cv2.VideoCapture(2)
# 设定分辨率720*1280
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


chessBoardXY = (410, 110)  # 棋盘方格左上角坐标，(x,y)，→为x正方向，↓为y正方向
chessBoardWH = (880, 620)  # 棋盘方格宽和高，(width,height)
sampleNum = 0
imgID = None
imgID_s = None
key = False
key2 = False


def cv_show(name, img):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def color_detection(rimg):
    area = 0
    # 传入图片
    img_hsv = cv2.cvtColor(rimg, cv2.COLOR_BGR2HSV)
    # 找出红色部分
    mask_red = cv2.inRange(img_hsv, lower_red, higher_red)  # 可以认为是过滤出红色部分，获得红色的掩膜
    # mask_red = cv2.medianBlur(mask_red, 7)  # 中值滤波
    # cv_show('mask_red', mask_red)
    # 二值化，阈值分割
    ret3, th3 = cv2.threshold(mask_red, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # 二值化 0 = black ; 1 = white
    # 算出面积
    height, width = th3.shape
    # cv_show('th3', th3)
    for i in range(height):
        for j in range(width):
            if th3[i, j] == 255:
                area += 1
    # 返回结果1为红色棋子，0为黑色棋子
    if area >= 40:
        return 1
    else:
        return 0


def x_abscissa(xs):
    xq = 10
    if 418 < xs < 468:
        xq = 0
    elif 468 < xs < 518:
        xq = 1
    elif 518 < xs < 568:
        xq = 2
    elif 568 < xs < 618:
        xq = 3
    elif 618 < xs < 669:
        xq = 4
    elif 669 < xs < 719:
        xq = 5
    elif 719 < xs < 769:
        xq = 6
    elif 769 < xs < 819:
        xq = 7
    elif 819 < xs < 870:
        xq = 8
    return xq


def y_ordinate(ys):
    yq = 10
    if 118 < ys < 167:
        yq = 0
    elif 167 < ys < 216:
        yq = 1
    elif 216 < ys < 266:
        yq = 2
    elif 266 < ys < 315:
        yq = 3
    elif 315 < ys < 365:
        yq = 4
    elif 365 < ys < 414:
        yq = 5
    elif 414 < ys < 464:
        yq = 6
    elif 464 < ys < 513:
        yq = 7
    elif 513 < ys < 563:
        yq = 8
    elif 563 < ys < 612:
        yq = 9
    return yq


if vc.isOpened():
    # 返回两值，open布尔值，frame
    open_video, frame = vc.read()
else:
    open_video = False


# while open_video:
def open_video_xq():
    global key, sampleNum, key2, imgID_s
    ret, img = vc.read(0)
    # if img is None:
    #     break
    if ret:
        # 取每一帧图片
        imgSource = cv2.cvtColor(img, 1)  # 读入一幅彩色图片
        # cv_show('imgSource', imgSource)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转为灰度图
        # cv_show('gray', gray)

        fil = cv2.medianBlur(gray, 3)  # 中值滤波
        imgEqualizeHist = cv2.equalizeHist(fil)  # 直方图均衡化

        # 每次先清空数据
        chessID = []
        chess_x = []
        chess_y = []

        # 输入图像，方法（类型），dp(dp=1时表示霍夫空间与输入图像空间的大小一致，dp=2时霍夫空间是输入图像空间的一半，以此类推)，
        # 最短距离-可以分辨是两个圆否 则认为是同心圆 ,边缘检测时使用Canny算子的高阈值，
        # 中心点累加器阈值—候选圆心（霍夫空间内累加和大于该阈值的点就对应于圆心），检测到圆的最小半径，检测到圆的的最大半径
        circles = cv2.HoughCircles(fil, cv2.HOUGH_GRADIENT, 1, 32, param1=300, param2=20, minRadius=10, maxRadius=22)
        i = 0
        if not circles is None:  # 检测到了圆circles不为空
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     key = True
            #     key2 = False
            for circle in circles[0]:  # 遍历每一个圆
                x, y, r = int(circle[0]), int(circle[1]), 22  # 标记圆的半径为16
                # 靠近边缘的棋子忽略，如果超出xy的范围跳出这个循环
                if x < chessBoardXY[0] or y < chessBoardXY[1] or x > chessBoardWH[0] or y > chessBoardWH[1]:
                    continue
                if key:
                    key2 = 1
                    sampleNum = sampleNum + 1
                    r = 15  # 矩形截取半径

                    # 截图出颜色判断图片区域
                    img_path = imgSource[y - r:y + r, x - r:x + r]
                    # 通过颜色识别函数识别出颜色，color_final返回识别出的颜色，1为红色，0为黑色
                    color_final = color_detection(img_path)

                    if color_final:  # 如果为红色
                        cv2.circle(imgSource, (x, y), 4, (0, 255, 0), -1)  # 红色棋子用黄点标记

                        imgID = 'r'

                        # imgID, conf = recognizerRed.predict(gray[y - r:y + r, x - r:x + r])  # 对检测到的棋子灰度图进行分类
                        # if conf < 190:  # 与样本中的数据置信度较高
                        #     imgID_s = chess[imgID]
                        # else:  # 置信度较低，标记为未知
                        #     imgID_s = "Uk"
                        # img = cv2.putText(imgSource, imgID_s, (x, y), font, 0.6, (255, 0, 0), 2)  # 标记棋子ID
                        # # print("坐标x = ",x)
                        # # print('坐标y = ',y)
                        # # cv_show("1", gray[y - r:y + r, x - r:x + r])
                    else:  # 黑色
                        cv2.circle(imgSource, (x, y), 4, (255, 255, 255), -1)  # 黑色棋子用白点标记

                        imgID = 'b'

                        # imgID, conf = recognizerBlack.predict(gray[y - r:y + r, x - r:x + r])  # 对检测到的棋子灰度图进行分类
                        # if conf < 190:  # 与样本中的数据置信度较高
                        #     imgID_s = chess[imgID]
                        # else:  # 置信度较低，标记为未知
                        #     imgID_s = "Uk"
                        # img = cv2.putText(imgSource, imgID_s, (x, y), font, 0.6, (0, 255, 255), 2)  # 标记棋子ID
                        # print("坐标x = ", x)
                        # print('坐标y = ', y)
                        # cv_show("2", gray[y - r:y + r, x - r:x + r])
                    # 将识别ID号存入数组
                    chessID.insert(i, imgID)
                    # 等于chessID[i] = imgID
                    # print('chessID', chessID)
                    # 把像素坐标转换象棋坐标
                    chess_x.insert(i, x_abscissa(x))
                    chess_y.insert(i, y_ordinate(y))
                    # chess_x[i] = x_ordinate(x)
                    # chess_y[i] = y_abscissa(y)
                    # print('chess_x', chess_x)
                    # print('chess_y', chess_y)

                    i += 1

                    '''
                    r = 15  # 矩形截取半径
                    # 获取训练图片程序
                    # k = 20
                    # img2 = gray[y - k:y + k, x - k:x + k]
                    # cv_show('img2', img2)
                    # cv2.imwrite(f'{str(sampleNum)}.jpg', img2)
    
                    # if key:
                    key2 = True
                    imgID, conf = recognizerRed.predict(gray[y - r:y + r, x - r:x + r])  # 对检测到的棋子灰度图进行分类
    
                    if conf < 190:  # 与样本中的数据置信度较高
                        imgID = chess[imgID]
                    else:  # 置信度较低，标记为未知
                        imgID = "Uk"
                    cv2.circle(img, (x, y), r, (0, 255, 0), 2)  # 标记检测到的棋子位置
                    img = cv2.putText(imgSource, imgID, (x, y), font, 0.6, (255, 0, 0), 2)  # 标记棋子ID
                    '''
                # 标记棋子ID
                # img = cv2.putText(imgSource, imgID_s, (x, y), font, 0.6, (255, 0, 0), 2)
                # 标记检测到的棋子位置
                cv2.circle(img, (x, y), r, (0, 255, 0), 2)

        # 打印识别的象棋数据
        # if key:
            # # global x5
            # # x5 = [1, 2]
            # print('x5-opencv', x5)
            # print('chessID', chessID)
            # print('chess_x', chess_x)
            # print('chess_y', chess_y)
        if key2:
            key = False
        cv2.rectangle(img, chessBoardXY, chessBoardWH, (255, 255, 0), 1, 4)  # 标记棋盘方格最外圈轮廓

        # 标定棋盘起始点和终点-1为点，2为圆
        cv2.circle(img, (443, 140), 6, (255, 255, 255), -1)  # 左上角白点标记
        cv2.circle(img, (845, 590), 6, (255, 255, 255), -1)  # 右下角用白点标记
        cv2.circle(img, (845, 140), 6, (255, 255, 255), -1)  # 左下角用白点标记
        cv2.circle(img, (443, 590), 6, (255, 255, 255), -1)  # 右上角用白点标记

        cv2.circle(img, (640, 360), 8, (255, 255, 255), -1)  # 中间用白点标记
        # cv2.namedWindow('my_phone', 0)
        cv2.imshow('my_phone', img)  # 窗口显示图片

        # 每帧处理速度10毫秒，键盘27（Esc键的ascall码）退出循环
        # if cv2.waitKey(10) & 0xFF == ord('q'):
        # if cv2.waitKey(20) & 0xFF == 27:
        #     break

        return chessID, chess_x, chess_y

# 关闭窗口
# vc.release()
# cv2.destroyAllWindows()

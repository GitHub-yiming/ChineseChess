1	运行环境说明

PLC

系统主控采用Siemens S7-1200 PLC，编程软件使用TIA Portal V16。

下载链接：https://mp.weixin.qq.com/s/9gr99aC8PfP83RTgo1FtTg

触摸屏

触摸屏采用昆仑通态(MCGS)TPC7062Ti型号，编程软件使用MCGS嵌入版7.7。

下载链接：http://wxmcgs.net/ruanjianxiazai/103.html

视觉

IDE采用Visual Studio Code，语言采用Python 3.11.6，视觉识别采用OpenCV开源库，与PLC通讯采用snap7库，象棋界面动画采用Pygame库。

下载链接：

1.Visual Studio Code：https://code.visualstudio.com/

2.Python：https://www.python.org/downloads/release/python-3116/

3.Snap7：pip install snap7

4.Pygame：pip install pygame

Snap7和Pygame要在cmd中输入pip指令安装。

 
2	系统运行前准备

PLC

1.PLC上电，确保PLC、触摸屏和电脑在同一局域网内即可。

2.PLC IP地址：192.168.0.1

触摸屏

1.触摸屏上电，确保PLC和触摸屏在同一局域网内。

2.触摸屏IP：192.168.0.13

视觉

1.先确保PLC和触摸屏已经上电，且与电脑在同一局域网下。

2.将相机连接至电脑，使用Vision\VideoCap.exe软件测试，在左上角点击【装置】选择视觉相机，出现实时画面即选择正确。

3.打开Visual Studio Code，到OpenCV.py文件中第22行，修改cv2.VideoCapture参数，一般0是电脑默认摄像头，1是视觉相机。

vc = cv2.VideoCapture(1)

4.运行ChineseChessVision.py文件，如果视频画面不正确，请回到OpenCV.py文件中修改cv2.VideoCapture()参数。视觉程序正常的启动时间会比较久，因电脑而异，笔者电脑的启动时间为1分钟左右。

5.将棋盘放入视觉画面中的方框内，并将方框内的4个白点对准象棋的四个角落，也就是4个车的位置。如果没有对准，就进行视觉检测，可能会出现视觉程序闪退的情况。

 
3	系统运行操作

视觉运行

1.点击【开始游戏】，让画面出现棋子。

工作位置标记

1.在触摸屏上点击【轴启用】，设置【Abs速度】与【点动速度】。

Abs参考速度：70mm/s，点动参考速度：50mm/s。

2.点击【方向键】来移动吸盘，将吸盘移动至机械原点，点击【设原点】按钮。这里需要注意在设置原点前，先将吸盘沿着XY轴点动运行一次，确保在XY轴上没有障碍物，否则后续执行命令时可能出现撞机！

3.点击【方向键】来移动吸盘，将吸盘移动至XY轴的极限位置，点击【Mark】按钮(mach_lim_x,mach_lim_y)，标记极限位置。

4. 点击【方向键】来移动吸盘，将吸盘移动至象棋原点，即左下角【车】的位置，按下【Mark】按钮(aPborg_x0,aPborg_y0)，标记象棋原点。

3.1.1	位置修正

功能说明：当棋盘的摆放位置出现了一定的旋转角度，也就是没有与机械坐标的XY轴垂直，那么由于在程序中默认棋盘坐标XY是与机械坐标XY完全垂直的，去计算位置时则会与实际位置不符。本功能则具有能测算出棋盘坐标相对于机械坐标旋转的角度，那么在计算位置时会加上旋转的角度，达到位置修正的目的。

注意：此功能需要对点定位的精度要求较高，由于吸盘直径为18mm，是一个圆形，定位时会有较大偏差。此功能在测试时，使用的是一支中性笔，由于笔尖足够细，定位精度较好，计算出来的位置与实际位置重合度较高。因此在使用吸盘定位时，此功能不保证位置精度。

1.点击【方向键】来移动吸盘，将吸盘沿着象棋原点的X轴移动一段距离(移动距离没有具体要求，定位精准即可)，按下【Mark】按钮(x1,y1)标记位置。

2.按下【Calcθ】按钮计算旋转角度，即后续的位置计算都会加上这个角度。

象棋界面操作

1.点击【AI】按钮，启动AI模式。

2.点击一个【棋子】，按下【Get】按钮吸取棋子。

3.操作【方向键】移动棋子，再次点击【棋子】，按下【Set】按钮下放棋子。

4.按下【OK】按钮，吸盘回原点后，启动视觉相机拍照。

5.等待视觉识别，待【AI】计算完位置后，会自动执行。

提示：在手动吃子时，需要先点击对方【棋子】，按下【Eliminate】按钮，将对方棋子移动到吃子位置。在由【AI】吃子时则自动完成此流程。

远程代码库：

1.Github：https://github.com/GitHub-yiming/ChineseChess

2.Gitee：https://gitee.com/hu-yiming123/ChineseChess

有问题可以创建Issues提问，后续如果更新会在上面提交最新代码。

注意：Github没有使用VPN的情况下可能出现无法访问，国内建议访问Gitee。

运行视频：

合集：https://www.bilibili.com/video/BV1NN4y1B7Dx/?spm_id_from=333.999.0.0&vd_source=8ab5c6efde6709df2c141423e2eb0c77

操作视频：https://www.bilibili.com/video/BV1ze41167f6/?spm_id_from=333.999.0.0&vd_source=8ab5c6efde6709df2c141423e2eb0c77


参考链接：

OpenCV：https://github.com/STM32xxx/OpenCV-Cascade-Classifier

Chess：https://github.com/58c/Chinese-chess


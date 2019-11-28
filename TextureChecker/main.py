import sys
from PyQt5.QtGui import QStandardItem, QStandardItemModel 
from PyQt5.QtWidgets import QAction, QApplication, QComboBox, QFileDialog, QLabel, QLineEdit, QTableView, QMainWindow
import os
from PIL import Image

import warnings
warnings.filterwarnings("ignore")

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        # 关键字段声明
        self.__printModel = "ONLY"
        self.__filterModel = "JPGE"
        self.__totalNumber = 0
        self.__errNumber = 0
        # 初始化标签，窗体设置
        self.FormInit()
        pass

    def FormInit(self):
        self.WindowInit()  # 窗体
        self.BarInit()  # 菜单、工具
        self.LabelInit() # label
        self.TextBoxInit()
        self.BtnInit()
        self.ComboxInit()
        self.TableViewInit()
        pass

    # 主窗体设置
    def WindowInit(self):
        self.setWindowTitle("贴图属性检查")
        self.setWindowOpacity(1)
        self.resize(800, 600)
        pass

    # label设置
    def LabelInit(self):
        lbDirSelect = QLabel("文件目录:", self)
        lbDirSelect.resize(60, 20)
        lbDirSelect.move(10, 35)
        lbModePrint = QLabel("输出模式:", self)
        lbModePrint.resize(60, 20)
        lbModePrint.move(10, 70)
        lbModeFilter = QLabel("过滤模式:", self)
        lbModeFilter.resize(60, 20)
        lbModeFilter.move(10, 105)
        lbResultTotalCheck = QLabel("校验总数:", self)
        lbResultTotalCheck.resize(60, 20)
        lbResultTotalCheck.move(10, 520)
        lbResultErrorCheck = QLabel("错误总数:", self)
        lbResultErrorCheck.resize(60, 20)
        lbResultErrorCheck.move(10, 550)
        pass

    def ComboxInit(self):
        # 模式选择下拉列表
        osCom = QComboBox(self)
        osCom.move(70, 70)
        osCom.resize(60, 20)
        osCom.addItem("ONLY")
        osCom.addItem("WHOLE")
        osCom.activated[str].connect(self.OnTriAct_SwitchPrintMode)

        ftCom = QComboBox(self)
        ftCom.move(70, 105)
        ftCom.resize(60, 20)
        ftCom.addItem("WHOLE")
        ftCom.addItem("JPGE")
        ftCom.addItem("PNG")
        ftCom.activated[str].connect(self.OnTriAct_SwitchFilterMode)
        pass

    def TextBoxInit(self):
        self.__textBoxDir = QLineEdit(self)
        self.__textBoxDir.move(70, 35)
        self.__textBoxDir.resize(400, 20)

        self.__textBoxTotal = QLineEdit(self)
        self.__textBoxTotal.resize(50, 20)
        self.__textBoxTotal.move(70, 520)

        self.__textBoxErr = QLineEdit(self)
        self.__textBoxErr.resize(50, 20)
        self.__textBoxErr.move(70, 550)
        pass

    def TableViewInit(self):
        self.__model = QStandardItemModel(0, 0)
        self.__headers = ["名称", "格式", "次幂", "大小", "路径"]
        self.__model.setHorizontalHeaderLabels(self.__headers)
        tbView = QTableView(self)
        tbView.setGeometry(200, 100, 500, 400)
        # 最后一列拉伸
        tbView.horizontalHeader().setStretchLastSection(True)
        tbView.setModel(self.__model)
        pass

    def TableViewClear(self):
        self.__model.clear()
        self.__model.setHorizontalHeaderLabels(self.__headers)
        pass

    # 按钮创建
    def BtnInit(self):
        # btnDirSelect = QPushButton("OPEN", self)
        # btnDirSelect.resize(60, 22)
        # btnDirSelect.move(67, 15)
        # btnDirSelect.clicked.connect(lambda:self.FolderSelect())
        pass

    def BarInit(self):
        # 状态栏
        self.statusBar()
        # 菜单栏
        self.menubar = self.menuBar()#获取窗体的菜单栏

        # 文件操作菜单
        self.file = self.menubar.addMenu("文件")
        # 文件操作子菜单创建
        fileOperate = self.file.addMenu("打开")
        # 文件夹选择子菜单
        actOpenDirs = QAction('文件夹', self)
        actOpenDirs.setStatusTip('选择并且打开文件夹')
        actOpenDirs.triggered.connect(self.FolderSelect)
        fileOperate.addAction(actOpenDirs)
        # 文件选择子菜单
        actOpenFile = QAction('文件', self)
        actOpenFile.setStatusTip('选择并且打开单个文件')
        actOpenFile.triggered.connect(self.FileSelect)
        fileOperate.addAction(actOpenFile)
        # 多文件选择子菜单
        actOpenMutiFile = QAction('文件多个', self)
        actOpenMutiFile.setStatusTip('选择并且打开多个文件')
        fileOperate.addAction(actOpenMutiFile)
        pass
        
    # 文件夹选择
    def FolderSelect(self):
        fileDirs = QFileDialog.getExistingDirectory(self, "文件夹选取", "C:/")
        self.__textBoxDir.setText(fileDirs) # 设置选择路径
        self.TableViewClear()
        # 计数器，针对多级子目录文件
        counter = 0 
        for root, dirs, files in os.walk(fileDirs):
            # 循环处理文件夹下的文件
            for raw in range(len(files)):
                # 列数显示对应的结果
                root.replace('\\', '/')  # 字符替换，os遍历路径会出现反斜杠，要做替换
                counter = self.ResultPrint(root, files[raw], counter)
        self.ResultInfoSet()
        pass

    # 单文件选择
    def FileSelect(self):
        filePath, ok = QFileDialog.getOpenFileName(self,"单文件选取","C:/","Images(*.jpg *.png)")
        if ok:
            self.__totalNumber += 1
            self.TableViewClear()
            strArray = filePath.strip('/').split('/')
            root = "" 
            for i in range(len(strArray)):
                if i < len(strArray) - 2:
                    root +=  strArray[i] + '/'
                elif i < len(strArray) - 1:
                    root += strArray[i]

            self.__textBoxDir.setText(root) # 设置选择路径
            self.ResultPrint(root, strArray[len(strArray) - 1], 0)
            self.ResultInfoSet()
        pass
    
    # 多文件选择
    def FileMutiSelect(self):
        filesPath, ok = QFileDialog.getOpenFileNames(self, "多文件选取", "C:/", "Images(*.jpg *.png)")
        if ok:
            print(filesPath)
        pass

    # 解析的图片信息，路径，次幂，名称
    def ResultPrint(self, dir, name, counter):
        # 这里需要做一步处理，排除非img格式
        strArray = name.split('.')
        if(strArray[1] != "jpg" and strArray[1] != 'png'):
            return counter
        # 模式过滤
        if(self.__filterModel == "JPGE" and strArray[1] != "jpg"):
            return counter
        if(self.__filterModel == "PNG" and strArray[1] != "png"):
            return counter
        self.__totalNumber += 1
        # 继续执行 img open
        img = Image.open(dir + "/" + name)
        # 首先检测宽高比例
        right = True if (img.size[0] == img.size[1]) else False
        # 检测是否2次幂
        if right:
            right = True if ((img.size[0] & (img.size[0] - 1)) == 0) else False
            self.__errNumber = self.__errNumber if right else self.__errNumber + 1
        else:
            self.__errNumber += 1 
        # 根据选择模式输出，若是判断结果正确，则不需要输出全部，也就是只输出格式不正确的
        if(self.__printModel == "ONLY" and right):
            return counter
        # info设定
        for col in range(5):
            it = QStandardItem() # 生成容器
            if col == 0:
                it.setText(str(strArray[0]))
            elif col == 1:
                it.setText(str('.' + strArray[1]))
            elif col == 2:
                it.setText(str(right))
            elif col == 3:
                it.setText(str(img.size))
            elif col == 4:
                it.setText(str(dir))
            
            self.__model.setItem(counter, col, it)

        return counter + 1
        pass

    # 数目信息统计输出
    def ResultInfoSet(self):
        self.__textBoxTotal.setText(str(self.__totalNumber))
        self.__textBoxErr.setText(str(self.__errNumber))
        self.__totalNumber = 0
        self.__errNumber = 0
        pass

    '''
    下面是与触发器相关的东西
    '''
    # 输出模式信号切换
    def OnTriAct_SwitchPrintMode(self, text):
        self.__printModel = str(text)
        pass

    def OnTriAct_SwitchFilterMode(self, text):
        self.__filterModel = str(text)
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())



    '''
    更新说明：
        1. 单文件选取，文件夹选取
        2. 文件格式检测
        3. 格式过滤PNG JPGE
        4. 输出信息同统计说明
    '''
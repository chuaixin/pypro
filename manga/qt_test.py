import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QToolBar, QStatusBar, QAction, QTextEdit, QFileDialog

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ###################################################
        # 创建菜单栏
        menubar = self.menuBar()
        # 创建文件菜单
        file_menu = menubar.addMenu('File')
        # 创建文件菜单项
        new_action = QAction('New', self)
        open_action = QAction('Open', self)
        save_action = QAction('Save', self)
        exit_action = QAction('Exit', self)
        # 添加文件菜单项到文件菜单
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()  # 分隔线
        file_menu.addAction(exit_action)
        # 连接菜单项和工具按钮的槽函数
        new_action.triggered.connect(self.newFile)
        open_action.triggered.connect(self.openFile)
        save_action.triggered.connect(self.saveFile)
        exit_action.triggered.connect(self.exitApp)
        ###################################################
        # 创建工具栏
        toolbar = self.addToolBar('Toolbar')
        # 在工具栏中添加工具按钮
        new_button = toolbar.addAction('New')       # 清空（当前）文本编辑框
        open_button = toolbar.addAction('Open')     # 打开txt文本并添加到文本编辑框
        save_button = toolbar.addAction('Save')     # 保存文本编辑框到txt文本
        # 连接菜单项和工具按钮的槽函数
        new_button.triggered.connect(self.newFile)
        open_button.triggered.connect(self.openFile)
        save_button.triggered.connect(self.saveFile)
        ###################################################
        # 创建状态栏
        statusbar = self.statusBar()
        # 在状态栏中显示消息: 'Ready' 是要显示的文本消息，30000 是消息显示的时间（以毫秒为单位），即30秒。
        statusbar.showMessage('Ready', 30000)
        ###################################################
        # 创建文本编辑框
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)  # 将文本编辑框设置为主窗口的中心组件

    def newFile(self):
        self.text_edit.clear()  # 清空文本编辑框

    def openFile(self):
        try:
            # 打开文件对话框，选择txt文件并读取内容，然后显示在文本编辑框中
            file_dialog = QFileDialog(self)
            file_path, _ = file_dialog.getOpenFileName()
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_contents = file.read()
                    self.text_edit.setPlainText(file_contents)
        except Exception as e:
            # 处理异常，例如显示错误消息
            print(f"Error opening file: {str(e)}")

    def saveFile(self):
        try:
            # 保存文件对话框，将文本编辑框中的内容保存到txt文件中
            file_dialog = QFileDialog(self)
            file_path, _ = file_dialog.getSaveFileName()
            if file_path:
                with open(file_path, 'w') as file:
                    file_contents = self.text_edit.toPlainText()
                    file.write(file_contents)
        except Exception as e:
            # 处理异常，例如显示错误消息
            print(f"Error saving file: {str(e)}")

    def exitApp(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle('PyQt Text Editor')
    window.setGeometry(100, 100, 800, 300)
    window.show()
    sys.exit(app.exec_())


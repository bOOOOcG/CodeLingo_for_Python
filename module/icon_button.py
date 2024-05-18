# module\icon_button.py

import os
import sys

from PySide6.QtCore import Qt, Signal, QSize, QRect
from PySide6.QtGui import QPainter, QPixmap, QColor, QBrush, QPen, QMouseEvent, QPaintEvent
from PySide6.QtWidgets import QWidget

class PinButton(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._active = False  # 初始化_active属性

        # 检查是否运行在一个PyInstaller打包后的环境
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # 使用PyInstaller的临时文件夹
            base_dir = sys._MEIPASS
        else:
            # 未打包时，使用main.py的目录
            base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        self.icon_path_on = os.path.join(base_dir, "resource", "png", "pin_icon_1.png")
        self.icon_path_off = os.path.join(base_dir, "resource", "png", "pin_icon_2.png")

        # 尝试加载默认状态的PNG并等比缩小
        self.currentIconPixmap = self.loadAndScaleIcon(self.icon_path_off, 18)

        if self.currentIconPixmap.isNull():
            print("Failed to load icon:", self.icon_path_off)
        else:
            print("Icon loaded successfully:", self.icon_path_off)
            self.setFixedSize(18, 18)  # 设置控件大小为18px

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 根据当前状态渲染对应的PNG图标
        painter.drawPixmap(0, 0, self.currentIconPixmap)
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._active = not self._active  # 切换_active状态
            # 根据当前状态选择PNG路径并等比缩小
            iconPath = self.icon_path_on if self._active else self.icon_path_off
            self.currentIconPixmap = self.loadAndScaleIcon(iconPath, 18)

            if self.currentIconPixmap.isNull():
                print("Failed to toggle icon:", iconPath)
            else:
                print("Toggled icon successfully:", iconPath)
                self.update()  # 触发重绘
                self.setWindowOnTop(self._active)

    def loadAndScaleIcon(self, path, size):
        """加载并等比缩小图标到指定尺寸"""
        pixmap = QPixmap(path)
        return pixmap.scaled(QSize(size, size), Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def setWindowOnTop(self, on_top):
        parent = self.window()
        if on_top:
            parent.setWindowFlags(parent.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            parent.setWindowFlags(parent.windowFlags() & ~Qt.WindowStaysOnTopHint | Qt.Window)
        parent.show()


class SettingsButton(QWidget):
    form_server_error_signal = Signal(str)  
    form_client_error_signal = Signal(str)
    form_server_msg_signal = Signal(str, str)
    form_server_broadcast_signal = Signal(str)
    image_data_received = Signal(list)

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.setFixedSize(24, 24)
        self.hover = False  # 新增一个属性来标记鼠标是否悬停
    
        self.main_window = main_window
    
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            base_dir = sys._MEIPASS
        else:
            # 未打包时，使用main.py的目录
            base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    
        self.icon_path = os.path.join(base_dir, "resource", "png", "settings_icon.png")
        self.originalIconPixmap = self.loadAndScaleIcon(self.icon_path, 18)
        self.currentIconPixmap = self.originalIconPixmap
        self.iconColor = None

    def loadAndScaleIcon(self, path, size):
        try:
            pixmap = QPixmap(path)
            if pixmap.isNull():
                raise IOError("无法加载图标: " + path)
            return pixmap.scaled(QSize(size, size), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        except Exception as e:
            print("加载图标失败:", e)
            return QPixmap()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 在这里绘制圆角矩形背景
        if self.hover:
            rect = QRect(0, 0, self.width(), self.height())
            painter.setBrush(QBrush(QColor(28, 28, 30)))
            painter.setPen(Qt.NoPen)  # 无边框
            painter.drawRoundedRect(rect, 4, 4)  # 可以调整圆角半径

        if self.iconColor:
            coloredPixmap = self.applyColorToPixmap(self.currentIconPixmap, self.iconColor)
            painter.drawPixmap((self.width() - coloredPixmap.width()) / 2, (self.height() - coloredPixmap.height()) / 2, coloredPixmap)
        else:
            painter.drawPixmap((self.width() - self.currentIconPixmap.width()) / 2, (self.height() - self.currentIconPixmap.height()) / 2, self.currentIconPixmap)

    def applyColorToPixmap(self, pixmap, color):
        coloredPixmap = QPixmap(pixmap.size())
        coloredPixmap.fill(Qt.transparent)
        painter = QPainter(coloredPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        return coloredPixmap

    def enterEvent(self, event):
        self.hover = True  # 鼠标进入时设置 hover 为 True
        self.update()

    def leaveEvent(self, event):
        self.hover = False  # 鼠标离开时设置 hover 为 False
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.iconColor = QColor(57, 57, 61)
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.iconColor = QColor(28, 28, 30)
            self.update()
            self.onClick()

    def onClick(self):
        print("Settings button clicked")
        self.show_settingGUI()

    def show_settingGUI(self):
        # from module.gui_module.app_dialog import UsernameDialog
        # usernameDialog = UsernameDialog(self)
        # usernameDialog.usernameSubmitted.connect(self.main_window.client_socket_manager.set_username)
        # usernameDialog.exec()
        from module.gui_module.setting.setting_gui import MainGUI
        from module.config_manager import ConfigManager
        config_manager = ConfigManager()
        # 初始化实例
        self.settings_gui = MainGUI(config_manager)
        # 获取主窗口的位置
        main_window_rect = self.main_window.geometry()
        # 设置设置窗口的位置
        self.settings_gui.move(main_window_rect.x(), main_window_rect.y())
        # 显示窗口
        self.settings_gui.show()

class TranslateButton(QWidget):
    def __init__(self, customTextEdit, parent=None):
        super().__init__(parent)
        self.setFixedSize(24, 24)
        self.hover = False  # 标记鼠标是否悬停
        self.pressed = False  # 标记鼠标是否按下
        self.customTextEdit = customTextEdit

        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            base_dir = sys._MEIPASS
        else:
            # 未打包时，使用main.py的目录
            base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        # 使用翻译图标替换设置图标的路径
        self.icon_path = os.path.join(base_dir, "resource", "png", "translate_icon.png")
        self.originalIconPixmap = self.loadAndScaleIcon(self.icon_path, 18)
        self.currentIconPixmap = self.originalIconPixmap
        self.backgroundColor = QColor(28, 28, 30)  # 默认背景颜色
        self.borderColor = QColor(10, 132, 255)  # 默认边框颜色

    def loadAndScaleIcon(self, path, size):
        try:
            pixmap = QPixmap(path)
            if pixmap.isNull():
                raise IOError("无法加载图标: " + path)
            return pixmap.scaled(QSize(size, size), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        except Exception as e:
            print("加载图标失败:", e)
            return QPixmap()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制背景
        rect = QRect(0, 0, self.width(), self.height())
        painter.setBrush(QBrush(self.backgroundColor if not self.pressed else QColor(57, 57, 61)))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 4, 4)
        
        # 如果鼠标悬停在按钮上，绘制边框
        if self.hover:
            painter.setPen(QPen(self.borderColor, 1))
            painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 4, 4)
        
        # 绘制图标
        painter.drawPixmap((self.width() - self.currentIconPixmap.width()) / 2, 
                           (self.height() - self.currentIconPixmap.height()) / 2, 
                           self.currentIconPixmap)

    def enterEvent(self, event):
        self.hover = True
        self.update()

    def leaveEvent(self, event):
        self.hover = False
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressed = True
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressed = False  # 重置鼠标按下状态
            self.update()
            self.onClick()  # 调用onClick方法

    def onClick(self):
        # 调用CustomTextEdit的翻译方法
        self.customTextEdit.translate_to_english()

# module\gui_module\setting\style_manager.py

class StyleManager:
    def __init__(self, light_mode=True):
        self.light_mode = light_mode
        self.custom_style = """
"""

    def get_style(self):
        """ 根据当前主题模式获取样式, 加上自定义样式 """
        if self.light_mode:
            return self.get_light_style()
        else:
            return self.get_dark_style()
        
    def set_custom_style(self, custom_style):
        """ 设置自定义样式 """
        self.custom_style = custom_style

    def switch_style(self, light_mode):
        if light_mode:
            return self.get_light_style()
        else:
            return self.get_dark_style()

    def get_light_style(self):
        # 这里放置原始代码中的白色主题样式表字符串
        return """
/* QPushButton */
QPushButton {
    border: 1px solid rgb(242,242,247); /* 更新边框颜色 */
    padding: 4px;
    min-width: 65px;
    min-height: 12px;
    color: rgb(0, 0, 0); /* 更新字体颜色 */
    background-color: transparent; /* 更新背景颜色 */
}
QPushButton:hover {
    background-color: rgb(255,255,255); /* 悬停时的背景颜色 */
    border-color: rgb(0,122,255); /* 悬停时的边框颜色 */
}
QPushButton:pressed {
    background-color: rgb(233,233,234); /* 按下时的背景颜色 */
    border-color: rgb(242,242,247); /* 按下时的边框颜色 */
    color: rgb(0, 0, 0); /* 按下时的字体颜色, 假设你想保持黑色 */
}
QPushButton:disabled {
    color: rgb(233,233,234); /* 禁用状态的字体颜色 */
    background-color: rgb(242,242,247); /* 禁用状态的背景颜色, 假设你想和正常状态一致 */
    border-color: rgb(233,233,234); /* 禁用状态的边框颜色 */
}

/* QSS */

QWidget { 
    color: rgb(0, 0, 0);
    font-family: 'Segoe UI', sans-serif;
    background-color: rgb(242,242,247);
}
QLabel, QPushButton, QLineEdit, QCheckBox, QFrame {
    background-color: transparent;
    color: black; /* 黑色文字 */
}
QPushButton, QLineEdit, QSlider, QSpinBox  {
    background-color: rgb(233,233,234);
    border-radius: 10px;
    padding: 5px;
}
QTextEdit {
    background-color: rgb(233,233,234);
    color: black; /* 设置文本颜色为黑色，以便在浅色背景上更易读 */
    border-radius: 10px;
    padding: 5px;
}

/* QCheckBox */
QCheckBox::indicator {
    width: 14px;
    height: 14px;
    border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
    margin-left: 5px; /* 比如这里设置左外边距为5像素 */
}
/* QCheckBox 未选中时的样式 */
QCheckBox::indicator:unchecked {
    border: 1px solid rgb(233,233,234); /* 边框颜色 */
    background: rgb(233,233,234); /* 内部颜色设置为RGB(233,233,234),在QSS中使用16进制表示 */
    border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
}
/* QCheckBox 选中时的样式 */
QCheckBox::indicator:checked {
    border: 1px solid rgb(52,199,89); /* 边框颜色 */
    background: rgb(52,199,89); /* 选中时的内部颜色 */
    border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
}

            QCheckBox#closeCheckbox {
                margin-left: -2px; /* 减少左边距 */
                margin-top: 0px; /* 向下移动3像素 */
                margin-right: -5px; /* 减少右边距 */
                margin-bottom: 5px;
                /* 其他样式设置 */
            }
            QCheckBox#minimizeButton{
                margin-top: 0px; /* 向下移动3像素 */
                margin-left: -5px; /* 减少左边距 */
                margin-right: -5px; /* 减少右边距 */
                margin-bottom: 5px;
            }
            QCheckBox#fullscreenCheckbox {
                margin-top: 0px; /* 向下移动3像素 */
                margin-left: -5px; /* 减少左边距 */
                margin-bottom: 5px;
                /* 其他样式设置 */
            }
            #alwaysOnTopButton {
                margin-bottom: 15px;
                /* 其他样式设置 */
            }


            /* #closeCheckbox */
            QCheckBox#closeCheckbox::indicator {
                width: 14px;
                height: 14px;
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
                margin-left: 5px; /* 比如这里设置左外边距为5像素 */
            }
            /* QCheckBox 未选中时的样式 */
            QCheckBox#closeCheckbox::indicator:unchecked {
                border: 0px solid rgb(252,95,86); /* 边框颜色 */
                background: rgb(252,95,86); /* 内部颜色设置为RGB(57, 57, 61),在QSS中使用16进制表示 */
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
            }
            /* QCheckBox 选中时的样式 */
            QCheckBox#closeCheckbox::indicator:checked {
                border: 0px solid rgb(252,95,86); /* 边框颜色 */
                background: rgb(252,95,86); /* 选中时的内部颜色 */
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
            }
            
            /* #minimizeButton */
            QCheckBox#minimizeButton::indicator {
                width: 14px;
                height: 14px;
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
                margin-left: 5px; /* 比如这里设置左外边距为5像素 */
            }
            /* QCheckBox 未选中时的样式 */
            QCheckBox#minimizeButton::indicator:unchecked {
                border: 0px solid rgb(252,188,42); /* 边框颜色 */
                background: rgb(252,188,42); /* 内部颜色设置为RGB(57, 57, 61),在QSS中使用16进制表示 */
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
            }
            /* QCheckBox 选中时的样式 */
            QCheckBox#minimizeButton::indicator:checked {
                border: 0px solid rgb(252,188,42); /* 边框颜色 */
                background: rgb(252,188,42); /* 选中时的内部颜色 */
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
            }

            /* #fullscreenCheckbox */
            QCheckBox#fullscreenCheckbox::indicator {
                width: 14px;
                height: 14px;
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
                margin-left: 5px; /* 比如这里设置左外边距为5像素 */
            }
            /* QCheckBox 未选中时的样式 */
            QCheckBox#fullscreenCheckbox::indicator:unchecked {
                border: 0px solid rgb(38,201,63); /* 边框颜色 */
                background: rgb(38,201,63); /* 内部颜色设置为RGB(57, 57, 61),在QSS中使用16进制表示 */
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
            }
            /* QCheckBox 选中时的样式 */
            QCheckBox#fullscreenCheckbox::indicator:checked {
                border: 0px solid rgb(38,201,63); /* 边框颜色 */
                background: rgb(38,201,63); /* 选中时的内部颜色 */
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
            }

/* OutLabel */
#OutLabel {
    color: rgb(133,133,139); /* out文字颜色 */
    padding: 0px;
    font-size: 12px; /* 设置字体大小 */
    padding-bottom: 0px; /* 减少内边距 */
    margin-left: 24px;  /* 左边距为10像素 */
}

/* QFrame */
QFrame#FrameA {
    background-color: rgb(255,255,255);
    border-radius: 15px;
    margin-left: 10px;  /* 左边距为10像素 */
    margin-right: 10px; /* 右边距为10像素 */
    padding-top: 0px;  /* 上内边距为10像素 */
    padding-bottom: 0px; /* 下内边距为10像素 */
}
#FrameLabelA {
    background-color: rgb(255,255,255);
    font-size: 14px; /* 设置字体大小 */
}
#FrameLabelB {
    background-color: rgb(233,233,234);
    font-size: 13px; /* 设置字体大小 */
}
#comboboxA {
    background-color: rgb(233,233,234);
    font-size: 13px; /* 设置字体大小 */
}

/* Custom */
#GradientLine {
    color: rgb(225,225,226);
}
#SwitchButton {
    /* 关闭状态下的背景颜色 */
    qproperty-background_color_off: rgb(233,233,234);
    
    /* 打开状态下的背景颜色 */
    qproperty-background_color_on: rgb(52,199,89);
    
    /* 特殊情况下的第二个打开状态的背景颜色 */
    qproperty-background_color_red: rgb(254, 70, 40);
    
    /* 滑块的颜色 */
    qproperty-thumb_color: rgb(255, 255, 255);
}
/* NormalLine是分割线 */
#NormalLine {
    color: rgb(225,225,226);
}


/* scrollBar */
QScrollBar:vertical {
    border: none;
    background: rgb(28,28,30);
    /* width: 8px; */
    width: 0px;
    margin: 0px 0px 0px 0px;
}

QScrollBar::handle:vertical {
    background: rgba(85, 85, 89, 0.7);
    /* min-height: 20px; */
    min-height: 0px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: none;
    height: 0px;
}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
    background: none;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    border: none;
    background: rgb(28,28,30);
    /* height: 8px; */
    height: 0px;
    margin: 0px 0px 0px 0px;
}

QScrollBar::handle:horizontal {
    background: rgba(85, 85, 89, 0.7);
    /* min-width: 20px; */
    min-width: 0px;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    background: none;
    width: 0px;
}

QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
    background: none;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}

            /* LineEdit 设置padding: 3px */
            QLineEdit {
                padding: 4px;
            }

            /* QComboBox */
            QComboBox {
                background-color: rgb(233,233,234);
                border-radius: 10px;
                padding: 3px;
                color: black;
                padding-right: 10px; /* 调整右侧填充以确保文本在下拉箭头显示时也能居中 */
                padding-left: 10px; /* 根据实际情况可能需要调整左侧填充以确保文本居中 */
                text-align: center;
            }
            QComboBox::drop-down {
                border: none;
                width: 0px;
            }
            QComboBox::down-arrow {
                image: none;
            }
            /* 下拉列表项的样式 */
            QComboBox QAbstractItemView {
                background: rgb(255,255,255);
                border-radius: 10px; /* 使下拉列表项的边角与QComboBox一致 */
                color: black;
                padding: 0px; /* 移除内部填充，确保没有额外的空间 */
                margin: 0px; /* 移除外部间距，确保没有额外的空间 */
                outline: none; /* 移除选中时的轮廓线 */
            }
            /* 移除选中项的边距 */
            QComboBox QAbstractItemView::item {
                margin: 0px; /* 移除项的外部间距 */
                padding: 0px; /* 移除项的内部填充 */
                min-height: 0px; /* 设置最小高度，以减少额外空间 */
            }
            /* 移除选中项的背景和边距 */
            QComboBox QAbstractItemView::item:selected {
                background: rgb(255,255,255);
                border-radius: 10px; /* 使选中项的边角与QComboBox一致 */
                margin: 0px; /* 移除项的外部间距 */
                padding: 0px; /* 移除项的内部填充 */
            }

        """

    def get_dark_style(self):
        # 这里放置原始代码中的黑色主题样式表字符串
        return """
            /* QPushButton */
            QPushButton {
                border: 1px solid rgb(28, 28, 30); /* 更新边框颜色 */
                padding: 4px;
                min-width: 65px;
                min-height: 12px;
                color: rgb(255, 255, 255); /* 更新字体颜色 */
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: rgb(28, 28, 30); /* 悬停时的背景颜色 */
                border-color: rgb(10, 132, 255); /* 悬停时的边框颜色 */
            }
            QPushButton:pressed {
                background-color: rgb(57, 57, 61); /* 按下时的背景颜色 */
                border-color: rgb(28, 28, 30); /* 按下时的边框颜色 */
                color: rgb(255, 255, 255); /* 按下时的字体颜色, 假设你想保持白色 */
            }
            QPushButton:disabled {
                color: rgb(57, 57, 61); /* 禁用状态的字体颜色 */
                background-color: rgb(28, 28, 30); /* 禁用状态的背景颜色, 假设你想和正常状态一致 */
                border-color: rgb(57, 57, 61); /* 禁用状态的边框颜色 */
            }

            /* QPushButton#unbanButton */
            QPushButton#unbanButton {
                min-width: 30px;
                min-height: 12px;
            }
            
            /* QSS */
            QWidget {
                color: rgb(255, 255, 255); /* 主程序文本颜色 */
                font-family: 'Segoe UI', sans-serif; /* 主程序文本字体设置 */
                background-color: rgba(0, 0, 0, 232);
            }

            QLabel, QPushButton, QLineEdit, QCheckBox, QFrame {
                background-color: transparent;
                color: white; /* 白色文字 */
            }

            QPushButton, QLineEdit, QSlider, QSpinBox  {
                background-color: rgb(57,57,61);
                border-radius: 10px;
                padding: 5px;
            }
            QTextEdit {
                background-color: rgb(57,57,61);
                color: white; /* 设置文本颜色为白色，以便在深色背景上更易读 */
                border-radius: 10px;
                padding: 5px;
            }
            /* QLineEdit QSpinBox */

            /* QCheckBox */
            QCheckBox::indicator {
                width: 14px;
                height: 14px;
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
                margin-left: 5px; /* 比如这里设置左外边距为5像素 */
            }
            /* QCheckBox 未选中时的样式 */
            QCheckBox::indicator:unchecked {
                border: 0px solid rgb(57, 57, 61); /* 边框颜色 */
                background: rgb(57, 57, 61); /* 内部颜色设置为RGB(57, 57, 61),在QSS中使用16进制表示 */
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
            }
            /* QCheckBox 选中时的样式 */
            QCheckBox::indicator:checked {
                border: 0px solid rgb(38,201,63 ); /* 边框颜色 */
                background: rgb(38,201,63 ); /* 选中时的内部颜色 */
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
            }

            QCheckBox#closeCheckbox {
                margin-left: -2px; /* 减少左边距 */
                margin-top: 0px; /* 向下移动3像素 */
                margin-right: -5px; /* 减少右边距 */
                margin-bottom: 5px;
                /* 其他样式设置 */
            }
            QCheckBox#minimizeButton{
                margin-top: 0px; /* 向下移动3像素 */
                margin-left: -5px; /* 减少左边距 */
                margin-right: -5px; /* 减少右边距 */
                margin-bottom: 5px;
            }
            QCheckBox#fullscreenCheckbox {
                margin-top: 0px; /* 向下移动3像素 */
                margin-left: -5px; /* 减少左边距 */
                margin-bottom: 5px;
                /* 其他样式设置 */
            }
            #alwaysOnTopButton {
                margin-bottom: 15px;
                /* 其他样式设置 */
            }


            /* #closeCheckbox */
            QCheckBox#closeCheckbox::indicator {
                width: 14px;
                height: 14px;
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
                margin-left: 5px; /* 比如这里设置左外边距为5像素 */
            }
            /* QCheckBox 未选中时的样式 */
            QCheckBox#closeCheckbox::indicator:unchecked {
                border: 0px solid rgb(252,95,86); /* 边框颜色 */
                background: rgb(252,95,86); /* 内部颜色设置为RGB(57, 57, 61),在QSS中使用16进制表示 */
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
            }
            /* QCheckBox 选中时的样式 */
            QCheckBox#closeCheckbox::indicator:checked {
                border: 0px solid rgb(252,95,86); /* 边框颜色 */
                background: rgb(252,95,86); /* 选中时的内部颜色 */
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
            }
            
            /* #minimizeButton */
            QCheckBox#minimizeButton::indicator {
                width: 14px;
                height: 14px;
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
                margin-left: 5px; /* 比如这里设置左外边距为5像素 */
            }
            /* QCheckBox 未选中时的样式 */
            QCheckBox#minimizeButton::indicator:unchecked {
                border: 0px solid rgb(252,188,42); /* 边框颜色 */
                background: rgb(252,188,42); /* 内部颜色设置为RGB(57, 57, 61),在QSS中使用16进制表示 */
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
            }
            /* QCheckBox 选中时的样式 */
            QCheckBox#minimizeButton::indicator:checked {
                border: 0px solid rgb(252,188,42); /* 边框颜色 */
                background: rgb(252,188,42); /* 选中时的内部颜色 */
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
            }

            /* #fullscreenCheckbox */
            QCheckBox#fullscreenCheckbox::indicator {
                width: 14px;
                height: 14px;
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
                margin-left: 5px; /* 比如这里设置左外边距为5像素 */
            }
            /* QCheckBox 未选中时的样式 */
            QCheckBox#fullscreenCheckbox::indicator:unchecked {
                border: 0px solid rgb(38,201,63); /* 边框颜色 */
                background: rgb(38,201,63); /* 内部颜色设置为RGB(57, 57, 61),在QSS中使用16进制表示 */
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
            }
            /* QCheckBox 选中时的样式 */
            QCheckBox#fullscreenCheckbox::indicator:checked {
                border: 0px solid rgb(38,201,63); /* 边框颜色 */
                background: rgb(38,201,63); /* 选中时的内部颜色 */
                border-radius: 7px; /* 设置圆角半径为宽度或高度的一半来制造圆形效果 */
            }

/* OutLabel */
#OutLabel {
    color: rgb(133,133,139); /* out文字颜色 */
    padding: 0px;
    font-size: 12px; /* 设置字体大小 */
    padding-bottom: 0px; /* 减少内边距 */
    margin-left: 24px;  /* 左边距为10像素 */
}

/* QFrame */
/* 框架的样式 */
QFrame#FrameA {
    background-color: rgb(28, 28, 30);
    border-radius: 15px;
    margin-left: 10px;  /* 左边距为10像素 */
    margin-right: 10px; /* 右边距为10像素 */
    padding-top: 0px;  /* 上内边距为10像素 */
    padding-bottom: 0px; /* 下内边距为10像素 */
}
/* 框架内文本样式 */
#FrameLabelA {
    background-color: rgb(28, 28, 30);
    font-size: 14px; /* 设置字体大小 */
}
/* 框架内文本样式B 具体哪个是哪个你自己改着试就知道了 */
#FrameLabelB {
    background-color: rgb(57, 57, 61);
    font-size: 13px; /* 设置字体大小 */
}
/* comboboxA */
/* 组合框 如:修改语言的 修改注入主题的 */
#comboboxA {
    background-color: rgb(57,57,61);
    font-size: 13px; /* 设置字体大小 */
}
/* Custom */
/* GradientLine是有渐变效果的线 */
#GradientLine {
    color: rgb(59, 59, 63);
}
/* NormalLine是分割线 */
#NormalLine {
    color: rgb(59, 59, 63);
}
/* SwitchButton是可以切换开关字体按钮 */
#SwitchButton {
    /* 关闭状态下的背景颜色 */
    qproperty-background_color_off: rgb(57, 57, 62);
    
    /* 打开状态下的背景颜色 */
    qproperty-background_color_on: rgb(48, 209, 88);
    
    /* 特殊情况下的第二个打开状态的背景颜色 */
    qproperty-background_color_red: rgb(254, 70, 40);
    
    /* 滑块的颜色 */
    qproperty-thumb_color: rgb(255, 255, 255);
}


/* scrollBar */
QScrollBar:vertical {
    border: none;
    background: rgb(28,28,30);
    /* width: 8px; */
    width: 0px;
    margin: 0px 0px 0px 0px;
}

QScrollBar::handle:vertical {
    background: rgba(85, 85, 89, 0.7);
    min-height: 20px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: none;
    height: 0px;
}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
    background: none;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    border: none;
    background: rgb(28,28,30);
    height: 8px;
    margin: 0px 0px 0px 0px;
}

QScrollBar::handle:horizontal {
    background: rgba(85, 85, 89, 0.7);
    min-width: 20px;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    background: none;
    width: 0px;
}

QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
    background: none;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}

            /* QComboBox */
            QComboBox {
                background-color: rgb(57,57,61);
                border-radius: 10px;
                padding: 3px;
                color: white;
                padding-right: 10px; /* 调整右侧填充以确保文本在下拉箭头显示时也能居中 */
                padding-left: 10px; /* 根据实际情况可能需要调整左侧填充以确保文本居中 */
                text-align: center;
            }
            QComboBox::drop-down {
                border: none;
                width: 0px;
            }
            QComboBox::down-arrow {
                image: none;
            }
            /* 下拉列表项的样式 */
            QComboBox QAbstractItemView {
                background: rgb(28,28,30);
                border-radius: 10px; /* 使下拉列表项的边角与QComboBox一致 */
                color: white;
                padding: 0px; /* 移除内部填充，确保没有额外的空间 */
                margin: 0px; /* 移除外部间距，确保没有额外的空间 */
                outline: none; /* 移除选中时的轮廓线 */
            }
            /* 移除选中项的边距 */
            QComboBox QAbstractItemView::item {
                margin: 0px; /* 移除项的外部间距 */
                padding: 0px; /* 移除项的内部填充 */
                min-height: 0px; /* 设置最小高度，以减少额外空间 */
            }
            /* 移除选中项的背景和边距 */
            QComboBox QAbstractItemView::item:selected {
                background: rgb(52, 58, 64);
                border-radius: 10px; /* 使选中项的边角与QComboBox一致 */
                margin: 0px; /* 移除项的外部间距 */
                padding: 0px; /* 移除项的内部填充 */
            }

            /* LineEdit 设置padding: 3px */
            QLineEdit {
                padding: 4px;
            }

        """

# module\top_control_bar.py

import os
import sys

from PySide6.QtWidgets import (QWidget, QHBoxLayout, QCheckBox, QLabel)
from PySide6.QtCore import Qt

from module.icon_button import PinButton

class TopControlBar(QWidget):
    def __init__(self, main_window, image_loader=None, config=None, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.image_loader = image_loader
        self.config = config or {
            'show_status': False, 
            'show_page_label': False, 
            'show_always_on_top_button': False  # 默认显示置顶按钮
        }
        self.setup_ui()

    def setup_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # 移除布局的边距

        # 创建并设置复选框和按钮
        self.close_checkbox = QCheckBox()
        self.minimize_checkbox = QCheckBox()
        self.fullscreen_checkbox = QCheckBox("")
        self.always_on_top_pin_button = PinButton()

        self.close_checkbox.setObjectName("closeCheckbox")
        self.minimize_checkbox.setObjectName("minimizeButton")
        self.fullscreen_checkbox.setObjectName("fullscreenCheckbox")
        self.always_on_top_pin_button.setObjectName("alwaysOnTopPinButton")

        # 添加控件到布局
        self.layout.addStretch(1)
        self.layout.addWidget(self.close_checkbox, 5)
        self.layout.addWidget(self.minimize_checkbox, 5)
        self.layout.addWidget(self.fullscreen_checkbox, 5) 
        self.layout.addStretch(250)

        if self.config['show_page_label'] and self.image_loader:
            self.pageLabel = QLabel("imagine_id:null | Page: 0/0")
            self.layout.addWidget(self.pageLabel, 1)
            self.image_loader.pageUpdated.connect(self.updatePageLabel)
        self.layout.addStretch(125)
        self.layout.addStretch(125)

        if self.config['show_status']:
            self.status_label = QLabel("未连接")
            self.status_label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(self.status_label, 6)

        self.layout.addStretch(10)
        if self.config['show_always_on_top_button']:
            self.layout.addWidget(self.always_on_top_pin_button, 5)  # 只有配置为True时才添加

        # 连接槽函数
        self.close_checkbox.stateChanged.connect(self.main_window.close)
        self.minimize_checkbox.stateChanged.connect(self.handle_minimize_checkbox)
        self.fullscreen_checkbox.stateChanged.connect(self.toggle_fullscreen)

    def update_status(self, status_text, tooltip_text=None):
        if hasattr(self, 'status_label'):
            self.status_label.setText(status_text)
            if tooltip_text:
                self.status_label.setToolTip(tooltip_text)

    def updatePageLabel(self):
        if hasattr(self, 'pageLabel'):
            total_pages = len(self.image_loader.imagesData)
            current_page = self.image_loader.currentIndex + 1
            current_image_info = self.image_loader.getCurrentImageInfo()
            imagine_id = current_image_info.get('imagine_id', 'null') if current_image_info else 'null'
            self.pageLabel.setText(f"imagine_id:{imagine_id} | Page: {current_page}/{total_pages}")

    def toggle_fullscreen(self, state):
        if state:
            self.main_window.showFullScreen()
        else:
            self.main_window.showNormal()

    def toggle_always_on_top(self, state):
        current_flags = self.main_window.windowFlags()
        stay_on_top_flag = Qt.WindowStaysOnTopHint
        if state:
            new_flags = current_flags | stay_on_top_flag
        else:
            new_flags = current_flags & ~stay_on_top_flag

        self.main_window.setWindowFlags(new_flags)
        self.main_window.hide()
        self.main_window.show()

    def handle_minimize_checkbox(self, state):
        if state:
            self.main_window.showMinimized()
        else:
            self.main_window.showNormal()
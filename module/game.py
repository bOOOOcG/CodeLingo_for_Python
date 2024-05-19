from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, 
    QLineEdit, QMessageBox, QGridLayout, QPlainTextEdit, QHBoxLayout, QSpacerItem, 
    QSizePolicy
)
from PySide6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QBrush, QColor, QPainter, QTextFormat
from PySide6.QtCore import Qt, QPoint, QRegularExpression, QSize
from levels import (Level1, Level2, Level3, Level4, Level5, Boss1,
                    Level6, Level7, Level8, Level9, Level10, Boss2,
                    )
from module.config_manager import ConfigManager
from module.style_manager import StyleManager
from module.save_manager import SaveManager
from module.menu import MainMenu
from module.top_control_bar import TopControlBar
import time
 
class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 关键词格式
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QBrush(QColor(86, 156, 214)))  # 蓝色
        keyword_format.setFontWeight(QFont.Bold)
        keywords = ["and", "as", "assert", "break", "class", "continue", "def", "del", "elif", "else", "except", "False", "finally", "for", "from", "global", "if", "import", "in", "is", "lambda", "None", "nonlocal", "not", "or", "pass", "raise", "return", "True", "try", "while", "with", "yield"]
        self.highlighting_rules = [(QRegularExpression(r'\b' + kw + r'\b'), keyword_format) for kw in keywords]

        # 单行注释格式
        single_line_comment_format = QTextCharFormat()
        single_line_comment_format.setForeground(QBrush(QColor(106, 153, 85)))  # 绿色
        self.highlighting_rules.append((QRegularExpression("#[^\n]*"), single_line_comment_format))

        # 引号格式
        quotation_format = QTextCharFormat()
        quotation_format.setForeground(QBrush(QColor(206, 145, 120)))  # 紫红色
        self.highlighting_rules.append((QRegularExpression("\".*\""), quotation_format))
        self.highlighting_rules.append((QRegularExpression("\'.*\'"), quotation_format))

        # 函数名格式
        function_format = QTextCharFormat()
        function_format.setForeground(QBrush(QColor(220, 220, 170)))  # 黄色
        self.highlighting_rules.append((QRegularExpression(r'\b[A-Za-z_][A-Za-z0-9_]*(?=\()'), function_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            match_iterator = expression.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class CodeTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setFont(QFont("Courier", 10))
        self.setPlaceholderText("在此输入代码...")
        self.highlighter = PythonHighlighter(self.document())

        self.setViewportMargins(50, 0, 0, 0)  # 为行号添加边距
        self.line_number_area = LineNumberArea(self)
        self.update_line_number_area_width(0)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area(self, rect=None, dy=None):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            if rect is None:
                rect = self.contentsRect()
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect and rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(cr.left(), cr.top(), self.line_number_area_width(), cr.height())

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(41, 53, 66)  # 比较暗的蓝灰色
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), Qt.lightGray)
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.line_number_area.width(), self.fontMetrics().height(), Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)

class PythonAdventurerGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeLingo for Python")

        self.setWindowFlags(Qt.FramelessWindowHint)  # 移除默认的窗口控制按钮

        self.config_manager = ConfigManager()
        self.user_code = ""
        self.save_manager = SaveManager()

        # 添加自定义的控制条
        self.top_control_bar = TopControlBar(self)
        self.set_menu_bar(self.top_control_bar)

        self.setup_main_menu()
        self.setup_level_ui()
        self.setup_level_selector()
        self.setup_levels()
        self.update_level_buttons()

        self.current_level = 0
        self.start_time = None

        # 从ConfigManager获取lightMode的值
        light_mode_setting = self.config_manager.get_setting("Visual.light_mode")
        # 确保light_mode_setting不是None，如果是None，则默认为True
        light_mode = light_mode_setting if light_mode_setting is not None else True
        self.style_manager = StyleManager(light_mode=light_mode)
        self.setStyleSheet(self.style_manager.get_style())

    def set_menu_bar(self, bar):
        self.menu_container = QWidget()
        self.menu_layout = QVBoxLayout(self.menu_container)
        self.menu_layout.setContentsMargins(10, 10, 10, 10)
        self.menu_layout.addWidget(bar)

        self.content_widget = QWidget()  # 容纳实际内容的部件
        self.content_layout = QVBoxLayout(self.content_widget)  # 为 content_widget 设置布局
        self.menu_layout.addWidget(self.content_widget)

        self.setCentralWidget(self.menu_container)

    def setup_main_menu(self):
        self.main_menu = MainMenu(self)
        self.content_layout.addWidget(self.main_menu)

    def setup_level_ui(self):
        self.level_widget = QWidget()
        self.level_layout = QVBoxLayout(self.level_widget)

        self.label = QLabel("欢迎使用CodeLingo for Python")
        self.level_layout.addWidget(self.label)

        self.code_text_edit = CodeTextEdit()  # 使用自定义的 CodeTextEdit
        self.code_text_edit.setFixedHeight(400)  # 设置默认高度为20行
        self.level_layout.addWidget(self.code_text_edit)

        self.output_label = QLabel("")
        self.level_layout.addWidget(self.output_label)

        # 创建运行代码和教学按钮所在的水平布局
        run_teach_layout = QHBoxLayout()
        run_teach_layout.addStretch(1)  # 左侧弹簧

        self.run_button = QPushButton("运行代码")
        self.run_button.clicked.connect(self.run_code)
        run_teach_layout.addWidget(self.run_button)

        self.teaching_button = QPushButton("教学")
        self.teaching_button.clicked.connect(self.show_teaching)
        run_teach_layout.addWidget(self.teaching_button)

        run_teach_layout.addStretch(1)  # 右侧弹簧
        self.level_layout.addLayout(run_teach_layout)

        # 创建显示答案和显示提示按钮所在的水平布局
        answer_hint_layout = QHBoxLayout()
        answer_hint_layout.addStretch(1)  # 左侧弹簧

        self.answer_button = QPushButton("显示答案")
        self.answer_button.clicked.connect(self.show_answer)
        answer_hint_layout.addWidget(self.answer_button)

        self.hint_button = QPushButton("显示提示")
        self.hint_button.clicked.connect(self.show_hint)
        answer_hint_layout.addWidget(self.hint_button)

        answer_hint_layout.addStretch(1)  # 右侧弹簧
        self.level_layout.addLayout(answer_hint_layout)

        self.console_log = QPlainTextEdit()
        self.console_log.setReadOnly(True)
        self.console_log.setVisible(self.config_manager.get_setting("General.show_console_log", False))
        self.level_layout.addWidget(self.console_log)

        self.level_layout.addStretch(1)  # 垂直弹簧

        # 创建上一关和下一关按钮所在的水平布局
        nav_buttons_layout = QHBoxLayout()
        nav_buttons_layout.addStretch(1)  # 左侧弹簧

        self.prev_level_button = QPushButton("上一关")
        self.prev_level_button.clicked.connect(self.prev_level)
        nav_buttons_layout.addWidget(self.prev_level_button)

        self.next_level_button = QPushButton("下一关")
        self.next_level_button.setEnabled(False)  # 初始化为禁用状态
        self.next_level_button.clicked.connect(self.next_level)
        nav_buttons_layout.addWidget(self.next_level_button)

        nav_buttons_layout.addStretch(1)  # 右侧弹簧
        self.level_layout.addLayout(nav_buttons_layout)

        self.level_layout.addStretch(1)  # 垂直弹簧

        self.back_to_menu_button = QPushButton("返回菜单")
        self.back_to_menu_button.clicked.connect(self.show_main_menu)
        self.level_layout.addWidget(self.back_to_menu_button)

    def setup_level_selector(self):
        self.level_selector_widget = QWidget()
        self.level_selector_layout = QVBoxLayout(self.level_selector_widget)
        self.level_buttons_layout = QGridLayout()
        self.level_selector_layout.addLayout(self.level_buttons_layout)

        # 添加垂直的伸缩空间在关卡按钮和翻页按钮之间
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.level_selector_layout.addItem(spacer)

        button_layout = QHBoxLayout()

        self.prev_button = QPushButton("上一页")
        self.prev_button.clicked.connect(self.prev_page)
        button_layout.addWidget(self.prev_button)

        # 添加一个空白的伸缩空间在翻页按钮之间
        page_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_layout.addItem(page_spacer)

        self.next_button = QPushButton("下一页")
        self.next_button.clicked.connect(self.next_page)
        button_layout.addWidget(self.next_button)

        self.level_selector_layout.addLayout(button_layout)

        self.current_page = 0
        self.levels_per_page = 25

    def setup_levels(self):
        level_classes = [Level1, Level2, Level3, Level4, Level5, Boss1,
                         Level6, Level7, Level8, Level9, Level10, Boss2]
        self.levels = [cls(self) for cls in level_classes]

    def show_main_menu(self):
        # 清空 content_layout 的内容
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.setup_main_menu()
    
    def start_game(self):
        self.setCentralWidget(self.level_widget)
        self.select_level(self.current_level)

    def update_level_buttons(self):
        # 清空当前布局中的所有按钮
        for i in reversed(range(self.level_buttons_layout.count())):
            widget = self.level_buttons_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
    
        levels_to_display = self.levels
        start_index = self.current_page * self.levels_per_page
        end_index = min(start_index + self.levels_per_page, len(levels_to_display))
    
        columns = 6  # 假设每行最多显示6个关卡按钮
    
        for i in range(start_index, end_index):
            # 设置按钮标签
            level_name = f"关卡 {i + 1}"
            if "Boss" in type(self.levels[i]).__name__:
                level_name = type(self.levels[i]).__name__
    
            button = QPushButton(level_name)
            button.clicked.connect(self.create_select_level_func(i))
    
            # 动态计算按钮的行和列
            row, col = divmod(i - start_index, columns)
            self.level_buttons_layout.addWidget(button, row, col)
    
        # 添加伸缩空间
        self.level_selector_layout.addStretch()
    
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(end_index < len(levels_to_display))
    
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_level_buttons()

    def next_page(self):
        if (self.current_page + 1) * self.levels_per_page < len(self.levels):
            self.current_page += 1
            self.update_level_buttons()

    def prev_level(self):
        prev_index = self.current_level - 1
        if prev_index >= 0:
            self.select_level(prev_index)

    def next_level(self):
        next_index = self.current_level + 1
        if next_index < len(self.levels):
            self.select_level(next_index)
        else:
            self.end_game()

    def create_select_level_func(self, index):
        def select_level():
            self.select_level(index)
        return select_level

    def select_level(self, index):
        self.current_level = index
        level = self.levels[self.current_level]
        
        # 清空 content_layout 中现有的布局和小部件
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        self.setup_level_ui()  # 重新创建 level_widget 和其内容
        self.label.setText(level.description())
        self.code_text_edit.clear()
        self.output_label.clear()
        self.console_log.clear()
        self.start_time = time.time()
    
        # 将 level_widget 添加到 content_widget 中
        self.content_layout.addWidget(self.level_widget)
        # self.update_level_info()
    
    def update_level_info(self):
        level = self.levels[self.current_level]
        self.label.setText(f"当前关卡: {self.current_level + 1}\n\n{level.description()}")

    def show_teaching(self):
        level = self.levels[self.current_level]
        teaching_message = level.teaching()
        self.console_log.appendPlainText(teaching_message)
        QMessageBox.information(self, "教学", teaching_message)

    def show_answer(self):
        level = self.levels[self.current_level]
        answer_message = level.answer()
        self.console_log.appendPlainText(answer_message)
        QMessageBox.information(self, "答案", answer_message)

    def show_hint(self):
        level = self.levels[self.current_level]
        hint_message = level.hint()
        self.console_log.appendPlainText(hint_message)
        QMessageBox.information(self, "提示", hint_message)

    def run_code(self):
        self.user_code = self.code_text_edit.toPlainText()
        level = self.levels[self.current_level]
        success, message = level.check_code(self.user_code)
        self.console_log.appendPlainText(self.user_code)
        if success:
            # 运行所有测试用例
            success, message = level.run_all_tests(self.user_code)
            self.output_label.setText(message)
            self.console_log.appendPlainText(message)
            if success:
                self.next_level_button.setEnabled(True)  # 成功后解禁“下一关”按钮
                QMessageBox.information(self, "成功", "恭喜你完成这一关！")
                end_time = time.time()
                time_taken = end_time - self.start_time
                self.save_manager.save_progress(f"关卡 {self.current_level + 1}", time_taken)
            else:
                QMessageBox.warning(self, "错误", message)
        else:
            self.output_label.setText(message)
            self.console_log.appendPlainText(message)

    def run_test(self):
        test_input = self.name_input.text()
        if not test_input:
            QMessageBox.warning(self, "测试错误", "测试数据错误。")
            return
        level = self.levels[self.current_level]
        success, message = level.run_test(test_input, self.user_code)
        self.output_label.setText(message)
        if success:
            QMessageBox.information(self, "成功", message)
        else:
            QMessageBox.warning(self, "失败", message)

    def end_game(self):
        self.label.setText("恭喜你完成所有任务！")
        self.code_text_edit.hide()
        self.run_button.hide()
        self.teaching_button.hide()
        self.name_input.hide()
        self.age_input.hide()
        self.test_button.hide()
        self.output_label.setText("")

    def show_level_selector(self):
        # 清空 content_widget 中现有的布局和小部件
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.level_selector_widget = QWidget()  # 重新创建 level_selector_widget 对象
        self.level_selector_layout = QVBoxLayout(self.level_selector_widget)
        self.level_buttons_layout = QGridLayout()
        self.level_selector_layout.addLayout(self.level_buttons_layout)

        button_layout = QHBoxLayout()

        self.prev_button = QPushButton("上一页")
        self.prev_button.clicked.connect(self.prev_page)
        button_layout.addWidget(self.prev_button)
        button_layout.setStretch(0, 1)  # 设置“上一页”按钮占 1/3

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_layout.addItem(spacer)
        button_layout.setStretch(1, 1)  # 设置空白弹簧占 1/3

        self.next_button = QPushButton("下一页")
        self.next_button.clicked.connect(self.next_page)
        button_layout.addWidget(self.next_button)
        button_layout.setStretch(2, 1)  # 设置“下一页”按钮占 1/3

        self.level_selector_layout.addLayout(button_layout)

        self.update_level_buttons()

        self.content_layout.addWidget(self.level_selector_widget)
    
    def load_last_level(self):
        progress = self.save_manager.get_progress()
        if progress:
            last_level = max(progress.keys(), key=lambda x: int(x.split()[1]))
            self.select_level(int(last_level.split()[1]) - 1)
            self.start_game()
        else:
            QMessageBox.information(self, "信息", "没有找到已保存的进度。")

    def save_game(self):
        # 这里可以实现更多的存档功能
        pass

    def moveEvent(self, event):
        super().moveEvent(event)
        if hasattr(self, 'backWindow'):
            # frame_width = self.frameGeometry().width() - self.geometry().width()
            # frame_height = self.frameGeometry().height() - self.geometry().height()
            # self.backWindow.move(self.x() + frame_width, self.y() + frame_height)
            self.backWindow.move(self.x(), self.y())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isDragging = True
            self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.isDragging:
            delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isDragging = False
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, 
    QLineEdit, QMessageBox, QGridLayout, QPlainTextEdit
)
from levels import (Level1, Level2, Level3, Level4, Level5, Boss1,
                    Level6, Level7, Level8, Level9, Level10, Boss2,
                    )
from module.config_manager import ConfigManager
from module.save_manager import SaveManager
from module.menu import MainMenu
import time
 
class PythonAdventurerGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeLingo for Python")

        self.config_manager = ConfigManager()
        self.user_code = ""
        self.save_manager = SaveManager()

        self.setup_main_menu()
        self.setup_level_ui()
        self.setup_level_selector()
        self.setup_levels()
        self.update_level_buttons()

        self.current_level = 0
        self.start_time = None

    def setup_main_menu(self):
        self.main_menu = MainMenu(self)
        self.setCentralWidget(self.main_menu)

    def setup_level_ui(self):
        self.level_widget = QWidget()
        self.level_layout = QVBoxLayout(self.level_widget)

        self.label = QLabel("欢迎使用CodeLingo for Python")
        self.level_layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        self.level_layout.addWidget(self.text_edit)

        self.run_button = QPushButton("运行代码")
        self.run_button.clicked.connect(self.run_code)
        self.level_layout.addWidget(self.run_button)

        self.teaching_button = QPushButton("教学")
        self.teaching_button.clicked.connect(self.show_teaching)
        self.level_layout.addWidget(self.teaching_button)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("输入名字")
        self.level_layout.addWidget(self.name_input)

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("输入年龄")
        self.level_layout.addWidget(self.age_input)

        self.test_button = QPushButton("运行测试")
        self.test_button.clicked.connect(self.run_test)
        self.level_layout.addWidget(self.test_button)

        self.output_label = QLabel("")
        self.level_layout.addWidget(self.output_label)

        self.console_log = QPlainTextEdit()
        self.console_log.setReadOnly(True)
        self.console_log.setVisible(self.config_manager.get_setting("show_console_log", False))
        self.level_layout.addWidget(self.console_log)

        self.back_to_menu_button = QPushButton("返回菜单")
        self.back_to_menu_button.clicked.connect(self.show_main_menu)
        self.level_layout.addWidget(self.back_to_menu_button)

    def setup_level_selector(self):
        self.level_selector_widget = QWidget()
        self.level_selector_layout = QVBoxLayout(self.level_selector_widget)
        self.level_buttons_layout = QGridLayout()
        self.level_selector_layout.addLayout(self.level_buttons_layout)

        self.prev_button = QPushButton("上一页")
        self.prev_button.clicked.connect(self.prev_page)
        self.level_selector_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("下一页")
        self.next_button.clicked.connect(self.next_page)
        self.level_selector_layout.addWidget(self.next_button)

        self.current_page = 0
        self.levels_per_page = 25

    def setup_levels(self):
        level_classes = [Level1, Level2, Level3, Level4, Level5, Boss1,
                         Level6, Level7, Level8, Level9, Level10, Boss2]
        self.levels = [cls(self) for cls in level_classes]

    def show_main_menu(self):
        self.main_menu = MainMenu(self)  # 重新创建 MainMenu 对象
        self.setCentralWidget(self.main_menu)

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

    def create_select_level_func(self, index):
        def select_level():
            self.select_level(index)
        return select_level

    def select_level(self, index):
        self.current_level = index
        level = self.levels[self.current_level]
        self.label.setText(level.description())
        self.text_edit.clear()
        self.output_label.clear()
        self.console_log.clear()
        self.name_input.hide()
        self.age_input.hide()
        self.test_button.hide()
        self.start_time = time.time()
        self.setCentralWidget(self.level_widget)
        self.update_level_info()

    def update_level_info(self):
        level = self.levels[self.current_level]
        self.label.setText(f"当前关卡: {self.current_level + 1}\n\n{level.description()}")

    def show_teaching(self):
        level = self.levels[self.current_level]
        teaching_message = level.teaching()
        self.console_log.appendPlainText(teaching_message)
        QMessageBox.information(self, "教学", teaching_message)

    def run_code(self):
        self.user_code = self.text_edit.toPlainText()
        level = self.levels[self.current_level]
        success, message = level.check_code(self.user_code)
        self.console_log.appendPlainText(self.user_code)
        if success:
            # 运行所有测试用例
            success, message = level.run_all_tests(self.user_code)
            if success:
                self.output_label.setText(message)
                self.console_log.appendPlainText(f"输出：{message}")
                QMessageBox.information(self, "成功", "恭喜你完成这一关！")
                end_time = time.time()
                time_taken = end_time - self.start_time
                self.save_manager.save_progress(f"关卡 {self.current_level + 1}", time_taken)
                self.next_level()
            else:
                self.output_label.setText(message)
                self.console_log.appendPlainText(message)
        else:
            self.output_label.setText(message)
            self.console_log.appendPlainText(message)

    def run_test(self):
        test_input = self.name_input.text()
        if not test_input:
            QMessageBox.warning(self, "输入错误", "请输入有效的测试数据。")
            return
        level = self.levels[self.current_level]
        success, message = level.run_test(test_input, self.user_code)
        self.output_label.setText(message)
        if success:
            QMessageBox.information(self, "成功", message)
        else:
            QMessageBox.warning(self, "失败", message)

    def next_level(self):
        next_index = self.current_level + 1
        if next_index < len(self.levels):
            self.select_level(next_index)
        else:
            self.end_game()

    def end_game(self):
        self.label.setText("恭喜你完成所有任务！")
        self.text_edit.hide()
        self.run_button.hide()
        self.teaching_button.hide()
        self.name_input.hide()
        self.age_input.hide()
        self.test_button.hide()
        self.output_label.setText("")

    def show_level_selector(self):
        self.setCentralWidget(self.level_selector_widget)

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

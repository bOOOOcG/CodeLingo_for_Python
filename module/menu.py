from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGridLayout

class MainMenu(QWidget):
    def __init__(self, game):
        super().__init__()
        
        self.game = game
        self.layout = QVBoxLayout(self)

        self.continue_button = QPushButton("继续游戏")
        self.continue_button.clicked.connect(self.continue_game)
        self.layout.addWidget(self.continue_button)

        self.select_level_button = QPushButton("选择关卡")
        self.select_level_button.clicked.connect(self.select_level)
        self.layout.addWidget(self.select_level_button)

        self.settings_button = QPushButton("设置")
        self.settings_button.clicked.connect(self.show_settings)
        self.layout.addWidget(self.settings_button)

        self.save_button = QPushButton("存档")
        self.save_button.clicked.connect(self.save_game)
        self.layout.addWidget(self.save_button)

        self.exit_button = QPushButton("退出")
        self.exit_button.clicked.connect(self.exit_game)
        self.layout.addWidget(self.exit_button)

    def continue_game(self):
        self.game.load_last_level()

    def select_level(self):
        self.game.show_level_selector()

    def show_settings(self):
        # 设置界面功能可以在这里实现
        pass

    def save_game(self):
        self.game.save_game()

    def exit_game(self):
        self.game.close()

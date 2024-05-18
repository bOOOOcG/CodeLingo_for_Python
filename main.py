from PySide6.QtWidgets import QApplication
from module.game import PythonAdventurerGame

if __name__ == "__main__":
    app = QApplication([])

    game = PythonAdventurerGame()
    game.show()

    app.exec()

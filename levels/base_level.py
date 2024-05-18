class BaseLevel:
    def __init__(self, game):
        self.game = game

    def description(self):
        raise NotImplementedError("每个关卡必须提供描述。")

    def check_code(self, code):
        raise NotImplementedError("每个关卡必须实现代码检查。")

    def teaching(self):
        raise NotImplementedError("每个关卡必须提供教学内容。")

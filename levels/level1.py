from levels.base_level import BaseLevel

class Level1(BaseLevel):
    def description(self):
        return "第一关：打印输出\n任务：使用 print 函数打印出“点燃火把！”"

    def check_code(self, code):
        if "print" in code and '点燃火把' in code:
            return True, "火把点燃了！"
        else:
            return False, "代码错误，请检查你的代码并重试。"

    def teaching(self):
        return ("在 Python 中，print 函数用于输出信息到控制台。"
                "使用 print('内容') 的格式可以将内容打印出来。例如：\n"
                "print('Hello, World!') 将打印出 Hello, World!")
    
    def answer(self):
        return "print('点燃火把！')"

    def hint(self):
        return "提示：使用 print 函数，并在括号内加上双引号和内容。"

    def run_all_tests(self, user_code):
        # 运行所有测试用例的逻辑
        success, message = self.check_code(user_code)
        if success:
            return True, "所有测试用例通过"
        else:
            return False, "部分测试用例未通过，请检查代码"

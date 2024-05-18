from levels.base_level import BaseLevel
import io
import contextlib

class Level5(BaseLevel):
    def description(self):
        return ("第五关：函数\n"
                "任务：定义一个函数 greet(name, age, height)，该函数接收三个参数：名字、年龄和身高，并打印出 '你好, name！你今年 age 岁，身高 height 米。'。\n"
                "然后调用这个函数。")

    def check_code(self, code):
        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误: {e}"

        if 'greet' not in local_namespace:
            return False, "代码错误：请定义函数 'greet'。"
        if not callable(local_namespace['greet']):
            return False, "代码错误：'greet' 应该是一个函数。"

        test_name = "测试"
        test_age = 30
        test_height = 1.75
        try:
            with contextlib.redirect_stdout(output):
                local_namespace['greet'](test_name, test_age, test_height)
        except Exception as e:
            return False, f"代码运行错误: {e}"

        printed_output = output.getvalue().strip()
        expected_output = f"你好, {test_name}！你今年 {test_age} 岁，身高 {test_height} 米。"
        if not printed_output:
            return False, "代码错误：输出为空，请检查是否正确调用了 'greet' 函数，并确保使用了正确的字符串格式化方法。"

        if printed_output != expected_output:
            if '{name}' in code or '{age}' in code or '{height}' in code:
                return False, "代码错误：请使用正确的字符串格式化方法，例如 f-string 或 .format。当前输出: {printed_output}"
            return False, f"代码错误，请使用正确的格式打印出 '{expected_output}'。当前输出: {printed_output}"

        return True, "代码正确！"

    def teaching(self):
        return ("函数用于将一段代码封装成一个可重复使用的代码块。使用 def 关键字来定义函数。例如：\n"
                "def 函数名(参数1, 参数2, ...):\n"
                "    # 函数体\n"
                "函数体内的代码块会在调用函数时执行。")

    def answer(self):
        return ("def greet(name, age, height):\n"
                "    print(f'你好, {name}！你今年 {age} 岁，身高 {height} 米。')\n"
                "\n"
                "greet('测试', 30, 1.75)")

    def hint(self):
        return ("提示：定义一个接收三个参数的函数，并使用 print 函数输出格式化的字符串。\n"
                "例如，使用 f-string 格式化字符串：\n"
                "print(f'你好, {name}！你今年 {age} 岁，身高 {height} 米。')")

    def run_all_tests(self, user_code):
        return self.check_code(user_code)

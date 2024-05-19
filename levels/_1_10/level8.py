import ast
from levels.base_level import BaseLevel
import io
import contextlib

class Level8(BaseLevel):
    def description(self):
        return ("第八关：字符串操作\n"
                "任务：定义一个函数 string_operations(text)，该函数接收一个字符串 text。\n"
                "1. 打印字符串的长度。\n"
                "2. 打印字符串的第一个字符和最后一个字符。\n"
                "3. 打印字符串中所有的单词。")

    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"代码执行错误: 语法错误在第 {e.lineno} 行: {e.text.strip()}"

        function_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "string_operations":
                function_found = True

        if not function_found:
            return False, "代码错误：请定义函数 string_operations。"

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误: {e}"

        if 'string_operations' not in local_namespace:
            return False, "代码错误：请定义函数 string_operations。"
        if not callable(local_namespace['string_operations']):
            return False, "代码错误：string_operations 应该是一个函数。"

        return True, "代码检查通过！现在输入测试数据并运行代码。"

    def run_test(self, func, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                func(*args)
            except Exception as e:
                return False, f"测试运行错误: {e}"

        printed_output = output.getvalue().strip().split('\n')
        text = args[0]
        words = text.split()
        expected_output = [str(len(text)), text[0], text[-1]]
        expected_output.extend(words)

        if printed_output != expected_output:
            return False, f"测试运行失败，请检查输出格式。当前输出: {printed_output}"

        return True, f"测试运行成功！当前输出: {printed_output}"

    def run_all_tests(self, user_code):
        test_cases = [
            "Hello world from Python",
            "Learning Python is fun",
            "Test case with multiple words"
        ]

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(user_code, {}, local_namespace)
                if 'string_operations' not in local_namespace or not callable(local_namespace['string_operations']):
                    return False, "代码错误：请定义函数 string_operations。"
            except Exception as e:
                return False, f"代码执行错误: {e}"

        string_operations_func = local_namespace['string_operations']

        for text in test_cases:
            success, message = self.run_test(string_operations_func, text)
            if not success:
                return False, message

        return True, "所有测试用例通过！"

    def teaching(self):
        return ("在这个关卡中，你需要学习如何操作字符串。你需要定义一个函数，并在函数内使用字符串方法和操作。\n"
                "例如，使用 len() 函数获取字符串的长度，使用索引访问字符串的第一个和最后一个字符，"
                "以及使用 split() 方法将字符串分割成单词。")

    def answer(self):
        return ("def string_operations(text):\n"
                "    print(len(text))\n"
                "    print(text[0])\n"
                "    print(text[-1])\n"
                "    words = text.split()\n"
                "    for word in words:\n"
                "        print(word)")

    def hint(self):
        return ("提示：你需要定义一个接收字符串参数的函数，并在函数内使用字符串的方法。\n"
                "例如，使用 len() 函数获取字符串的长度，使用索引访问字符串的第一个和最后一个字符，"
                "以及使用 split() 方法将字符串分割成单词。")


import ast
from levels.base_level import BaseLevel
import io
import contextlib

class Level10(BaseLevel):
    def description(self):
        return ("第十关：文件操作\n"
                "任务：定义一个函数 file_operations(filename)，该函数接收一个文件名 filename。\n"
                "1. 读取文件内容并打印出来。\n"
                "2. 将文件内容按行读取并打印每行的长度。")

    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"代码执行错误: 语法错误在第 {e.lineno} 行: {e.text.strip()}"

        function_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "file_operations":
                function_found = True

        if not function_found:
            return False, "代码错误：请定义函数 file_operations。"

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误: {e}"

        if 'file_operations' not in local_namespace:
            return False, "代码错误：请定义函数 file_operations。"
        if not callable(local_namespace['file_operations']):
            return False, "代码错误：file_operations 应该是一个函数。"

        return True, "代码检查通过！现在输入测试数据并运行代码。"

    def run_test(self, func, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                func(*args)
            except Exception as e:
                return False, f"测试运行错误: {e}"

        printed_output = output.getvalue().strip().split('\n')
        filename = args[0]
        with open(filename, 'r') as file:
            content = file.read()
            file.seek(0)
            lines = file.readlines()

        expected_output = [content.strip()]
        expected_output.extend([str(len(line.strip())) for line in lines])

        if printed_output != expected_output:
            return False, f"测试运行失败，请检查输出格式。当前输出: {printed_output}"

        return True, "测试运行成功！"

    def run_all_tests(self, user_code):
        # 创建测试文件
        with open('example1.txt', 'w') as file:
            file.write("Hello world\nPython programming")

        with open('example2.txt', 'w') as file:
            file.write("Learning Python\nis fun")

        test_cases = ['example1.txt', 'example2.txt']

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(user_code, {}, local_namespace)
                if 'file_operations' not in local_namespace or not callable(local_namespace['file_operations']):
                    return False, "代码错误：请定义函数 file_operations。"
            except Exception as e:
                return False, f"代码执行错误: {e}"

        file_operations_func = local_namespace['file_operations']

        for filename in test_cases:
            success, message = self.run_test(file_operations_func, filename)
            if not success:
                return False, message

        return True, "所有测试用例通过！"

    def teaching(self):
        return ("在这个关卡中，你需要学习如何操作文件。你需要定义一个函数，并在函数内使用文件操作方法。\n"
                "示例：\n"
                "def file_operations(filename):\n"
                "    with open(filename, 'r') as file:\n"
                "        content = file.read()\n"
                "        print(content)\n"
                "        file.seek(0)\n"
                "        lines = file.readlines()\n"
                "        for line in lines:\n"
                "            print(len(line))\n")

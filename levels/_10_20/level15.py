import ast
from levels.base_level import BaseLevel
import io
import contextlib

class Level15(BaseLevel):
    def description(self):
        return ("关卡15：文件读写\n"
                "任务：定义一个函数 file_read_write(filename, text)，该函数接收一个文件名 filename 和一个字符串 text。\n"
                "1. 将字符串 text 写入文件 filename 中。\n"
                "2. 读取文件 filename 的内容并打印出来。")

    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"代码执行错误：语法错误在第 {e.lineno} 行：{e.text.strip()}"

        function_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "file_read_write":
                function_found = True

        if not function_found:
            return False, "代码错误：请定义函数 file_read_write。"

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误：{e}"

        if 'file_read_write' not in local_namespace:
            return False, "代码错误：请定义函数 file_read_write。"
        if not callable(local_namespace['file_read_write']):
            return False, "代码错误：file_read_write 应该是一个函数。"

        return True, "代码检查通过！现在输入测试数据并运行代码。"

    def run_test(self, func, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                func(*args)
            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                return False, f"测试运行错误：{e}\n调用堆栈：\n{tb}"

        printed_output = output.getvalue().strip().split('\n')
        text = args[1]
        expected_output = [text]

        if printed_output != expected_output:
            return False, f"测试运行失败，请检查输出格式。当前输出：{printed_output}，预期输出：{expected_output}"

        return True, f"测试运行成功！当前输出：{printed_output}"

    def run_all_tests(self, user_code):
        test_cases = [
            ('level15_example1.txt', 'Hello, Python!'),
            ('level15_example2.txt', 'Learning Python is fun!'),
            ('level15_example3.txt', 'File operations in Python')
        ]

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(user_code, {}, local_namespace)
                if 'file_read_write' not in local_namespace or not callable(local_namespace['file_read_write']):
                    return False, "代码错误：请定义函数 file_read_write。"
            except Exception as e:
                return False, f"代码执行错误：{e}"

        file_read_write_func = local_namespace['file_read_write']

        all_messages = []
        for filename, text in test_cases:
            success, message = self.run_test(file_read_write_func, filename, text)
            all_messages.append(message)
            if not success:
                return False, '\n'.join(all_messages)

        return True, '\n'.join(all_messages)

    def teaching(self):
        return ("在这个关卡中，你需要学习如何进行文件读写操作。\n"
                "你需要定义一个函数，并在函数内使用文件读写操作方法。\n"
                "以下是一些步骤，帮助你完成任务：\n"
                "1. 打开文件进行写操作，并将字符串写入文件。\n"
                "2. 打开文件进行读操作，并读取文件内容。\n"
                "3. 打印读取的内容。\n"
                "你可以使用 open() 函数来完成文件的读写操作。试着将这些步骤实现到函数中，并运行代码来查看结果吧！")

    def answer(self):
        return ("def file_read_write(filename, text):\n"
                "    with open(filename, 'w') as file:\n"
                "        file.write(text)\n"
                "    with open(filename, 'r') as file:\n"
                "        content = file.read()\n"
                "        print(content)")

    def hint(self):
        return ("提示：你需要定义一个接收文件名和字符串参数的函数，并在函数内使用文件读写操作方法。\n"
                "1. 使用 open() 函数打开文件，并传入 'w' 模式写入字符串内容。\n"
                "2. 使用 open() 函数打开文件，并传入 'r' 模式读取文件内容并打印出来。")

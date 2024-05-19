import ast
from levels.base_level import BaseLevel
import io
import contextlib

class Level20(BaseLevel):
    def description(self):
        return ("关卡20：文件和JSON操作\n"
                "任务：定义一个函数 read_and_parse_json(filename)，该函数接收一个文件名 filename，并完成以下任务：\n"
                "1. 读取文件 filename 的内容，并将其解析为JSON对象。\n"
                "2. 打印JSON对象中的所有键值对。")

    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"代码执行错误: 语法错误在第 {e.lineno} 行: {e.text.strip()}"

        function_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "read_and_parse_json":
                function_found = True

        if not function_found:
            return False, "代码错误：请定义函数 read_and_parse_json。"

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误: {e}"

        if 'read_and_parse_json' not in local_namespace:
            return False, "代码错误：请定义函数 read_and_parse_json。"
        if not callable(local_namespace['read_and_parse_json']):
            return False, "代码错误：read_and_parse_json 应该是一个函数。"

        return True, "代码检查通过！现在输入测试数据并运行代码。"

    def run_test(self, func, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                func(*args)
            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                return False, f"测试运行错误: {e}\n调用堆栈:\n{tb}"

        printed_output = output.getvalue().strip().split('\n')
        expected_output = ["name: Alice", "age: 25", "city: New York"]

        if printed_output != expected_output:
            return False, f"测试运行失败，请检查输出格式。当前输出: {printed_output}。"

        return True, "测试运行成功！"

    def run_all_tests(self, user_code):
        test_cases = [
            'example1.json',
            'example2.json'
        ]

        # 预先创建测试用例文件
        with open('example1.json', 'w') as file:
            file.write('{"name": "Alice", "age": 25, "city": "New York"}')

        with open('example2.json', 'w') as file:
            file.write('{"name": "Bob", "age": 30, "city": "Los Angeles"}')

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(user_code, {}, local_namespace)
                if 'read_and_parse_json' not in local_namespace or not callable(local_namespace['read_and_parse_json']):
                    return False, "代码错误：请定义函数 read_and_parse_json。"
            except Exception as e:
                return False, f"代码执行错误: {e}"

        read_and_parse_json_func = local_namespace['read_and_parse_json']

        for filename in test_cases:
            success, message = self.run_test(read_and_parse_json_func, filename)
            if not success:
                return False, message

        return True, "所有测试用例通过！"

    def teaching(self):
        return ("在这个关卡中，你需要学习如何进行文件和JSON操作。你需要定义一个函数，并在函数内使用文件读写操作和JSON解析方法。\n"
                "例如，使用 open() 函数打开文件，使用 json.load() 方法解析JSON文件，并打印JSON对象中的键值对。")

    def answer(self):
        return ("import json\n\n"
                "def read_and_parse_json(filename):\n"
                "    with open(filename, 'r') as file:\n"
                "        data = json.load(file)\n"
                "        for key, value in data.items():\n"
                "            print(f'{key}: {value}')")

    def hint(self):
        return ("提示：你需要定义一个接收文件名参数的函数，并在函数内使用文件读写操作和JSON解析方法。\n"
                "例如，使用 open() 函数打开文件，使用 json.load() 方法解析JSON文件，并打印JSON对象中的键值对。")

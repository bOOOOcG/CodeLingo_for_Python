import ast
from levels.base_level import BaseLevel
import io
import contextlib

class Level7(BaseLevel):
    def description(self):
        return ("第七关：字典操作\n"
                "任务：定义一个函数 dict_operations(info)，该函数接收一个包含用户信息的字典 info。\n"
                "1. 打印字典中所有的键。\n"
                "2. 打印字典中所有的值。\n"
                "3. 打印字典中键为 name 的值。")

    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"代码执行错误: 语法错误在第 {e.lineno} 行: {e.text.strip()}"

        function_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "dict_operations":
                function_found = True

        if not function_found:
            return False, "代码错误：请定义函数 dict_operations。"

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误: {e}"

        if 'dict_operations' not in local_namespace:
            return False, "代码错误：请定义函数 dict_operations。"
        if not callable(local_namespace['dict_operations']):
            return False, "代码错误：dict_operations 应该是一个函数。"

        return True, "代码检查通过！现在输入测试数据并运行代码。"

    def run_test(self, func, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                func(*args)
            except Exception as e:
                return False, f"测试运行错误: {e}"

        printed_output = output.getvalue().strip().split('\n')
        info = args[0]
        expected_output = [str(list(info.keys())), str(list(info.values())), str(info['name'])]

        if printed_output != expected_output:
            return False, f"测试运行失败，请检查输出格式。当前输出: {printed_output}"

        return True, f"测试运行成功！当前输出: {printed_output}"

    def run_all_tests(self, user_code):
        test_cases = [
            {'name': 'Alice', 'age': 25, 'city': 'New York'},
            {'name': 'Bob', 'age': 30, 'city': 'Los Angeles'}
        ]

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(user_code, {}, local_namespace)
                if 'dict_operations' not in local_namespace or not callable(local_namespace['dict_operations']):
                    return False, "代码错误：请定义函数 dict_operations。"
            except Exception as e:
                return False, f"代码执行错误: {e}"

        dict_operations_func = local_namespace['dict_operations']

        for info in test_cases:
            success, message = self.run_test(dict_operations_func, info)
            if not success:
                return False, message

        return True, "所有测试用例通过！"

    def teaching(self):
        return ("在这个关卡中，你需要学习如何操作字典。你需要定义一个函数，并在函数内使用字典的方法和操作。\n"
                "例如，你可以使用 .keys() 方法获取字典的所有键，使用 .values() 方法获取字典的所有值，"
                "以及使用索引访问字典中具体键的值。")

    def answer(self):
        return ("def dict_operations(info):\n"
                "    print(info.keys())\n"
                "    print(info.values())\n"
                "    print(info['name'])")

    def hint(self):
        return ("提示：你需要定义一个接收字典参数的函数，并在函数内使用字典的方法。\n"
                "例如，使用 .keys() 方法获取字典的所有键，使用 .values() 方法获取字典的所有值，"
                "以及使用索引访问字典中具体键的值。")


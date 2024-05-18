import ast
from levels.base_level import BaseLevel
import io
import contextlib

class Level6(BaseLevel):
    def description(self):
        return ("第六关：列表操作\n"
                "任务：定义一个函数 list_operations(numbers)，该函数接收一个整数列表。\n"
                "1. 打印列表的长度。\n"
                "2. 打印列表的第一个元素和最后一个元素。\n"
                "3. 打印列表中所有偶数。")

    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"代码执行错误: 语法错误在第 {e.lineno} 行: {e.text.strip()}"

        function_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "list_operations":
                function_found = True
                has_for = any(isinstance(child, ast.For) for child in ast.walk(node))
                if not has_for:
                    return False, "代码错误：函数 list_operations 中缺少 for 循环。"

        if not function_found:
            return False, "代码错误：请定义函数 list_operations。"

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误: {e}"

        if 'list_operations' not in local_namespace:
            return False, "代码错误：请定义函数 list_operations。"
        if not callable(local_namespace['list_operations']):
            return False, "代码错误：list_operations 应该是一个函数。"

        return True, "代码检查通过！现在输入测试数据并运行代码。"

    def run_test(self, func, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                func(*args)
            except Exception as e:
                return False, f"测试运行错误: {e}"

        printed_output = output.getvalue().strip().split('\n')
        numbers = args[0]
        expected_output = [str(len(numbers))]
        expected_output.append(str(numbers[0]))
        expected_output.append(str(numbers[-1]))
        expected_output.extend([str(num) for num in numbers if num % 2 == 0])

        if printed_output != expected_output:
            return False, f"测试运行失败，请检查输出格式。当前输出: {printed_output}"

        return True, "测试运行成功！"

    def run_all_tests(self, user_code):
        test_cases = [
            ([1, 2, 3, 4, 5]),
            ([10, 15, 20, 25, 30]),
            ([2, 4, 6, 8, 10]),
            ([1, 3, 5, 7, 9]),
            ([11, 22, 33, 44, 55])
        ]

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(user_code, {}, local_namespace)
                if 'list_operations' not in local_namespace or not callable(local_namespace['list_operations']):
                    return False, "代码错误：请定义函数 list_operations。"
            except Exception as e:
                return False, f"代码执行错误: {e}"

        list_operations_func = local_namespace['list_operations']

        for numbers in test_cases:
            success, message = self.run_test(list_operations_func, numbers)
            if not success:
                return False, message

        return True, "所有测试用例通过！"

    def teaching(self):
        return ("在这个关卡中，你需要学习如何操作列表。你需要定义一个函数，并在函数内使用循环和列表操作。\n"
                "示例：\n"
                "def list_operations(numbers):\n"
                "    print(len(numbers))\n"
                "    print(numbers[0])\n"
                "    print(numbers[-1])\n"
                "    for num in numbers:\n"
                "        if num % 2 == 0:\n"
                "            print(num)\n")

import ast
from levels.base_level import BaseLevel
import io
import contextlib

class Level9(BaseLevel):
    def description(self):
        return ("第九关：列表和字典综合应用\n"
                "任务：定义一个函数 list_dict_operations(data)，该函数接收一个包含多个字典的列表 data。\n"
                "1. 打印每个人的信息，格式为 'name: age, city'。\n"
                "2. 打印所有人的名字。")

    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"代码执行错误: 语法错误在第 {e.lineno} 行: {e.text.strip()}"

        function_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "list_dict_operations":
                function_found = True

        if not function_found:
            return False, "代码错误：请定义函数 list_dict_operations。"

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误: {e}"

        if 'list_dict_operations' not in local_namespace:
            return False, "代码错误：请定义函数 list_dict_operations。"
        if not callable(local_namespace['list_dict_operations']):
            return False, "代码错误：list_dict_operations 应该是一个函数。"

        return True, "代码检查通过！现在输入测试数据并运行代码。"

    def run_test(self, func, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                func(*args)
            except Exception as e:
                return False, f"测试运行错误: {e}"

        printed_output = output.getvalue().strip().split('\n')
        data = args[0]
        expected_output = []
        for person in data:
            expected_output.append(f"{person['name']}: {person['age']}, {person['city']}")
        for person in data:
            expected_output.append(person['name'])

        if printed_output != expected_output:
            return False, f"测试运行失败，请检查输出格式。当前输出: {printed_output}"

        return True, f"测试运行成功！当前输出: {printed_output}"

    def run_all_tests(self, user_code):
        test_cases = [
            [
                {'name': 'Alice', 'age': 25, 'city': 'New York'},
                {'name': 'Bob', 'age': 30, 'city': 'Los Angeles'}
            ],
            [
                {'name': 'Charlie', 'age': 35, 'city': 'Chicago'},
                {'name': 'David', 'age': 40, 'city': 'Houston'}
            ]
        ]

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(user_code, {}, local_namespace)
                if 'list_dict_operations' not in local_namespace or not callable(local_namespace['list_dict_operations']):
                    return False, "代码错误：请定义函数 list_dict_operations。"
            except Exception as e:
                return False, f"代码执行错误: {e}"

        list_dict_operations_func = local_namespace['list_dict_operations']

        for data in test_cases:
            success, message = self.run_test(list_dict_operations_func, data)
            if not success:
                return False, message

        return True, "所有测试用例通过！"

    def teaching(self):
        return ("在这个关卡中，你需要综合运用列表和字典的操作。你需要定义一个函数，并在函数内使用循环和字典操作。\n"
                "例如，你可以使用 for 循环遍历列表，并在循环体内使用字典的方法获取字典的值。")

    def answer(self):
        return ("def list_dict_operations(data):\n"
                "    for person in data:\n"
                "        print(f\"{person['name']}: {person['age']}, {person['city']}\")\n"
                "    for person in data:\n"
                "        print(person['name'])")

    def hint(self):
        return ("提示：你需要定义一个接收包含字典的列表参数的函数，并在函数内使用循环和字典的方法。\n"
                "例如，使用 for 循环遍历列表，并在循环体内使用字典的方法获取字典的值。")


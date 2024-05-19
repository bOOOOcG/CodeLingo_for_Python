import ast
from levels.base_level import BaseLevel
import io
import contextlib

class Level14(BaseLevel):
    def description(self):
        return ("关卡14：嵌套数据结构\n"
                "任务：定义一个函数 nested_data_operations(data)，该函数接收一个包含嵌套字典和列表的数据结构 data。\n"
                "1. 打印第一个人的名字。\n"
                "2. 打印第二个人的年龄。\n"
                "3. 打印所有人的城市。\n"
                "如这样的字典{'name': 'Alice', 'age': 25, 'city': 'New York'}")

    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"代码执行错误：语法错误在第 {e.lineno} 行：{e.text.strip()}"

        function_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "nested_data_operations":
                function_found = True

        if not function_found:
            return False, "代码错误：请定义函数 nested_data_operations。"

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误：{e}"

        if 'nested_data_operations' not in local_namespace:
            return False, "代码错误：请定义函数 nested_data_operations。"
        if not callable(local_namespace['nested_data_operations']):
            return False, "代码错误：nested_data_operations 应该是一个函数。"

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
        data = args[0]
        expected_output = [data[0]['name'], str(data[1]['age'])]
        expected_output.extend([person['city'] for person in data])

        if printed_output != expected_output:
            return False, f"测试运行失败，请检查输出格式。当前输出：{printed_output}，预期输出：{expected_output}"

        return True, f"测试运行成功！当前输出：{printed_output}"

    def run_all_tests(self, user_code):
        test_cases = [
            [
                {'name': 'Alice', 'age': 25, 'city': 'New York'},
                {'name': 'Bob', 'age': 30, 'city': 'Los Angeles'},
                {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}
            ],
            [
                {'name': 'David', 'age': 40, 'city': 'Houston'},
                {'name': 'Eve', 'age': 45, 'city': 'San Francisco'},
                {'name': 'Frank', 'age': 50, 'city': 'Seattle'}
            ]
        ]

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(user_code, {}, local_namespace)
                if 'nested_data_operations' not in local_namespace or not callable(local_namespace['nested_data_operations']):
                    return False, "代码错误：请定义函数 nested_data_operations。"
            except Exception as e:
                return False, f"代码执行错误：{e}"

        nested_data_operations_func = local_namespace['nested_data_operations']

        all_messages = []
        for data in test_cases:
            success, message = self.run_test(nested_data_operations_func, data)
            all_messages.append(message)
            if not success:
                return False, '\n'.join(all_messages)

        return True, '\n'.join(all_messages)

    def teaching(self):
        return ("在这个关卡中，你需要学习如何操作嵌套数据结构。\n"
                "嵌套数据结构指的是包含其他数据结构的列表或字典。\n"
                "以下是一些示例，帮助你理解如何操作嵌套数据结构：\n"
                "1. 访问列表中的元素：使用索引，例如 data[0] 访问第一个元素。\n"
                "2. 访问字典中的值：使用键，例如 data[0]['name'] 访问第一个人的名字。\n"
                "3. 遍历列表中的所有元素：使用 for 循环\n"
                "通过这些操作，你可以轻松地从嵌套数据结构中提取信息。试着将这些步骤实现到函数中，并运行代码来查看结果吧！")

    def answer(self):
        return ("def nested_data_operations(data):\n"
                "    print(data[0]['name'])\n"
                "    print(data[1]['age'])\n"
                "    for person in data:\n"
                "        print(person['city'])")

    def hint(self):
        return ("提示：你需要定义一个接收嵌套数据结构参数的函数，并在函数内使用嵌套数据结构操作方法。\n"
                "1. 使用索引访问列表中的元素。例如，data[0] 访问第一个元素。\n"
                "2. 使用键访问字典中的值。例如，data[0]['name'] 访问第一个人的名字。\n"
                "3. 使用 for 循环遍历列表中的元素。例如，for person in data: print(person['city'])。")

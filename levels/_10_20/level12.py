import ast
from levels.base_level import BaseLevel
import io
import contextlib

class Level12(BaseLevel):
    def description(self):
        return ("关卡12：字典的高级操作\n"
                "任务：定义一个函数 advanced_dict_operations(info)，该函数接收一个包含用户信息的字典 info。\n"
                "1. 添加一个新的键值对 country: 'USA'。\n"
                "2. 更新键 age 的值为 30。\n"
                "3. 打印字典中所有的键值对。")

    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"代码执行错误: 语法错误在第 {e.lineno} 行: {e.text.strip()}"

        function_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "advanced_dict_operations":
                function_found = True

        if not function_found:
            return False, "代码错误：请定义函数 advanced_dict_operations。"

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误: {e}"

        if 'advanced_dict_operations' not in local_namespace:
            return False, "代码错误：请定义函数 advanced_dict_operations。"
        if not callable(local_namespace['advanced_dict_operations']):
            return False, "代码错误：advanced_dict_operations 应该是一个函数。"

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
        info = args[0]
        expected_output = [str(dict(info))]

        if printed_output != expected_output:
            return False, f"测试运行失败，请检查输出格式。当前输出: {printed_output}, 预期输出: {expected_output}"

        return True, f"测试运行成功！当前输出: {printed_output}"

    def run_all_tests(self, user_code):
        test_cases = [
            {'name': 'Alice', 'age': 25, 'city': 'New York'},
            {'name': 'Bob', 'age': 30, 'city': 'Los Angeles'},
            {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}
        ]

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(user_code, {}, local_namespace)
                if 'advanced_dict_operations' not in local_namespace or not callable(local_namespace['advanced_dict_operations']):
                    return False, "代码错误：请定义函数 advanced_dict_operations。"
            except Exception as e:
                return False, f"代码执行错误: {e}"

        advanced_dict_operations_func = local_namespace['advanced_dict_operations']

        all_messages = []
        for info in test_cases:
            success, message = self.run_test(advanced_dict_operations_func, info)
            all_messages.append(message)
            if not success:
                return False, '\n'.join(all_messages)

        return True, '\n'.join(all_messages)

    def teaching(self):
        return ("在这个关卡中，你需要学习如何操作字典。\n"
                "字典是一种包含键值对的数据结构，每个键都有一个对应的值。\n"
                "以下是你需要完成的步骤：\n"
                "1. 添加一个新的键值对：你可以通过将新键的名称放在方括号中，并为其赋值来添加一个新的键值对。例如，要添加键 'country' 并将其值设为 'USA'，你可以这样写：info['country'] = 'USA'。\n"
                "2. 更新现有键的值：你可以通过直接给现有键赋新值来更新它的值。例如，要将键 'age' 的值更新为 30，你可以这样写：info['age'] = 30。\n"
                "3. 打印字典中所有的键值对：你可以使用 dict() 函数将字典转换为字符串形式，然后使用 print() 函数打印出来。例如：print(dict(info))。\n"
                "通过这些操作，你可以轻松地管理和操作字典中的数据。试着将这些步骤实现到函数中，并运行代码来查看结果吧！")

    def answer(self):
        return ("def advanced_dict_operations(info):\n"
                "    info['country'] = 'USA'\n"
                "    info['age'] = 30\n"
                "    print(dict(info))")

    def hint(self):
        return ("提示：你需要定义一个接收字典参数的函数，并在函数内使用字典操作方法。\n"
                "1. 使用赋值语句添加新的键值对。例如，info['country'] = 'USA'。\n"
                "2. 使用赋值语句更新现有键的值。例如，info['age'] = 30。\n"
                "3. 使用 print(dict(info)) 打印字典中的所有键值对。")

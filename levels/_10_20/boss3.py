import ast
from levels.base_level import BaseLevel
import io
import contextlib

class Boss3(BaseLevel):
    def description(self):
        return ("Boss关3：综合应用\n"
                "任务：定义一个函数 ultimate_adventure(name, age, info, data, filename, text)，该函数接收六个参数，分别是名字、年龄、一个包含用户信息的字典、一个包含多个字典的列表、一个文件名和一个字符串。\n"
                "1. 根据年龄打印不同的信息（参考Boss1）。\n"
                "2. 打印字典 info 中键为 city 的值。\n"
                "3. 打印列表 data 中所有人的名字。\n"
                "4. 将字符串 text 写入文件 filename 中。\n"
                "5. 读取文件 filename 的内容并打印出来。\n"
                "示例数据：\n"
                "name = 'Alice', age = 20, info = {'name': 'Alice', 'age': 20, 'city': 'New York'},\n"
                "data = [{'name': 'Bob', 'age': 30, 'city': 'Los Angeles'}, {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}],\n"
                "filename = 'boss3_example1.txt', text = 'Hello, Python!'")

    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"代码执行错误：语法错误在第 {e.lineno} 行：{e.text.strip()}"

        function_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "ultimate_adventure":
                function_found = True

        if not function_found:
            return False, "代码错误：请定义函数 ultimate_adventure。"

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误：{e}"

        if 'ultimate_adventure' not in local_namespace:
            return False, "代码错误：请定义函数 ultimate_adventure。"
        if not callable(local_namespace['ultimate_adventure']):
            return False, "代码错误：ultimate_adventure 应该是一个函数。"

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
        name, age, info, data, filename, text = args
        expected_output = [f"欢迎，{name}，您是一名{'成年人' if age > 18 else '未成年人'}。", info['city']]
        expected_output.extend([person['name'] for person in data])
        expected_output.append(text)

        if printed_output != expected_output:
            return False, f"测试运行失败，请检查输出格式。当前输出：{printed_output}，预期输出：{expected_output}"

        return True, f"测试运行成功！当前输出：{printed_output}"

    def run_all_tests(self, user_code):
        test_cases = [
            ("Alice", 20, {'name': 'Alice', 'age': 20, 'city': 'New York'}, [{'name': 'Bob', 'age': 30, 'city': 'Los Angeles'}, {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}], 'boss3_example1.txt', 'Hello, Python!'),
            ("David", 17, {'name': 'David', 'age': 17, 'city': 'Houston'}, [{'name': 'Eve', 'age': 25, 'city': 'San Francisco'}, {'name': 'Frank', 'age': 28, 'city': 'Seattle'}], 'boss3_example2.txt', 'Learning Python is fun!')
        ]

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(user_code, {}, local_namespace)
                if 'ultimate_adventure' not in local_namespace or not callable(local_namespace['ultimate_adventure']):
                    return False, "代码错误：请定义函数 ultimate_adventure。"
            except Exception as e:
                return False, f"代码执行错误：{e}"

        ultimate_adventure_func = local_namespace['ultimate_adventure']

        all_messages = []
        for args in test_cases:
            success, message = self.run_test(ultimate_adventure_func, *args)
            all_messages.append(message)
            if not success:
                return False, '\n'.join(all_messages)

        return True, '\n'.join(all_messages)

    def teaching(self):
        return ("在这个关卡中，你需要综合运用前面所学的所有知识。\n"
                "你需要定义一个函数 ultimate_adventure，并在函数内使用条件语句、列表操作、字典操作和文件操作。\n"
                "1. 根据年龄打印不同的信息：使用 if 语句检查年龄，并打印相应的消息。\n"
                "2. 打印字典中的值：使用键访问字典中的值。\n"
                "3. 打印列表中的名字：使用 for 循环遍历列表，打印每个人的名字。\n"
                "4. 写入文件：使用 open() 函数以写模式打开文件，并将字符串写入文件。\n"
                "5. 读取文件：使用 open() 函数以读模式打开文件，并打印文件内容。\n"
                "通过这些操作，你可以完成综合应用的任务。")

    def answer(self):
        return ("def ultimate_adventure(name, age, info, data, filename, text):\n"
                "    if age > 18:\n"
                "        print(f'欢迎，{name}，您是一名成年人。')\n"
                "    else:\n"
                "        print(f'欢迎，{name}，您是一名未成年人。')\n"
                "    print(info['city'])\n"
                "    for person in data:\n"
                "        print(person['name'])\n"
                "    with open(filename, 'w') as file:\n"
                "        file.write(text)\n"
                "    with open(filename, 'r') as file:\n"
                "        content = file.read()\n"
                "        print(content)")

    def hint(self):
        return ("提示：你需要定义一个接收名字、年龄、字典、列表、文件名和字符串参数的函数，并在函数内使用条件语句、列表操作、字典操作和文件操作。\n"
                "1. 使用 if 语句判断年龄并打印相应的信息。\n"
                "2. 使用键访问字典中的值，并打印出来。\n"
                "3. 使用 for 循环遍历列表，并打印每个人的名字。\n"
                "4. 使用 open() 函数以写模式打开文件，并将字符串写入文件。\n"
                "5. 使用 open() 函数以读模式打开文件，并打印文件内容。")

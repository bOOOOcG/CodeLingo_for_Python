import ast
from levels.base_level import BaseLevel
import io
import contextlib

class Boss2(BaseLevel):
    def description(self):
        return ("Boss关2：综合应用\n"
                "任务：定义一个函数 comprehensive_adventure(name, age, info, data, filename)，该函数接收五个参数。\n"
                "1. 根据年龄打印不同的信息。\n"
                "2. 打印字典 info 中键为 city 的值。\n"
                "3. 打印列表 data 中所有人的名字。\n"
                "4. 读取文件 filename 的内容并打印出来。")

    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"代码执行错误: 语法错误在第 {e.lineno} 行: {e.text.strip()}"

        function_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "comprehensive_adventure":
                function_found = True

        if not function_found:
            return False, "代码错误：请定义函数 comprehensive_adventure。"

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误: {e}"

        if 'comprehensive_adventure' not in local_namespace:
            return False, "代码错误：请定义函数 comprehensive_adventure。"
        if not callable(local_namespace['comprehensive_adventure']):
            return False, "代码错误：comprehensive_adventure 应该是一个函数。"

        return True, "代码检查通过！现在输入测试数据并运行代码。"

    def run_test(self, func, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                func(*args)
            except Exception as e:
                return False, f"测试运行错误: {e}"

        printed_output = output.getvalue().strip().split('\n')
        name, age, info, data, filename = args
        with open(filename, 'r') as file:
            content = file.read().strip()

        expected_output = [
            f"欢迎，{name}，您是一名{'成年人' if age > 18 else '未成年人'}。",
            info['city']
        ]
        expected_output.extend([person['name'] for person in data])
        expected_output.append(content)

        if printed_output != expected_output:
            return False, f"测试运行失败，请检查输出格式。当前输出: {printed_output}"

        return True, "测试运行成功！"

    def run_all_tests(self, user_code):
        # 创建测试文件
        with open('example1.txt', 'w') as file:
            file.write("Hello world\nPython programming")

        with open('example2.txt', 'w') as file:
            file.write("Learning Python\nis fun")

        test_cases = [
            ('Alice', 20, {'name': 'Alice', 'age': 20, 'city': 'New York'},
             [{'name': 'Bob', 'age': 30, 'city': 'Los Angeles'}, {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}], 'example1.txt'),
            ('David', 17, {'name': 'David', 'age': 17, 'city': 'Houston'},
             [{'name': 'Eve', 'age': 25, 'city': 'San Francisco'}, {'name': 'Frank', 'age': 28, 'city': 'Seattle'}], 'example2.txt')
        ]

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(user_code, {}, local_namespace)
                if 'comprehensive_adventure' not in local_namespace or not callable(local_namespace['comprehensive_adventure']):
                    return False, "代码错误：请定义函数 comprehensive_adventure。"
            except Exception as e:
                return False, f"代码执行错误: {e}"

        comprehensive_adventure_func = local_namespace['comprehensive_adventure']

        for args in test_cases:
            success, message = self.run_test(comprehensive_adventure_func, *args)
            if not success:
                return False, message

        return True, "所有测试用例通过！"

    def teaching(self):
        return ("在这个关卡中，你需要综合运用前面所学的所有知识。你需要定义一个函数，并在函数内使用条件语句、字典和列表操作以及文件操作。\n"
                "首先，使用 if 语句根据年龄打印不同的信息。\n"
                "其次，使用字典方法获取键为 city 的值。\n"
                "然后，使用 for 循环遍历列表，打印每个人的名字。\n"
                "最后，使用文件操作方法读取并打印文件内容。")

    def answer(self):
        return ("def comprehensive_adventure(name, age, info, data, filename):\n"
                "    if age > 18:\n"
                "        print(f'欢迎，{name}，您是一名成年人。')\n"
                "    else:\n"
                "        print(f'欢迎，{name}，您是一名未成年人。')\n"
                "    print(info['city'])\n"
                "    for person in data:\n"
                "        print(person['name'])\n"
                "    with open(filename, 'r') as file:\n"
                "        print(file.read().strip())")

    def hint(self):
        return ("提示：你需要定义一个接收名字、年龄、字典、列表和文件名参数的函数。\n"
                "在函数内使用 if 语句判断年龄并打印相应的信息。\n"
                "使用字典方法获取并打印 city 的值。\n"
                "使用 for 循环遍历 data 列表并打印每个人的名字。\n"
                "使用 open() 函数打开文件并读取内容，然后打印出来。")

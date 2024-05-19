import ast
from levels.base_level import BaseLevel
import io
import contextlib

class Level17(BaseLevel):
    def description(self):
        return ("关卡17：类和对象\n"
                "任务：定义一个类 Person，该类具有以下属性和方法：\n"
                "1. 使用 __init__ 方法初始化 name 和 age 属性。\n"
                "2. 定义一个 greet 方法，打印 'Hello, my name is name'。")

    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"代码执行错误：语法错误在第 {e.lineno} 行：{e.text.strip()}"

        class_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == "Person":
                class_found = True

        if not class_found:
            return False, "代码错误：请定义类 Person。"

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误：{e}"

        if 'Person' not in local_namespace:
            return False, "代码错误：请定义类 Person。"

        return True, "代码检查通过！现在输入测试数据并运行代码。"

    def run_test(self, cls, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                obj = cls(*args)
                obj.greet()
            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                return False, f"测试运行错误：{e}\n调用堆栈：\n{tb}"

        printed_output = output.getvalue().strip().split('\n')
        name = args[0]
        expected_output = [f"Hello, my name is {name}"]

        if printed_output != expected_output:
            return False, f"测试运行失败，请检查输出格式。当前输出：{printed_output}，预期输出：{expected_output}"

        return True, f"测试运行成功！当前输出：{printed_output}"

    def run_all_tests(self, user_code):
        test_cases = [
            ("Alice", 25),
            ("Bob", 30),
            ("Charlie", 35),
            ("David", 40),
            ("Eve", 45)
        ]

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(user_code, {}, local_namespace)
                if 'Person' not in local_namespace:
                    return False, "代码错误：请定义类 Person。"
            except Exception as e:
                return False, f"代码执行错误：{e}"

        Person_cls = local_namespace['Person']

        all_messages = []
        for args in test_cases:
            success, message = self.run_test(Person_cls, *args)
            all_messages.append(message)
            if not success:
                return False, '\n'.join(all_messages)

        return True, '\n'.join(all_messages)

    def teaching(self):
        return ("在这个关卡中，你将学习如何定义类和创建对象。\n"
                "类是对象的蓝图或模板，定义了对象的属性和行为。\n"
                "你需要完成以下任务：\n"
                "1. 定义一个名为 Person 的类。\n"
                "2. 使用 __init__ 方法初始化类的属性 name 和 age。\n"
                "3. 定义一个 greet 方法，打印问候语。\n"
                "例如，如果 name 为 'Alice'，greet 方法应该打印 'Hello, my name is Alice'。")

    def answer(self):
        return ("class Person:\n"
                "    def __init__(self, name, age):\n"
                "        self.name = name\n"
                "        self.age = age\n"
                "    def greet(self):\n"
                "        print(f'Hello, my name is {self.name}')")

    def hint(self):
        return ("提示：你需要定义一个类，并在类内定义初始化方法和其他方法。\n"
                "1. 使用 __init__ 方法初始化类的属性 name 和 age。\n"
                "2. 定义一个 greet 方法，打印 'Hello, my name is name'。\n"
                "例如：\n"
                "class Person:\n"
                "    def __init__(self, name, age):\n"
                "        self.name = name\n"
                "        self.age = age\n"
                "    def greet(self):\n"
                "        print(f'Hello, my name is {self.name}')")

import ast
from levels.base_level import BaseLevel
import io
import contextlib

class Level18(BaseLevel):
    def description(self):
        return ("关卡18：继承\n"
                "任务：定义一个类 Student, 继承自 Person 类, 具有以下属性和方法：\n"
                "1. 使用 __init__ 方法初始化 name、age 和 student_id 属性。\n"
                "2. 重写 greet 方法, 打印 'Hello, my name is name and my student ID is student_id'。")

    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"代码执行错误：语法错误在第 {e.lineno} 行：{e.text.strip()}"

        class_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == "Student":
                class_found = True

        if not class_found:
            return False, "代码错误：请定义类 Student。"

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误：{e}"

        if 'Student' not in local_namespace:
            return False, "代码错误：请定义类 Student。"

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
        name, age, student_id = args
        expected_output = [f"Hello, my name is {name} and my student ID is {student_id}"]

        if printed_output != expected_output:
            return False, f"测试运行失败, 请检查输出格式。当前输出：{printed_output}, 预期输出：{expected_output}"

        return True, f"测试运行成功！当前输出：{printed_output}"

    def run_all_tests(self, user_code):
        test_cases = [
            ("Alice", 25, "S12345"), 
            ("Bob", 30, "S67890"), 
            ("Charlie", 35, "S11223"), 
            ("David", 40, "S44556"), 
            ("Eve", 45, "S77889")
        ]

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(user_code, {}, local_namespace)
                if 'Student' not in local_namespace:
                    return False, "代码错误：请定义类 Student。"
            except Exception as e:
                return False, f"代码执行错误：{e}"

        Student_cls = local_namespace['Student']

        all_messages = []
        for args in test_cases:
            success, message = self.run_test(Student_cls, *args)
            all_messages.append(message)
            if not success:
                return False, '\n'.join(all_messages)

        return True, '\n'.join(all_messages)

    def teaching(self):
        return ("在这个关卡中, 你将学习如何定义类的继承。\n"
                "继承是面向对象编程中的一个重要概念, 它允许一个类继承另一个类的属性和方法。\n"
                "你需要完成以下任务：\n"
                "1. 定义一个名为 Student 的类, 继承自 Person 类。\n"
                "2. 使用 __init__ 方法初始化 name、age 和 student_id 属性。\n"
                "3. 重写 greet 方法, 打印问候语和学号。\n"
                "例如, 如果 name 为 'Alice', student_id 为 'S12345', greet 方法应该打印 'Hello, my name is Alice and my student ID is S12345'。")

    def answer(self):
        return ("class Person:\n"
                "    def __init__(self, name, age):\n"
                "        self.name = name\n"
                "        self.age = age\n"
                "    def greet(self):\n"
                "        print(f'Hello, my name is {self.name}')\n\n"
                "class Student(Person):\n"
                "    def __init__(self, name, age, student_id):\n"
                "        super().__init__(name, age)\n"
                "        self.student_id = student_id\n"
                "    def greet(self):\n"
                "        print(f'Hello, my name is {self.name} and my student ID is {self.student_id}')")

    def hint(self):
        return ("提示：你需要定义一个继承自其他类的新类, 并在新类内重写方法。\n"
                "1. 定义一个类 Student 继承自 Person 类。\n"
                "2. 使用 __init__ 方法初始化 name、age 和 student_id 属性。\n"
                "3. 重写 greet 方法, 打印 'Hello, my name is name and my student ID is student_id'。\n"
                "例如：\n"
                "class Person:\n"
                "    def __init__(self, name, age):\n"
                "        self.name = name\n"
                "        self.age = age\n"
                "    def greet(self):\n"
                "        print(f'Hello, my name is {self.name}')\n\n"
                "class Student(Person):\n"
                "    def __init__(self, name, age, student_id):\n"
                "        super().__init__(name, age)\n"
                "        self.student_id = student_id\n"
                "    def greet(self):\n"
                "        print(f'Hello, my name is {self.name} and my student ID is {self.student_id}')")

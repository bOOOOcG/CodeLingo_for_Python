import ast
from levels.base_level import BaseLevel
import io
import contextlib

class Boss4(BaseLevel):
    def description(self):
        return ("Boss关4：综合应用\n"
                "任务：定义一个函数 final_adventure(name, age, student_id, data, json_filename, text)，该函数接收六个参数，分别是名字、年龄、学生ID、一个包含多个字典的列表、一个JSON文件名和一个字符串。\n"
                "1. 根据年龄打印不同的信息（参考Boss1）。\n"
                "2. 使用继承定义一个 Student 类，并重写 greet 方法，打印 'Hello, my name is name and my student ID is student_id'。\n"
                "3. 使用 Student 类的实例调用 greet 方法。\n"
                "4. 打印列表 data 中所有人的名字。\n"
                "5. 将字符串 text 写入JSON文件 json_filename 中，读取并打印JSON文件的内容。")

    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"代码执行错误: 语法错误在第 {e.lineno} 行: {e.text.strip()}"

        function_found = False
        class_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "final_adventure":
                function_found = True
            if isinstance(node, ast.ClassDef) and node.name == "Student":
                class_found = True

        if not function_found:
            return False, "代码错误：请定义函数 final_adventure。"
        if not class_found:
            return False, "代码错误：请定义类 Student。"

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误: {e}"

        if 'final_adventure' not in local_namespace:
            return False, "代码错误：请定义函数 final_adventure。"
        if 'Student' not in local_namespace:
            return False, "代码错误：请定义类 Student。"

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
        name, age, student_id, data, json_filename, text = args
        expected_output = [f"欢迎，{name}，您是一名{'成年人' if age > 18 else '未成年人'}。", 
                           f"Hello, my name is {name} and my student ID is {student_id}"]
        expected_output.extend([person['name'] for person in data])
        expected_output.append(f"text: {text}")

        if printed_output != expected_output:
            return False, f"测试运行失败，请检查输出格式。当前输出: {printed_output}。"

        return True, "测试运行成功！"

    def run_all_tests(self, user_code):
        test_cases = [
            ("Alice", 20, "S12345", [{'name': 'Bob', 'age': 30, 'city': 'Los Angeles'}, {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}], 'example1_boss4.json', 'Hello, final adventure!'),
            ("David", 17, "S67890", [{'name': 'Eve', 'age': 25, 'city': 'San Francisco'}, {'name': 'Frank', 'age': 28, 'city': 'Seattle'}], 'example2_boss4.json', 'Learning Python is fun!')
        ]

        # 预先创建测试用例文件
        with open('example1_boss4.json', 'w') as file:
            file.write('{"text": "Hello, final adventure!"}')

        with open('example2_boss4.json', 'w') as file:
            file.write('{"text": "Learning Python is fun!"}')

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(user_code, {}, local_namespace)
                if 'final_adventure' not in local_namespace or not callable(local_namespace['final_adventure']):
                    return False, "代码错误：请定义函数 final_adventure。"
                if 'Student' not in local_namespace:
                    return False, "代码错误：请定义类 Student。"
            except Exception as e:
                return False, f"代码执行错误: {e}"

        final_adventure_func = local_namespace['final_adventure']

        for args in test_cases:
            success, message = self.run_test(final_adventure_func, *args)
            if not success:
                return False, message

        return True, "所有测试用例通过！"

    def teaching(self):
        return ("在这个Boss关中，你需要综合运用前面所学的所有知识。你需要定义一个函数 final_adventure，并在函数内使用类和继承、文件和JSON操作等。\n"
                "例如，定义 Student 类继承自 Person 类，并在 final_adventure 函数中实例化 Student 对象，调用其 greet 方法，"
                "然后操作文件，将字符串写入JSON文件，并读取和打印JSON文件的内容。")

    def answer(self):
        return ("import json\n\n"
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
                "        print(f'Hello, my name is {self.name} and my student ID is {self.student_id}')\n\n"
                "def final_adventure(name, age, student_id, data, json_filename, text):\n"
                "    if age > 18:\n"
                "        print(f'欢迎，{name}，您是一名成年人。')\n"
                "    else:\n"
                "        print(f'欢迎，{name}，您是一名未成年人。')\n"
                "    student = Student(name, age, student_id)\n"
                "    student.greet()\n"
                "    for person in data:\n"
                "        print(person['name'])\n"
                "    with open(json_filename, 'w') as file:\n"
                "        json.dump({'text': text}, file)\n"
                "    with open(json_filename, 'r') as file:\n"
                "        json_data = json.load(file)\n"
                "        for key, value in json_data.items():\n"
                "            print(f'{key}: {value}')")

    def hint(self):
        return ("提示：你需要定义一个函数 final_adventure，并在函数内使用类和继承、文件和JSON操作等。\n"
                "例如，定义 Student 类继承自 Person 类，并在 final_adventure 函数中实例化 Student 对象，调用其 greet 方法，"
                "然后操作文件，将字符串写入JSON文件，并读取和打印JSON文件的内容。")

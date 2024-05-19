import ast
from levels.base_level import BaseLevel
import io
import contextlib
import tempfile
import os

class Level19(BaseLevel):
    def description(self):
        return ("关卡19：模块和包\n"
                "任务：定义一个模块 math_utils，包含以下函数：\n"
                "1. add(a, b) 返回 a 和 b 的和。\n"
                "2. subtract(a, b) 返回 a 减去 b 的结果。\n"
                "你需要创建一个名为 math_utils.py 的文件，并在其中定义上述函数。\n"
                "然后在一个名为 main.py 的文件中导入这些函数，并调用它们来进行测试。\n"
                "在代码中使用 # math_utils.py 和 # main.py 作为标记来分隔模块代码和主程序代码。")

    def parse_code(self, code):
        files = {}
        current_file = None

        for line in code.split('\n'):
            if line.strip().startswith('#'):
                current_file = line.strip()[1:].strip()
                files[current_file] = []
            elif current_file:
                files[current_file].append(line)

        for key in files:
            files[key] = '\n'.join(files[key])

        return files

    def check_code(self, code):
        files = self.parse_code(code)
        
        if 'math_utils.py' not in files or 'main.py' not in files:
            return False, "代码错误：请确保定义了 math_utils.py 和 main.py 文件。"

        try:
            tree = ast.parse(files['math_utils.py'])
        except SyntaxError as e:
            return False, f"代码执行错误：math_utils.py 语法错误在第 {e.lineno} 行：{e.text.strip()}"

        function_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and (node.name == "add" or node.name == "subtract"):
                function_found = True

        if not function_found:
            return False, "代码错误：请定义函数 add 和 subtract。"

        return True, "代码检查通过！现在输入测试数据并运行代码。"

    def run_test(self, func_name, a, b, expected_result):
        try:
            func = self.local_namespace[func_name]
            result = func(a, b)
            if result != expected_result:
                return False, f"测试运行失败：函数 {func_name}({a}, {b}) 的返回结果是 {result}，但预期结果是 {expected_result}。"
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            return False, f"测试运行错误：{e}\n调用堆栈：\n{tb}"

        return True, "测试运行成功！"

    def run_all_tests(self, user_code):
        files = self.parse_code(user_code)

        if 'math_utils.py' not in files or 'main.py' not in files:
            return False, "代码错误：请确保定义了 math_utils.py 和 main.py 文件。"

        with tempfile.TemporaryDirectory() as temp_dir:
            math_utils_path = os.path.join(temp_dir, 'math_utils.py')
            main_path = os.path.join(temp_dir, 'main.py')

            with open(math_utils_path, 'w') as f:
                f.write(files['math_utils.py'])

            with open(main_path, 'w') as f:
                f.write(files['main.py'])

            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                try:
                    exec(open(main_path).read(), {'__name__': '__main__', '__file__': main_path})
                except Exception as e:
                    return False, f"代码执行错误：{e}"

            printed_output = output.getvalue().strip().split('\n')
            expected_output = ["15", "5", "0", "-3"]

            if printed_output != expected_output:
                return False, f"测试运行失败，请检查输出格式。当前输出：{printed_output}，预期输出：{expected_output}"

        return True, "所有测试用例通过！"

    def teaching(self):
        return ("在这个关卡中，你需要学习如何定义和使用模块。\n"
                "模块是包含相关函数、类和变量的文件，可以在其他文件中导入和使用这些内容。\n"
                "你需要完成以下任务：\n"
                "1. 创建一个名为 math_utils.py 的文件，定义 add 和 subtract 函数。\n"
                "2. 在 add 函数中，返回两个参数 a 和 b 的和。\n"
                "3. 在 subtract 函数中，返回两个参数 a 和 b 的差。\n"
                "4. 创建一个名为 main.py 的文件，使用 from ... import ... 语句导入 add 和 subtract 函数。\n"
                "5. 调用这些函数并打印结果。\n"
                "通过这种方式，你可以将功能分离到不同的模块中，使代码更加组织化和易于维护。\n"
                "在代码中使用 # math_utils.py 和 # main.py 作为标记来分隔模块代码和主程序代码。")

    def answer(self):
        return ("# math_utils.py\n"
                "def add(a, b):\n"
                "    return a + b\n\n"
                "def subtract(a, b):\n"
                "    return a - b\n\n"
                "# main.py\n"
                "from math_utils import add, subtract\n\n"
                "print(add(10, 5))\n"
                "print(subtract(10, 5))\n"
                "print(add(-3, 3))\n"
                "print(subtract(7, 10))")

    def hint(self):
        return ("提示：你需要定义一个包含函数的模块，并在其他文件中导入和调用这些函数。\n"
                "1. 创建一个名为 math_utils 的模块，定义 add 和 subtract 函数。\n"
                "2. 使用 from ... import ... 语句在主程序中导入这些函数，并调用它们。\n"
                "例如：\n"
                "# math_utils.py\n"
                "def add(a, b):\n"
                "    return a + b\n"
                "def subtract(a, b):\n"
                "    return a - b\n"
                "# main.py\n"
                "from math_utils import add, subtract\n"
                "print(add(10, 5))\n"
                "print(subtract(10, 5))\n"
                "print(add(-3, 3))\n"
                "print(subtract(7, 10))")

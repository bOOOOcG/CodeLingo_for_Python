import ast
from levels.base_level import BaseLevel
import io
import contextlib

class Level13(BaseLevel):
    def description(self):
        return ("关卡13：字符串的高级操作\n"
                "任务：定义一个函数 advanced_string_operations(text)，该函数接收一个字符串 text。\n"
                "1. 将字符串转换为大写并打印。\n"
                "2. 检查字符串是否以 'Hello' 开头，如果是则打印 'Greeting detected'。\n"
                "3. 替换字符串中的空格为下划线并打印。")

    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"代码执行错误: 语法错误在第 {e.lineno} 行: {e.text.strip()}"

        function_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "advanced_string_operations":
                function_found = True

        if not function_found:
            return False, "代码错误：请定义函数 advanced_string_operations。"

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误: {e}"

        if 'advanced_string_operations' not in local_namespace:
            return False, "代码错误：请定义函数 advanced_string_operations。"
        if not callable(local_namespace['advanced_string_operations']):
            return False, "代码错误：advanced_string_operations 应该是一个函数。"

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
        text = args[0]
        expected_output = [text.upper()]
        if text.startswith("Hello"):
            expected_output.append("Greeting detected")
        expected_output.append(text.replace(" ", "_"))

        if printed_output != expected_output:
            return False, f"测试运行失败，请检查输出格式。当前输出: {printed_output}，预期输出: {expected_output}"

        return True, f"测试运行成功！当前输出: {printed_output}"

    def run_all_tests(self, user_code):
        test_cases = [
            "Hello world from Python",
            "Learning Python is fun",
            "Goodbye world",
            "Hello again",
            "Python programming"
        ]

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(user_code, {}, local_namespace)
                if 'advanced_string_operations' not in local_namespace or not callable(local_namespace['advanced_string_operations']):
                    return False, "代码错误：请定义函数 advanced_string_operations。"
            except Exception as e:
                return False, f"代码执行错误: {e}"

        advanced_string_operations_func = local_namespace['advanced_string_operations']

        all_messages = []
        for text in test_cases:
            success, message = self.run_test(advanced_string_operations_func, text)
            all_messages.append(message)
            if not success:
                return False, '\n'.join(all_messages)

        return True, '\n'.join(all_messages)

    def teaching(self):
        return ("在这个关卡中，你需要学习如何操作字符串。\n"
                "你需要定义一个函数，并在函数内使用字符串操作方法。\n"
                "下面是一些步骤和示例，帮助你完成任务：\n"
                "1. 将字符串转换为大写：使用 upper() 方法。例如，如果 text 是 'Hello'，则 text.upper() 会返回 'HELLO'。\n"
                "2. 检查字符串是否以特定前缀开头：使用 startswith() 方法。例如，如果 text 是 'Hello'，则 text.startswith('Hello') 会返回 True。\n"
                "3. 替换字符串中的子字符串：使用 replace() 方法。例如，如果 text 是 'Hello world'，则 text.replace(' ', '_') 会返回 'Hello_world'。\n"
                "通过这些操作，你可以轻松地处理字符串。试着将这些步骤实现到函数中，并运行代码来查看结果吧！")

    def answer(self):
        return ("def advanced_string_operations(text):\n"
                "    print(text.upper())\n"
                "    if text.startswith('Hello'):\n"
                "        print('Greeting detected')\n"
                "    print(text.replace(' ', '_'))")

    def hint(self):
        return ("提示：你需要定义一个接收字符串参数的函数，并在函数内使用字符串操作方法。\n"
                "例如，使用 upper() 方法将字符串转换为大写，使用 startswith() 方法检查字符串是否以特定前缀开头，"
                "以及使用 replace() 方法替换字符串中的子字符串。")

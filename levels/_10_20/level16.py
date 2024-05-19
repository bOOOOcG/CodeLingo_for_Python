import ast
from levels.base_level import BaseLevel
import io
import contextlib

class Level16(BaseLevel):
    def description(self):
        return ("关卡16：异常处理\n"
                "任务：定义一个函数 safe_divide(a, b)，该函数接收两个参数 a 和 b。\n"
                "1. 尝试计算 a 除以 b 的结果并打印。\n"
                "2. 如果发生除零错误，打印 'Division by zero error'。")

    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"代码执行错误：语法错误在第 {e.lineno} 行：{e.text.strip()}"

        function_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "safe_divide":
                function_found = True

        if not function_found:
            return False, "代码错误：请定义函数 safe_divide。"

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误：{e}"

        if 'safe_divide' not in local_namespace:
            return False, "代码错误：请定义函数 safe_divide。"
        if not callable(local_namespace['safe_divide']):
            return False, "代码错误：safe_divide 应该是一个函数。"

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
        a, b = args
        if b == 0:
            expected_output = ["Division by zero error"]
        else:
            expected_output = [str(a / b)]

        if printed_output != expected_output:
            return False, f"测试运行失败，请检查输出格式。当前输出：{printed_output}，预期输出：{expected_output}"

        return True, f"测试运行成功！当前输出：{printed_output}"

    def run_all_tests(self, user_code):
        test_cases = [
            (10, 2),
            (10, 0),
            (20, 5),
            (30, 3),
            (50, 10)
        ]

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(user_code, {}, local_namespace)
                if 'safe_divide' not in local_namespace or not callable(local_namespace['safe_divide']):
                    return False, "代码错误：请定义函数 safe_divide。"
            except Exception as e:
                return False, f"代码执行错误：{e}"

        safe_divide_func = local_namespace['safe_divide']

        all_messages = []
        for args in test_cases:
            success, message = self.run_test(safe_divide_func, *args)
            all_messages.append(message)
            if not success:
                return False, '\n'.join(all_messages)

        return True, '\n'.join(all_messages)

    def teaching(self):
        return ("在这个关卡中，你需要学习如何处理异常。\n"
                "异常处理是指在程序运行过程中，处理可能会发生的错误情况，防止程序崩溃。\n"
                "你需要定义一个函数，并在函数内使用 try 和 except 块处理除零错误。\n"
                "1. 使用 try 块尝试执行可能会引发错误的代码。\n"
                "2. 使用 except 块捕获特定的异常，并进行相应的处理。\n"
                "在这个任务中，你将尝试进行除法运算，并捕获 ZeroDivisionError 异常。\n"
                "试着在代码中实现这些步骤，并运行测试来查看结果。")

    def answer(self):
        return ("def safe_divide(a, b):\n"
                "    try:\n"
                "        result = a / b\n"
                "        print(result)\n"
                "    except ZeroDivisionError:\n"
                "        print('Division by zero error')")

    def hint(self):
        return ("提示：你需要定义一个接收两个参数的函数，并在函数内使用 try 和 except 块处理除零错误。\n"
                "1. 使用 try 块尝试计算 a 除以 b 的结果。\n"
                "2. 使用 except 块捕获 ZeroDivisionError 并打印错误信息。")

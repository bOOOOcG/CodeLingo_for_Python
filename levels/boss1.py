import ast
from levels.base_level import BaseLevel
import io
import contextlib

class Boss1(BaseLevel):
    def description(self):
        return ("Boss关1：综合应用\n"
                "任务：定义一个函数 adventure(name, age, height)，该函数接收三个参数：名字、年龄和身高。\n"
                "如果年龄大于18，打印“欢迎，name，您是一名成年人。”，否则打印“欢迎，name，您是一名未成年人。”。\n"
                "接着，使用 for 循环打印从 1 到 age 之间的所有数字。\n"
                "然后在函数中检查 height 是否大于 1.70，"
                "如果是则打印 '你很高'，否则打印 '你不高'。")

    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"代码执行错误: 语法错误在第 {e.lineno} 行: {e.text.strip()}"

        function_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "adventure":
                function_found = True
                has_for = any(isinstance(child, ast.For) for child in ast.walk(node))
                has_if = any(isinstance(child, ast.If) for child in ast.walk(node))
                if not has_for:
                    return False, "代码错误：函数 adventure 中缺少 for 循环。"
                if not has_if:
                    return False, "代码错误：函数 adventure 中缺少 if 语句。"

        if not function_found:
            return False, "代码错误：请定义函数 adventure。"

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误: {e}"

        if 'adventure' not in local_namespace:
            return False, "代码错误：请定义函数 adventure。"
        if not callable(local_namespace['adventure']):
            return False, "代码错误：adventure 应该是一个函数。"

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
        name, age, height = args
        expected_output = [f"欢迎，{name}，您是一名{'成年人' if age > 18 else '未成年人'}。"]
        expected_output.extend([str(i) for i in range(1, age + 1)])
        if height > 1.70:
            expected_output.append("你很高")
        else:
            expected_output.append("你不高")

        if printed_output != expected_output:
            if printed_output[0] != expected_output[0]:
                reason = ("年龄判断错误。" if '成年人' in printed_output[0] else "未成年人判断错误。")
                return False, f"测试运行失败，请检查输出格式。当前输出: {printed_output}。{reason}"
            else:
                return False, f"测试运行失败，请检查 for 循环和 height 的判断是否正确。当前输出: {printed_output}"

        return True, "测试运行成功！"

    def run_all_tests(self, user_code):
        test_cases = [
            ("Alice", 20, 1.80),
            ("Bob", 16, 1.65),
            ("Charlie", 18, 1.75),
            ("David", 5, 1.50),
            ("Eve", 21, 1.85)
        ]

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(user_code, {}, local_namespace)
                if 'adventure' not in local_namespace or not callable(local_namespace['adventure']):
                    return False, "代码错误：请定义函数 adventure。"
            except Exception as e:
                return False, f"代码执行错误: {e}"

        adventure_func = local_namespace['adventure']

        for name, age, height in test_cases:
            success, message = self.run_test(adventure_func, name, age, height)
            if not success:
                return False, message

        return True, "所有测试用例通过！"

    def teaching(self):
        return ("在这个关卡中，你需要综合运用前面所学的所有知识。你需要定义一个函数 adventure，并在函数内使用条件语句和循环。\n"
                "你可以通过 if 语句检查年龄，并使用 for 循环打印一系列数字。\n"
                "此外，你还需要定义一个变量来检查身高，并根据条件打印相应的信息。")

    def answer(self):
        return ("def adventure(name, age, height):\n"
                "    if age > 18:\n"
                "        print(f'欢迎，{name}，您是一名成年人。')\n"
                "    else:\n"
                "        print(f'欢迎，{name}，您是一名未成年人。')\n"
                "    for i in range(1, age + 1):\n"
                "        print(i)\n"
                "    if height > 1.70:\n"
                "        print('你很高')\n"
                "    else:\n"
                "        print('你不高')")

    def hint(self):
        return ("提示：你需要定义一个接收名字、年龄和身高参数的函数，并在函数内使用条件语句和循环。\n"
                "例如，使用 if 语句判断年龄，使用 for 循环打印从 1 到年龄的所有数字，并使用 if 语句判断身高。")


import ast
from levels.base_level import BaseLevel
import io
import contextlib

class Level11(BaseLevel):
    def description(self):
        return ("关卡11：列表的高级操作\n"
                "任务：定义一个函数 advanced_list_operations(numbers)，该函数接收一个整数列表 numbers。\n"
                "1. 将列表按升序排序并打印排序后的列表。\n"
                "2. 打印列表中最大值和最小值。\n"
                "3. 计算并打印列表中所有元素的平均值。")

    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"代码执行错误: 语法错误在第 {e.lineno} 行: {e.text.strip()}"

        function_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "advanced_list_operations":
                function_found = True

        if not function_found:
            return False, "代码错误：请定义函数 advanced_list_operations。"

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误: {e}"

        if 'advanced_list_operations' not in local_namespace:
            return False, "代码错误：请定义函数 advanced_list_operations。"
        if not callable(local_namespace['advanced_list_operations']):
            return False, "代码错误：advanced_list_operations 应该是一个函数。"

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
        numbers = args[0]
        sorted_numbers = sorted(numbers)
        expected_output = [str(sorted_numbers), str(max(numbers)), str(min(numbers)), str(sum(numbers) / len(numbers))]

        if printed_output != expected_output:
            return False, f"测试运行失败，请检查输出格式。当前输出: {printed_output}。"

        return True, "测试运行成功！"

    def run_all_tests(self, user_code):
        test_cases = [
            [3, 1, 4, 1, 5, 9, 2, 6, 5],
            [10, 15, 20, 25, 30],
            [2, 4, 6, 8, 10],
            [1, 3, 5, 7, 9],
            [11, 22, 33, 44, 55]
        ]

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(user_code, {}, local_namespace)
                if 'advanced_list_operations' not in local_namespace or not callable(local_namespace['advanced_list_operations']):
                    return False, "代码错误：请定义函数 advanced_list_operations。"
            except Exception as e:
                return False, f"代码执行错误: {e}"

        advanced_list_operations_func = local_namespace['advanced_list_operations']

        for numbers in test_cases:
            success, message = self.run_test(advanced_list_operations_func, numbers)
            if not success:
                return False, message

        return True, "所有测试用例通过！"

    def teaching(self):
        return ("在这个关卡中，你需要学习如何操作列表。你需要定义一个函数，并在函数内使用列表操作方法。\n"
                "例如，使用 sort() 方法对列表进行排序，使用 max() 和 min() 函数获取列表的最大值和最小值，"
                "以及使用 sum() 和 len() 函数计算列表元素的平均值。")

    def answer(self):
        return ("def advanced_list_operations(numbers):\n"
                "    numbers.sort()\n"
                "    print(numbers)\n"
                "    print(max(numbers))\n"
                "    print(min(numbers))\n"
                "    average = sum(numbers) / len(numbers)\n"
                "    print(average)")

    def hint(self):
        return ("提示：你需要定义一个接收整数列表参数的函数，并在函数内使用列表操作方法。\n"
                "例如，使用 sort() 方法对列表进行排序，使用 max() 和 min() 函数获取列表的最大值和最小值，"
                "以及使用 sum() 和 len() 函数计算列表元素的平均值。")

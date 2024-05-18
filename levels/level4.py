from levels.base_level import BaseLevel
import io
import contextlib

class Level4(BaseLevel):
    def description(self):
        return "第四关：循环\n任务：使用 for 循环打印从 1 到 10 的所有数字。"

    def check_code(self, code):
        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误: {e}"

        printed_output = output.getvalue().strip().split()
        expected_output = [str(i) for i in range(1, 11)]
        if printed_output == expected_output:
            return True, "成功打印出 1 到 10 的所有数字！"
        else:
            return False, f"代码错误，请使用 for 循环打印从 1 到 10 的所有数字。当前输出: {printed_output}"

    def teaching(self):
        return ("循环用于重复执行一段代码。在 Python 中，可以使用 for 关键字编写 for 循环。例如：\n"
                "for 变量 in 范围:\n"
                "    # 执行的代码块\n"
                "for 循环会遍历指定范围内的每一个值，并在每次迭代时执行代码块中的代码。")

    def answer(self):
        return ("for i in range(1, 11):\n"
                "    print(i)")

    def hint(self):
        return ("提示：使用 for 循环和 range 函数。\n"
                "例如，for i in range(1, 11) 可以生成从 1 到 10 的数字。\n"
                "在循环体中使用 print(i) 来打印每个数字。")

    def run_all_tests(self, user_code):
        return self.check_code(user_code)

from levels.base_level import BaseLevel
import io
import contextlib

class Level4(BaseLevel):
    def description(self):
        return "第四关：循环\n任务：使用for循环打印从1到10的所有数字。"

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
            return True, "成功打印出1到10的所有数字！"
        else:
            return False, f"代码错误，请使用for循环打印从1到10的所有数字。当前输出: {printed_output}"

    def teaching(self):
        return "循环用于重复执行一段代码。使用 for 关键字可以编写 for 循环。例如：\nfor i in range(1, 11):\n    print(i)\n这段代码会打印出从 1 到 10 的所有数字。"

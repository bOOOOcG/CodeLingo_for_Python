from levels.base_level import BaseLevel
import io
import contextlib

class Level3(BaseLevel):
    def description(self):
        return "第三关：条件语句\n任务：定义一个变量age，并将其值设为一个整数，然后使用if语句检查age是否大于18，如果是则打印'成年人'，否则打印'未成年人'。"

    def check_code(self, code):
        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误: {e}"

        if 'age' not in local_namespace:
            return False, "代码错误：请定义变量 'age'。"
        if not isinstance(local_namespace['age'], int):
            return False, "代码错误：变量 'age' 应该是整数类型。"

        printed_output = output.getvalue().strip()
        if local_namespace['age'] > 18:
            expected_output = "成年人"
        else:
            expected_output = "未成年人"

        if expected_output not in printed_output:
            return False, f"代码错误，请正确使用if语句检查age的值并打印正确的结果。当前输出: {printed_output}"

        return True, expected_output

    def teaching(self):
        return ("条件语句用于根据条件的真或假来执行不同的代码块。使用 if 关键字来编写条件语句。例如：\n"
                "age = 20\n"
                "if age > 18:\n"
                "    print('成年人')\n"
                "else:\n"
                "    print('未成年人')\n"
                "这段代码会检查 age 是否大于 18，并打印相应的结果。")

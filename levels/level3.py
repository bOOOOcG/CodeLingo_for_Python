from levels.base_level import BaseLevel
import io
import contextlib

class Level3(BaseLevel):
    def description(self):
        return ("第三关：条件语句\n"
                "任务：定义一个变量 `age`，并将其值设为一个整数，然后使用 `if` 语句检查 `age` 是否大于 18，"
                "如果是则打印 '成年人'，否则打印 '未成年人'。\n"
                "此外，定义一个变量 `height` 并将其值设为一个浮点数，然后使用 `if` 语句检查 `height` 是否大于 1.70，"
                "如果是则打印 '你很高'，否则打印 '你不高'。")

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

        if 'height' not in local_namespace:
            return False, "代码错误：请定义变量 'height'。"
        if not isinstance(local_namespace['height'], float):
            return False, "代码错误：变量 'height' 应该是浮点数类型。"

        printed_output = output.getvalue().strip().split('\n')
        expected_output = []
        if local_namespace['age'] > 18:
            expected_output.append("成年人")
        else:
            expected_output.append("未成年人")

        if local_namespace['height'] > 1.70:
            expected_output.append("你很高")
        else:
            expected_output.append("你不高")

        if printed_output != expected_output:
            return False, f"代码错误，请正确使用 if 语句检查 age 和 height 的值并打印正确的结果。当前输出: {printed_output}"

        return True, "代码正确！"

    def teaching(self):
        return ("条件语句用于根据条件的真或假来执行不同的代码块。使用 if 关键字来编写条件语句。例如：\n"
                "age = 20\n"
                "if age > 18:\n"
                "    print('成年人')\n"
                "else:\n"
                "    print('未成年人')\n"
                "height = 1.75\n"
                "if height > 1.70:\n"
                "    print('你很高')\n"
                "else:\n"
                "    print('你不高')\n"
                "这段代码会检查 age 是否大于 18，并打印相应的结果，同时检查 height 是否大于 1.70 并打印相应的结果。")

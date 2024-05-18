from levels.base_level import BaseLevel
import io
import contextlib

class Level2(BaseLevel):
    def description(self):
        return ("第二关：变量和数据类型\n"
                "任务：定义一个变量 `name` 并将其值设为你的名字，然后使用 `print` 函数打印出 '你好, name！'。\n"
                "此外，定义一个变量 `age` 并将其值设为你的年龄，定义一个变量 `height` 并将其值设为你的身高（单位：米）。\n"
                "使用 `print` 函数分别打印出这些变量的值。")

    def check_code(self, code):
        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误: {e}"

        # 检查变量 name
        if 'name' not in local_namespace:
            return False, "代码错误：请定义变量 'name'。"
        if not isinstance(local_namespace['name'], str):
            return False, "代码错误：变量 'name' 应该是字符串类型。"

        # 检查变量 age
        if 'age' not in local_namespace:
            return False, "代码错误：请定义变量 'age'。"
        if not isinstance(local_namespace['age'], int):
            return False, "代码错误：变量 'age' 应该是整数类型。"

        # 检查变量 height
        if 'height' not in local_namespace:
            return False, "代码错误：请定义变量 'height'。"
        if not isinstance(local_namespace['height'], float):
            return False, "代码错误：变量 'height' 应该是浮点数类型。"

        # 检查输出
        printed_output = output.getvalue().strip()
        if all(val in printed_output for val in [local_namespace['name'], str(local_namespace['age']), str(local_namespace['height'])]):
            return True, "代码正确！"
        else:
            return False, f"代码错误：输出应包含 'name'、'age' 和 'height'。当前输出: {printed_output}"

    def teaching(self):
        return ("在 Python 中，变量用于存储数据。可以使用等号 '=' 来赋值。例如：\n"
                "name = 'Alice'\n"
                "age = 25\n"
                "height = 1.70\n"
                "这会将字符串 'Alice' 赋值给变量 name，将整数 25 赋值给变量 age，将浮点数 1.70 赋值给变量 height。\n"
                "然后可以使用 `print` 函数来打印变量的值，例如：\n"
                "print(f'你好, {name}！')\n"
                "print(f'年龄: {age}')\n"
                "print(f'身高: {height}')\n"
                "在这个任务中，你需要定义变量 `name`、`age` 和 `height`，并分别打印它们的值。")

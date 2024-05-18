from levels.base_level import BaseLevel
import io
import contextlib

class Level2(BaseLevel):
    def description(self):
        return "第二关：变量和输入\n任务：定义一个变量name，并将其值设为你的名字，然后使用print函数打印出'你好, name！'"

    def check_code(self, code):
        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误: {e}"

        if 'name' not in local_namespace:
            return False, "代码错误：请定义变量 'name'。"
        if not isinstance(local_namespace['name'], str):
            return False, "代码错误：变量 'name' 应该是字符串类型。"

        printed_output = output.getvalue().strip()
        expected_output = f"你好, {local_namespace['name']}"
        
        if expected_output != printed_output:
            if '{name}' in code:
                return False, "代码错误：请使用正确的字符串格式化方法，例如 f-string 或 .format。"
            return False, f"代码错误：请使用 print 函数打印出 '你好, {local_namespace['name']}！'，而不是 '{printed_output}'。"

        return True, expected_output

    def teaching(self):
        return ("在 Python 中，变量用于存储数据。可以使用等号 '=' 来赋值。例如：\n"
                "name = 'Alice'\n"
                "这会将字符串 'Alice' 赋值给变量 name。然后可以使用 print(name) 来打印变量的值。\n"
                "在这个任务中，你需要定义一个变量 name，并将其值设为你的名字，然后使用 print 函数打印出 '你好, name！'")

import os

def create_files(start, end):
    # 确保输入的范围是有效的数字
    try:
        start = int(start)
        end = int(end)
    except ValueError:
        print("请输入有效的数字范围，例如 10-15")
        return

    # 检查范围是否有效
    if start > end or start < 1:
        print("请输入有效的范围，确保开始值小于或等于结束值，并且开始值大于 0")
        return

    # 确保目标目录存在
    target_dir = f"levels/_{start}_{end}"
    os.makedirs(target_dir, exist_ok=True)

    # 模板代码
    template = """from levels.base_level import BaseLevel

class {class_name}(BaseLevel):
    def description(self):
        return "{class_name} 的描述"

    def check_code(self, code):
        # 在这里添加代码检查逻辑
        pass

    def teaching(self):
        return "{class_name} 的教学内容"

    def answer(self):
        return "{class_name} 的参考答案"

    def hint(self):
        return "{class_name} 的提示"

    def run_all_tests(self, user_code):
        # 运行所有测试用例的逻辑
        pass
"""

    # 创建关卡文件
    for level in range(start, end + 1):
        filename = f"level{level}.py"
        class_name = f"Level{level}"
        file_path = os.path.join(target_dir, filename)
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(template.format(class_name=class_name))
        else:
            print(f"文件 {file_path} 已存在，跳过创建。")

    # 创建 Boss 文件
    for level in range(start, end + 1):
        if level % 5 == 0:
            boss_number = level // 5
            boss_filename = f"boss{boss_number}.py"
            boss_class_name = f"Boss{boss_number}"
            boss_file_path = os.path.join(target_dir, boss_filename)
            if not os.path.exists(boss_file_path):
                with open(boss_file_path, "w", encoding="utf-8") as f:
                    f.write(template.format(class_name=boss_class_name))
            else:
                print(f"文件 {boss_file_path} 已存在，跳过创建。")

    print("文件创建完成。")

# 获取用户输入
input_range = input("请输入关卡范围（例如 10-15）：")
try:
    start, end = input_range.split('-')
    create_files(start, end)
except ValueError:
    print("请输入有效的范围，例如 10-15")

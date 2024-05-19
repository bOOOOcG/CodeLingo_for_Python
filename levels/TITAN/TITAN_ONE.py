import ast
from levels.base_level import BaseLevel
import io
import contextlib
import logging
from datetime import datetime

class TitanOne(BaseLevel):
    def description(self):
        return ("TITAN_ONE：史诗级关卡\n"
                "任务：定义一个类 TitanOne，该类需要实现以下复杂的数据操作和逻辑处理。\n"
                "1. 类 TitanOne\n"
                "   - 初始化方法 __init__(self, name, data_file, json_file, log_file)，接收四个参数：名字 name、数据文件 data_file、JSON 文件 json_file 和日志文件 log_file。\n"
                "   - 方法 load_data(self)，从 data_file 中读取数据并解析为字典列表，数据格式如下：\n"
                "     name,age,city\n"
                "     Alice,30,New York\n"
                "     Bob,25,Los Angeles\n"
                "     Charlie,35,Chicago\n"
                "   - 方法 analyze_data(self)，分析数据，打印平均年龄，并根据城市统计人数。\n"
                "   - 方法 save_to_json(self)，将分析结果保存到 json_file 中。\n"
                "   - 方法 log_operation(self, operation)，记录每次操作的日志到 log_file 中，日志格式为 操作名称: 时间戳。\n"
                "   - 方法 display_results(self)，读取 json_file 并打印结果。\n"
                "   - 方法 safe_divide(self, a, b)，尝试计算 a 除以 b 的结果并打印，如果发生除零错误，打印 'Division by zero error'。\n"
                "   - 方法 greet(self)，打印 'Hello, my name is name'。")

    def check_code(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"代码执行错误: 语法错误在第 {e.lineno} 行: {e.text.strip()}"

        class_found = False
        methods = {"__init__", "load_data", "analyze_data", "save_to_json", "log_operation", "display_results", "safe_divide", "greet"}
        found_methods = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == "TitanOne":
                class_found = True
                for body_item in node.body:
                    if isinstance(body_item, ast.FunctionDef):
                        if body_item.name in methods:
                            found_methods.add(body_item.name)

        if not class_found:
            return False, "代码错误：请定义类 TitanOne。"
        
        missing_methods = methods - found_methods
        if missing_methods:
            return False, f"代码错误：缺少方法 {', '.join(missing_methods)}。"

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(code, {}, local_namespace)
            except Exception as e:
                return False, f"代码执行错误: {e}"

        if 'TitanOne' not in local_namespace:
            return False, "代码错误：请定义类 TitanOne。"

        return True, "代码检查通过！现在输入测试数据并运行代码。"

    def run_test(self, cls, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                titan = cls(*args)
                titan.load_data()
                titan.analyze_data()
                titan.save_to_json()
                titan.display_results()
                titan.safe_divide(10, 2)
                titan.safe_divide(10, 0)
                titan.greet()
            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                return False, f"测试运行错误: {e}\n调用堆栈:\n{tb}"

        printed_output = output.getvalue().strip().split('\n')
        name, data_file, json_file, log_file = args
        expected_output = [
            "Average age: 30.0",
            "New York: 1",
            "Los Angeles: 1",
            "Chicago: 1",
            "{'average_age': 30.0, 'city_count': {'New York': 1, 'Los Angeles': 1, 'Chicago': 1}}",
            "5.0",
            "Division by zero error",
            f"Hello, my name is {name}"
        ]

        if printed_output != expected_output:
            return False, f"测试运行失败，请检查输出格式。当前输出: {printed_output}。"

        return True, "测试运行成功！"

    def run_all_tests(self, user_code):
        test_cases = [
            ("Titan", "data_titan_one.csv", "results_titan_one.json", "log_titan_one.txt"),
            ("Titan2", "data_titan_one2.csv", "results_titan_one2.json", "log_titan_one2.txt")
        ]

        # 预先创建测试用例文件
        with open('data_titan_one.csv', 'w') as file:
            file.write('name,age,city\nAlice,30,New York\nBob,25,Los Angeles\nCharlie,35,Chicago\n')

        with open('data_titan_one2.csv', 'w') as file:
            file.write('name,age,city\nDavid,40,Houston\nEve,45,San Francisco\nFrank,50,Seattle\n')

        local_namespace = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                exec(user_code, {}, local_namespace)
                if 'TitanOne' not in local_namespace or not callable(local_namespace['TitanOne']):
                    return False, "代码错误：请定义类 TitanOne。"
            except Exception as e:
                return False, f"代码执行错误: {e}"

        TitanOne_cls = local_namespace['TitanOne']

        for args in test_cases:
            success, message = self.run_test(TitanOne_cls, *args)
            if not success:
                return False, message

        return True, "所有测试用例通过！"

    def teaching(self):
        return ("在这个TITAN_ONE关卡中，你需要综合运用前面所学的所有知识。你需要定义一个类 TitanOne，并在类中实现多个方法来处理复杂的数据操作和逻辑处理。\n"
                "例如，定义 __init__ 方法初始化属性，定义 load_data 方法读取数据文件，定义 analyze_data 方法分析数据，定义 save_to_json 方法保存分析结果，"
                "定义 log_operation 方法记录操作日志，定义 display_results 方法显示结果，定义 safe_divide 方法处理除零错误，定义 greet 方法打印问候语。")

    def answer(self):
        return ("import json\n"
                "import csv\n"
                "import logging\n"
                "from datetime import datetime\n\n"
                "class TitanOne:\n"
                "    def __init__(self, name, data_file, json_file, log_file):\n"
                "        self.name = name\n"
                "        self.data_file = data_file\n"
                "        self.json_file = json_file\n"
                "        self.log_file = log_file\n"
                "        self.data = []\n"
                "        self.analysis_result = {}\n"
                "        logging.basicConfig(filename=log_file, level=logging.INFO)\n\n"
                "    def load_data(self):\n"
                "        try:\n"
                "            with open(self.data_file, 'r') as file:\n"
                "                reader = csv.DictReader(file)\n"
                "                self.data = [row for row in reader]\n"
                "            self.log_operation('load_data')\n"
                "        except FileNotFoundError:\n"
                "            print('Data file not found')\n"
                "            self.log_operation('load_data_failed')\n\n"
                "    def analyze_data(self):\n"
                "        if not self.data:\n"
                "            print('No data loaded')\n"
                "            self.log_operation('analyze_data_failed')\n"
                "            return\n"
                "        total_age = 0\n"
                "        city_count = {}\n"
                "        for person in self.data:\n"
                "            age = int(person['age'])\n"
                "            total_age += age\n"
                "            city = person['city']\n"
                "            if city in city_count:\n"
                "                city_count[city] += 1\n"
                "            else:\n"
                "                city_count[city] = 1\n"
                "        average_age = total_age / len(self.data)\n"
                "        self.analysis_result = {\n"
                "            'average_age': average_age,\n"
                "            'city_count': city_count\n"
                "        }\n"
                "        print(f'Average age: {average_age}')\n"
                "        for city, count in city_count.items():\n"
                "            print(f'{city}: {count}')\n"
                "        self.log_operation('analyze_data')\n\n"
                "    def save_to_json(self):\n"
                "        if not self.analysis_result:\n"
                "            print('No analysis result to save')\n"
                "            self.log_operation('save_to_json_failed')\n"
                "            return\n"
                "        try:\n"
                "            with open(self.json_file, 'w') as file:\n"
                "                json.dump(self.analysis_result, file)\n"
                "            self.log_operation('save_to_json')\n"
                "        except Exception as e:\n"
                "            print(f'Failed to save JSON file: {e}')\n"
                "            self.log_operation('save_to_json_failed')\n\n"
                "    def log_operation(self, operation):\n"
                "        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')\n"
                "        logging.info(f'{operation}: {timestamp}')\n\n"
                "    def display_results(self):\n"
                "        try:\n"
                "            with open(self.json_file, 'r') as file:\n"
                "                results = json.load(file)\n"
                "                print(results)\n"
                "            self.log_operation('display_results')\n"
                "        except FileNotFoundError:\n"
                "            print('JSON file not found')\n"
                "            self.log_operation('display_results_failed')\n\n"
                "    def safe_divide(self, a, b):\n"
                "        try:\n"
                "            result = a / b\n"
                "            print(result)\n"
                "            self.log_operation('safe_divide_success')\n"
                "        except ZeroDivisionError:\n"
                "            print('Division by zero error')\n"
                "            self.log_operation('safe_divide_failed')\n\n"
                "    def greet(self):\n"
                "        print(f'Hello, my name is {self.name}')\n"
                "        self.log_operation('greet')\n\n"
                "# 示例调用\n"
                "titan = TitanOne('Titan', 'data_titan_one.csv', 'results_titan_one.json', 'log_titan_one.txt')\n"
                "titan.load_data()\n"
                "titan.analyze_data()\n"
                "titan.save_to_json()\n"
                "titan.display_results()\n"
                "titan.safe_divide(10, 2)\n"
                "titan.safe_divide(10, 0)\n"
                "titan.greet()")

    def hint(self):
        return ("提示：你需要定义一个类 TitanOne，并在类中实现多个方法来处理复杂的数据操作和逻辑处理。\n"
                "例如，定义 __init__ 方法初始化属性，定义 load_data 方法读取数据文件，定义 analyze_data 方法分析数据，"
                "定义 save_to_json 方法保存分析结果，定义 log_operation 方法记录操作日志，定义 display_results 方法显示结果，"
                "定义 safe_divide 方法处理除零错误，定义 greet 方法打印问候语。")

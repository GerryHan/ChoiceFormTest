# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pytest
import os
import allure
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pass
    # pytest.main(["case/standard", "--alluredir=report/allure/xml"])
    # os.system('allure generate ./report/allure/xml -o ./report/allure/html --clean')

# 第一种方法
# 生成报告xml命令
# pytest case/standard --alluredir ./report/allure/xml
# 生成报告命令
# allure generate  ./report/allure/xml -o ./report/allure/html --clean
# 打开报告
# allure open ./report/allure/html

# 第二种方法
# pytest --alluredir=./allure --clean-alluredir
# allure serve ./allure

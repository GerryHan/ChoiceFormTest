import allure
import pytest

from lib.standard.business.spaceInterface import SpaceInterface
from tools.printTool import zPrint
a=1
b=3


@allure.feature("巧思科技")
@allure.story("测试空间")
@allure.suite("工作流")
@allure.title(f"异常场景")
@pytest.mark.smoke
def testExecCase():
    f"""异常场景
    """
    try:
        # 前置
        preset()
        # 用例执行体
        case()

    finally:
        # 后置
        reset()


@allure.step("前置")
def preset():
    """
    用例内部前置方法名为
    :return:
    """


@allure.step("后置")
def reset():
    """
    用例内部后置方法名为
    :return:
    """


@allure.step("执行体")
def case():
    """
    执行体方法, 用例主要步骤
    :return:
    """
    with allure.step("step1"):
        with allure.step("step1.1"):
            pass
    with allure.step("step2 断言数字"):
        with allure.step("step2.1 断言数字"):
            with allure.step("step2.1.1 断言数字"):
                zPrint("工作流运行错误")
    with allure.step("step3 断言数字"):
        with allure.step("新建一个空间"):
            res = SpaceInterface.createSpace(name="测试空间1号")
            print(res)


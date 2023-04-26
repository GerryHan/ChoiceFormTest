import allure
import pytest

from tools.printTool import zPrint


@allure.feature("巧思科技")
@allure.story("测试空间")
@allure.suite("工作流")
@allure.title(f"工作流运行工作流")
@pytest.mark.smoke
def testExecCase():
    f"""查询表数据
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
    with allure.step("R"):
        zPrint("R")


@allure.step("执行体")
def case():
    """
    执行体方法, 用例主要步骤
    :return:
    """
    with allure.step("step1"):
        with allure.step("step1.1"):
            zPrint("工作流运行正确")
    with allure.step("step2 断言数字"):
        with allure.step("step2.1 断言数字"):
            with allure.step("step2.1.1 断言数字"):
                zPrint("工作流运行错误")
    with allure.step("step3 断言数字"):
        assert 1 == 2

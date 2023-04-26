使用说明书：
第一步：使用下面命令安装相关插件
    pip install -r requirements.txt
第二步：在pytest.ini文件中配置需要跑的用例目录和命令
第三步：在pytest的终端中输入pytest

项目分层介绍：
整个Workflow项目分为case,config,lib,logs,report,resource,tools七层
    1.config层：放配置文件，把所有的项目相关的配置均放到这个目录里，实现配置与代码分离,
        globals下为全局配置文件
        其他分别是各个模块对应配置。例如contract存放合同相关的配置文件
        环境配置：jenkins创建多个环境job
    2.lib层：根据业务分为global,menu,module三个目录
        standard：标准共功能
            global：存放全局功能模块或公共单接口，例如寻源模块
                寻源.py
                协同.py
                商城.py
                public.py
            menu：放置功能模块单接口,单接口组成的业务模块文件。
            business：根据业务由单接口组成的提供给case使用的小模块
               zyRequest.py
               order.py
               logistics.py
               ......

    3.resource层：
        drivers放所需的驱动，如Chromedriver、IEDriverServer等；(为后期UI自动化做准备)
        files放置lib下module中各个模块需要的文件例如doc，pdf，png等
    4.logs层：所有生成的日志均存放在这里，可将日志分类，如运行时日志test log，错误日志error log等。
    5.report层：放程序运行生成的aluer报告。
    6.tools:自定义的一些工具类等
    7.case层，放所有用例。其中更进一步的分层：
        mobile：移动端
        secOpen：二次开发
        standard：标准共功能
            (1)initGlobal：放所全局初始化文件。
            (2)clearGlobal：放全局清理工作文件。
            conftest.py 前后置文件 内部方法命名为 globalPresetAndReset():
            (3)根据业务流程分的各个模块,例如寻源-供应商管理等
                平台功能-注册&登录
                    conftest.py 前后置文件 内部方法命名为 businessPresetAndReset():
                    用例文件名(SVN用例文件名)
                        conftest.py 前后置文件 内部方法命名为 modulePresetAndReset():
                        用例1.py
                            # 为了保证前后置失败，也判定用例失败
                            用例内部前置方法名为 preset()
                            用例内部后置方法名为 reset()
                            执行体方法execCase()
                            用例执行方法
                                testExecCase():
                                    preset()
                                    # 用例执行体
                                    execCase()
                                    reset()

                        用例2.py
                        ......
                    用例文件名2(SVN用例文件名2)
                    ......
                寻源套件-供应商管理
                ......


注意事项:跑前开启vpn(获取验证码,)需要
2023-02-08 更新
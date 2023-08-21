# Pytest_API
基于python-pytest开发的接口自动化测试框架，使用YAML文件来管理测试用例
Python+pytest+requests+YAML+Allure+Jenkins数据驱动接口自动化测试框架,共六个大模块，详细信息如下说明。



common：

--api_method.py：二次封装get、post请求方法，获取请求响应信息

--check_result.py：自定义断言方法，在断言的时候可以调入该类校验预期结果与实际结果是否一致

--dependent_data.py：处理依赖接口之间的关系，获取依赖接口与被依赖接口的数据信息

--get_template_variable.py：封装template模板下的变量，即将请求头信息、请求数据封装为全局变量

--get_testcase_data.py：获取测试用例信息

--testcase_parameter.py：将测试用例进行参数化




config:

--case_list.txt:测试用例运行清单

--config.ini：全局配置信息，如：域名、账户信息、数据库、邮箱、接口、日志等的配置项，方便统一调度使用

--header.json：请求头信息



data:

--expected_result.json:预期结果数据

--request_data.json：请求数据信息

--testcase.yaml：测试用例



result:

--log:日志文件信息

--report:测试报告



utils:

--connect_db.py:这个文件是数据库连接池的相关内容

--dateencoder_json.py:数据转码，在连接数据库时需要调入该类

--e_mail.py：这个文件主要是配置发送邮件的主题、正文等，将测试报告发送并抄送到相关人

--operate_config.py：读取配置文件的方法，并返回文件中内容

--operate_json.py：封装读取json的方法

--operate_yaml.py：封装读取yaml的方法

--set_log.py：日志，用来打印生成日志





run_start:主程序入口，开始执行接口自动化测试，项目工程部署完毕后直接运行该文件即可



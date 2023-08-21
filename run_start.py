import os
import pytest


class Run_Start():
    def start(self):
        pytest.main(["./comm/testcase_parameter.py","-sv","--failed-first","--maxfail=5","--alluredir","./result/report/json"])
        os.system("allure generate ./result/report/json -o ./result/report/html --clean")


if __name__ == "__main__":
    r = Run_Start()
    r.start()







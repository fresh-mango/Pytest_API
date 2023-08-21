#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import time
import logging
import logging.handlers
from utils.operate_config import ParserConfig,log_path


class Set_Log():

    def log_info(self,logger_name=None):
        # 定义日志默认路径和日志名称
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        runtime = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        logfile = os.path.join(log_path, runtime+'.log')
        logfile_err = os.path.join(log_path, runtime+'_error.log')

        p = ParserConfig()
        backup = p.get_section_options('log', 'backup')
        logger_level = p.get_section_options('log','logger_level')
        console_level = p.get_section_options('log','console_level')
        logfile_level = p.get_section_options('log', 'logfile_level')
        logfile_err_level = p.get_section_options('log', 'logfile_err_level')


        # 第一步，初始化日志对象并设置日志等级
        logger = logging.getLogger(logger_name)
        logger.setLevel(logger_level)


        #第二步，设置格式器
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(filename)s  - [line:%(lineno)d] - %(levelname)s: %(message)s")


        # 第三步，创建一个handler，用于输出info日志到控制台
        if not logger.handlers:
            ch = logging.StreamHandler(sys.stdout)
            ch.setFormatter(formatter)
            ch.setLevel(console_level)
            logger.addHandler(ch)


            # 第四步，创建一个handler，用于写入error日志文件
            fh_err = logging.FileHandler(logfile_err,mode='a+')
            fh_err.setFormatter(formatter)
            fh_err.setLevel(logfile_err_level)
            logger.addHandler(fh_err)


            # 第四步，再创建一个handler，每天重新创建一个日志文件，最多保留backup_count份
            fh = logging.handlers.TimedRotatingFileHandler(filename=logfile,
                                                           when='midnight',
                                                           interval=1,
                                                           backupCount=backup,
                                                           delay=True,
                                                           encoding='utf-8')
            fh.setFormatter(formatter)
            fh.setLevel(logfile_level)
            logger.addHandler(fh)

        return logger




if __name__ == "__main__":
    s = Set_Log()
    log =s.log_info()
    log.info('ces')
    log.debug('mm')
    log.error('ppp')
    log.critical('rrr')


'''
根据已有数据库表创建对应的class
'''

import os
import pymysql
pymysql.install_as_MySQLdb()
os.system(
    "sqlacodegen --noviews --noconstraints --noindexes --outfile models2.py mysql://root:root@127.0.0.1:3306/tcm_qa"
)

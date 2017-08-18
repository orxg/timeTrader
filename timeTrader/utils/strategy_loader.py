# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 16:06:00 2017

@author: LDH
"""

# strategy_loader.py

import six
import codecs 

class StrategyLoader():
    '''
    负责返回编译后的user function以及其运行环境的__dict__.
    目前支持文本。
    '''
    def __init__(self,user_file_path):
        self.user_file_path = user_file_path
    
    def load(self,scope):
        with codecs.open(self.user_file_path,encoding = 'utf8') as f:
            source_code = f.read()
        source_code = source_code.encode('utf8')
        source_code_compiled = compile(source_code,'','exec')
        six.exec_(source_code_compiled,scope)
        return scope

if __name__ == '__main__':
    sl = StrategyLoader('test.py')


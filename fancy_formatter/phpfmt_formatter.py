# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

import os
import re
import subprocess
from .base import *
import tempfile


class PhpfmtFormatter(IBaseFormatter):

    def __init__(self,  name: str,setting:ISettingReader,  debug : bool ):
        super().__init__(name,setting,debug)
        self._support_file_type_list :List[EFileType]= [EFileType.PHP]

    def is_support(self,file_type:EFileType)->bool:         
        return file_type in self._support_file_type_list 

    def format_text(self, file_type:EFileType, text:str) -> FormatResult:
        php_path = 'php'
        if self._setting.get("php_path"):
            php_path = self._setting.get("php_path")
            if not os.path.exists(php_path) or not os.path.isfile(php_path):
                return FormatResult.fatal_error(f"Can't find php path: {php_path}")                

        cmd = []
        cmd.append(str(php_path))
        cmd.append('-ddisplay_errors=stderr')
        cmd.append('-dshort_open_tag=On')

        phpfmt_path = self._setting.get("path")
        if not os.path.exists(phpfmt_path) or not os.path.isfile(phpfmt_path):
            return FormatResult.fatal_error(f"Can't find phpfmt_path: {phpfmt_path}")
        cmd.append(phpfmt_path)

        
        option_reader = self._setting.create_sub("option")
        if option_reader.get("psr1"):
            cmd.append('--psr1')
        if option_reader.get("psr1_naming"):
            cmd.append('--psr1-naming')
        if option_reader.get("psr2"):
            cmd.append('--psr2')

        indent_with_space = option_reader.get("indent_with_space")
        if indent_with_space is True:
            cmd.append('--indent_with_space')
        elif indent_with_space > 0:
            cmd.append('--indent_with_space=' + str(indent_with_space))

        if option_reader.get("enable_auto_align"):
            cmd.append('--enable_auto_align')

        if option_reader.get("visibility_order"):
            cmd.append('--visibility_order')

        if option_reader.get("smart_linebreak_after_curly"):
            cmd.append('--smart_linebreak_after_curly')

        passes =option_reader.get("passes")
        if len(passes) > 0:
            cmd.append('--passes=' + ','.join(passes))

        excludes =option_reader.get("excludes")   
        if len(excludes) > 0:
            cmd.append('--exclude=' + ','.join(excludes))

        cmd.append('-')
        return execute_with_pipe(cmd,text)     
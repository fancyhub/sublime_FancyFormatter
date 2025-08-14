# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

import re
import sys 
import os
import subprocess
import tempfile
from .base import *


# use clang-format to format code
class ClangFormatFormatter(IBaseFormatter):

    def __init__(self, setting:ISettingReader, debug : bool ):
        self._setting = setting
        self._debug = debug
        self._support_file_type_list :List[EFileType]= [
            EFileType.C,EFileType.CPP,
            EFileType.CS,
            EFileType.JAVA,
            EFileType.JS,EFileType.TS,EFileType.JSON,
            EFileType.M,EFileType.MM,
            EFileType.PROTO]

    def get_support_file_type(self)->List[EFileType]:        
        return self._support_file_type_list     

    def format_text(self, file_type:EFileType, text:str) -> FormatResult:
        
        cmd=[]
        
        exe_path = self._setting.get("exe_path")
        if exe_path:
            if not os.path.exists(exe_path) or not os.path.isfile(exe_path):
                return FormatResult.fatal_error(f"Can't find clang_format.exe.path: {exe_path}")
        else:
            exe_path = "clang-format"
        cmd.append(exe_path)

        style = self._setting.get(f"style_{file_type.get_suffix()}",'style')
        cmd.append(f"-assume-filename=file.{file_type.get_suffix()}")
        cmd.append(f"-style={style}")
        cmd.append("-")
        if self._debug:
            print(" ".join(cmd))
        return execute_with_pipe(cmd,text) 

    def _get_hidden_startupinfo(self):
        if sys.platform.startswith('win32'):
            startupinfo = subprocess.STARTUPINFO()
            # 设置窗口隐藏标志
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            return startupinfo
        return None
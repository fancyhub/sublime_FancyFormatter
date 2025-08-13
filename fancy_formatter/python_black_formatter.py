# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)


import os
from .base import *

# use black, pip install black
class PythonBlackFormatter(IBaseFormatter):
    def __init__(self, setting:ISettingReader, debug : bool ):
        self._setting = setting
        self._debug = debug

    def get_support_file_type(self)->List[FileType]:
        support_list= [FileType.PY]
        ret=[]
        for syntax in self._setting.get("syntaxes"):
            ft = FileType.from_string(syntax)
            if ft in support_list:
                ret.append(ft)
        return ret

    def format_text(self, file_type:FileType, text:str) -> FormatResult:
        cmd=[]
        
        exe_path = self._setting.get("exe_path")
        if exe_path:
            if not os.path.exists(exe_path) or not os.path.isfile(exe_path):
                return FormatResult.fatal_error(f"Can't find black: {exe_path}")
        else:
            exe_path = "black"        
        cmd.append(exe_path)

        cmd.append("--quiet")
        cmd.append("-")

        if self._debug:
            print(" ".join(cmd))

        return execute_with_pipe(cmd, text)
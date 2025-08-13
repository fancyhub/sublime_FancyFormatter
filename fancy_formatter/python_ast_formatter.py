# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

import ast
from .base import *


class PythonAstFormatter(ISettingReader):
    def __init__(self, setting:ISettingReader, debug : bool ):
        self._setting = setting
        self._debug = debug

    def get_support_file_type(self)->List[EFileType]:
        support_list= [EFileType.PY]
        ret=[]
        for syntax in self._setting.get("syntaxes"):
            ft = EFileType.from_string(syntax)
            if ft in support_list:
                ret.append(ft)
        return ret

    def format_text(self, file_type:EFileType, text:str) -> FormatResult:        
        
        try:
            tree = ast.parse(text)            
            formatted_code = ast.unparse(tree)
            return FormatResult(formatted_code)
        except SyntaxError as e:            
            return FormatResult.normal_error(f"Line: {e.lineno}, Col: {e.offset}: {e.msg}")
        except Exception as e:
            return FormatResult.from_exception(e)

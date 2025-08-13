# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

from .base import *

class GofmtFormatter:

    def __init__(self, setting:ISettingReader, debug : bool ):
        self._setting = setting
        self._debug = debug

    def get_support_file_type(self)->List[EFileType]:
        support_list= [EFileType.GO]
        ret=[]
        for syntax in self._setting.get("syntaxes"):
            ft = EFileType.from_string(syntax)
            if ft in support_list:
                ret.append(ft)
        return ret

    def format_text(self, file_type:EFileType, text:str) -> Tuple[str,str]:
        return execute_with_pipe(['gofmt'], text)
        
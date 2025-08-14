# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

from .base import *

class GofmtFormatter:

    def __init__(self, setting:ISettingReader, debug : bool ):
        self._setting = setting
        self._support_file_type_list :List[EFileType]= [EFileType.GO]

    def get_support_file_type(self)->List[EFileType]:        
        return self._support_file_type_list


    def format_text(self, file_type:EFileType, text:str) -> Tuple[str,str]:
        cmd=[]
        
        exe_path = self._setting.get("exe_path")
        if exe_path:
            if not os.path.exists(exe_path) or not os.path.isfile(exe_path):
                return FormatResult.fatal_error(f"Can't find gofmt path: {exe_path}")
        else:
            exe_path = "gofmt"
        cmd.append(exe_path)

        return execute_with_pipe(cmd, text)
        
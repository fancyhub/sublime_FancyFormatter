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
        return execute_with_pipe(['gofmt'], text)
        
# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)


from .base import *    
from .lib.cssbeautifier import *


class CssbeautifierFormatter(IBaseFormatter):

    def __init__(self, name: str, setting:ISettingReader, debug : bool ):
        super().__init__(name,setting,debug)
        self._support_file_type_list :List[EFileType]= [EFileType.CSS,EFileType.LESS]

    def is_support(self,file_type:EFileType)->bool:         
        return file_type in self._support_file_type_list      
 
    def format_text(self, file_type:EFileType, text:str) -> FormatResult:

        options=default_options()
        option_reader = self._setting.create_sub("option")
        for key in option_reader.get_keys():
            setattr(options, key, option_reader.get(key))

        try:
            stdout = beautify(text, options)
            return FormatResult(stdout)
        except Exception as e:
            return FormatResult.from_exception(e)        

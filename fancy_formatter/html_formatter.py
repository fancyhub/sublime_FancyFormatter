# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

 
from .base import * 
from .lib.htmlbeautifier import *

class HtmlFormatter(IBaseFormatter):

    def __init__(self, setting:ISettingReader, debug : bool ):
        self._setting = setting
        self._debug = debug

    def get_support_file_type(self)->List[FileType]:
        support_list= [FileType.HTML,FileType.ASP,FileType.XML]
        ret=[]
        for syntax in self._setting.get("syntaxes"):
            ft = FileType.from_string(syntax)
            if ft in support_list:
                ret.append(ft)
        return ret    

    def format_text(self, file_type:FileType, text:str) -> FormatResult:
        options=default_options()
        keys = [            
            'indent_size',
            'indent_char',
            'indent_with_tabs',
            'exception_on_tag_mismatch',
            'minimum_attribute_count',
            'first_attribute_on_new_line',
            'expand_tags',
            'reduce_empty_tags',
            'reduce_whole_word_tags',
            'custom_singletons',
        ]
                
        for key in keys:             
            setattr(options, key, self._setting.get(key))

        try:
            return FormatResult(beautify(text, options))
        except Exception as e:
            return FormatResult.from_exception(e)    
        
 
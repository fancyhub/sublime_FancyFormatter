# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)


from .base import *    
from .lib.cssbeautifier import *


class CssFormatter:

    def __init__(self, setting:ISettingReader, debug : bool ):
        self._setting = setting
        self._debug = debug

    def get_support_file_type(self)->List[EFileType]:
        support_list= [EFileType.CSS,EFileType.LESS]
        ret=[]
        for syntax in self._setting.get("syntaxes"):
            ft = EFileType.from_string(syntax)
            if ft in support_list:
                ret.append(ft)
        return ret
 

    def format_text(self, file_type:EFileType, text:str) -> FormatResult:
        stderr = ''
        stdout = ''

        keys = [
            'indent_size',
            'indent_char',
            'indent_with_tabs',
            'selector_separator_newline',
            'end_with_newline',
            'eol',
            'space_around_combinator',
            'newline_between_rules',
            'format_on_save'
        ]

        options=default_options()
        for key in keys:
            setattr(options, key, self._setting.get(key))

        try:
            stdout = beautify(text, options)
            return FormatResult(stdout)
        except Exception as e:
            return FormatResult.from_exception(e)        

# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

from .lib.cssbeautifier import *
from .base import *


class ScssFormatter:

    def __init__(self, setting:ISettingReader, debug : bool ):
        self._setting = setting
        self._debug = debug
        self._support_file_type_list :List[EFileType]=[EFileType.SCSS,EFileType.SASS]

    def get_support_file_type(self)->List[EFileType]:        
        return self._support_file_type_list 

    def format_text(self, file_type:EFileType, text:str) -> FormatResult:

        options = default_options()
        keys = [
            'indent_size',
            'indent_char',
            'indent_with_tabs',
            'selector_separator_newline',
            'end_with_newline',
            'eol',
            'space_around_combinator',
            'newline_between_rules'
        ]
        for key in keys:             
            setattr(options, key, self._setting.get(key))

        try:
            return FormatResult(beautify(text, options))
        except Exception as e:
            return FormatResult.from_exception(e)
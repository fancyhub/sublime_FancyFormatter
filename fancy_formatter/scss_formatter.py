# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

from .lib.cssbeautifier import *
from .base import *


class ScssFormatter:

    def __init__(self, setting:ISettingReader, debug : bool ):
        self._setting = setting
        self._debug = debug

    def get_support_file_type(self)->List[FileType]:
        support_list= [FileType.SCSS,FileType.SASS]
        ret=[]
        for syntax in self._setting.get("syntaxes"):
            ft = FileType.from_string(syntax)
            if ft in support_list:
                ret.append(ft)
        return ret

    def format_text(self, file_type:FileType, text:str) -> FormatResult:

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
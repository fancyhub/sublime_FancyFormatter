# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

import os
import sys
import re
from typing import Dict
from .base import *

from .javascript_formatter import JavascriptFormatter
from .gofmt_formatter import GofmtFormatter
from .clang_format_formatter import ClangFormatFormatter
from .html_formatter import HtmlFormatter
from .css_formatter import CssFormatter
from .scss_formatter import ScssFormatter
from .python_black_formatter import PythonBlackFormatter
from .php_cs_fixer_formatter import PhpCsFixerFormatter


map_settings_formatter = [
            ('clang_format', ClangFormatFormatter),
            ('gofmt', GofmtFormatter),
            ('javascript', JavascriptFormatter),
            ("html", HtmlFormatter),
            ("css",CssFormatter),
            ("scss",ScssFormatter),
            ("python_black",PythonBlackFormatter),
            ("php_cs_fixer",PhpCsFixerFormatter),
        ]


class FancyFormatter:
    def __init__(self, setting:ISettingReader):
        self._setting = setting
        self._classmap:Dict[FileType, ISettingReader] = {}

        debug = setting.get("debug")
        # map of settings names with related class
        for name, _class in map_settings_formatter:
            sub_setting= self._setting.create_sub(name)
            formatter = _class(sub_setting,debug)
            for file_type in formatter.get_support_file_type():
                self._classmap[file_type] = formatter
           

    def format_text(self, file_type:FileType, text:str) -> FormatResult:
        formatter = self._classmap[file_type]
        if formatter is None:
            return FormatResult.fatal_error(f"{file_type.name} is not support")
        
        try:
            return formatter.format_text(file_type,text)
        except TypeError as e:
            return FormatResult.from_exception(e)
        except Exception as e:
            return FormatResult.from_exception(e)

    def exists(self, file_type:FileType)->bool:
        return file_type in self._classmap 

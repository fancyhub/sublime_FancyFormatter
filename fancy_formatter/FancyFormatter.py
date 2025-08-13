# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

import os
import sys
import re
from typing import Dict
from .base import *

from .jsbeautifier_formatter import JsBeautifierFormatter
from .gofmt_formatter import GofmtFormatter
from .clang_format_formatter import ClangFormatFormatter
from .html_formatter import HtmlFormatter
from .python_black_formatter import PythonBlackFormatter
from .php_cs_fixer_formatter import PhpCsFixerFormatter
from .beautiful_soup_formatter import BeautifulSoupFormatter
from .css_formatter import CssFormatter
from .scss_formatter import ScssFormatter

map_settings_formatter = [
            ('clang_format', ClangFormatFormatter),
            ('gofmt', GofmtFormatter),
            ('jsbeautifier', JsBeautifierFormatter),
            ("html", HtmlFormatter),            
            ("python_black",PythonBlackFormatter),
            ("php_cs_fixer",PhpCsFixerFormatter),
            ("css",CssFormatter),
            ("scss",ScssFormatter),
            ("beautiful_soup",BeautifulSoupFormatter),
        ]


class FancyFormatter:
    def __init__(self, setting:ISettingReader):
        self._setting = setting
        self._classmap:Dict[FileType, ISettingReader] = {}

        self._debug = setting.get("debug")
        # map of settings names with related class
        for name, _class in map_settings_formatter:
            sub_setting= self._setting.create_sub(name)
            formatter = _class(sub_setting,self._debug)
            for file_type in formatter.get_support_file_type():
                self._classmap[file_type] = formatter
        
        if self._debug:
            for key,value in self._classmap.items():
                print(f"FileType: {key.name.lower()}  \t-> {value.__class__.__name__}")
           

    def format_text(self, file_type:FileType, text:str) -> FormatResult:        
        if file_type not in self._classmap :
            return FormatResult.fatal_error(f"{file_type.name} is not support")
        
        formatter = self._classmap[file_type]
        try:
            return formatter.format_text(file_type,text)
        except TypeError as e:
            return FormatResult.from_exception(e)
        except Exception as e:
            return FormatResult.from_exception(e)

    def exists(self, file_type:FileType)->bool:
        return file_type in self._classmap 

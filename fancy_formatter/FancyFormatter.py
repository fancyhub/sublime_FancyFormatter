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
from .python_black_formatter import PythonBlackFormatter
from .php_cs_fixer_formatter import PhpCsFixerFormatter
from .phpfmt_formatter import PhpfmtFormatter
from .beautiful_soup_formatter import BeautifulSoupFormatter
from .css_formatter import CssFormatter
from .scss_formatter import ScssFormatter
from .prettier_formatter import PrettierFormatter

map_settings_formatter = {
            'clang_format': ClangFormatFormatter,
            'gofmt': GofmtFormatter,
            'jsbeautifier': JsBeautifierFormatter,
            "python_black":PythonBlackFormatter,
            "php_cs_fixer":PhpCsFixerFormatter,
            "css":CssFormatter,
            "scss":ScssFormatter,
            "beautiful_soup":BeautifulSoupFormatter,
            "prettier":PrettierFormatter,
            "phpfmt":PhpfmtFormatter,
}

class FancyFormatter:
    def __init__(self, setting:ISettingReader):
        self._setting = setting
        self._formatter_map:Dict[str, ISettingReader] = {}
        self._debug = setting.get("debug")
        if self._debug:
            print("FancyFormatter is in debug mode")
           

    def _get_formatter_by_name(self,formatter_name:str)->IBaseFormatter:
        global map_settings_formatter
        if not formatter_name:
            return None

        if formatter_name not in map_settings_formatter:
            if self._debug:
                print(f"formatter name:  {formatter_name} not found")
            return None
        
        ret :IBaseFormatter =None
        if formatter_name not in self._formatter_map:
            class_type = map_settings_formatter[formatter_name]
            ret=class_type(self._setting.create_sub(formatter_name),self._debug)
            self._formatter_map[formatter_name] = ret
        else:
            ret = self._formatter_map[formatter_name]       
        return ret
        
        
    def format_text(self, file_type:EFileType, text:str) -> FormatResult:
        formatter_name=self._setting.get(f"file_type.{file_type.get_suffix()}")
        if not formatter_name:
            return FormatResult.fatal_error(f"{file_type.get_suffix()} is not support 1")

        formatter= self._get_formatter_by_name(formatter_name)
        if formatter is None:
            return FormatResult.fatal_error(f"{file_type.get_suffix()}({formatter_name}) is not support 2")
        
        if formatter.get_support_file_type() and file_type not in formatter.get_support_file_type():
            return FormatResult.fatal_error(f"{file_type.get_suffix()}({formatter_name}) is not support 3")
        

        if self._debug:
            print(f"format file \"{file_type.get_suffix()}\" with \"{formatter_name}\"")

        try:
            return formatter.format_text(file_type,text)
        except TypeError as e:
            traceback.print_exc()
            return FormatResult.from_exception(e)
        except Exception as e:
            traceback.print_exc()
            return FormatResult.from_exception(e)

    def exists(self, file_type:EFileType)->bool:
        return file_type in self._classmap 

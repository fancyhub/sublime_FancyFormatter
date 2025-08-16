# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

import os
import sys
import re
from typing import Dict
from .base import *

from .jsbeautifier_formatter import JsBeautifierFormatter
from .php_cs_fixer_formatter import PhpCsFixerFormatter
from .phpfmt_formatter import PhpfmtFormatter
from .beautiful_soup_formatter import BeautifulSoupFormatter
from .cssbeautifier_formatter import CssbeautifierFormatter
from .scssbeautifier_formatter import ScssbeautifierFormatter
from .prettier_formatter import PrettierFormatter
from .custom_formatter import CustomFormatter

map_settings_formatter = {
            'jsbeautifier': JsBeautifierFormatter,
            "php_cs_fixer":PhpCsFixerFormatter,
            "cssbeautifier":CssbeautifierFormatter,
            "scssbeautifier":ScssbeautifierFormatter,
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
           

    def _get_inner_formatter(self,formatter_name:str)->IBaseFormatter:
        global map_settings_formatter
        if not formatter_name:
            return None

        if formatter_name not in map_settings_formatter:            
            return None
        
        ret :IBaseFormatter =None
        if formatter_name not in self._formatter_map:
            class_type = map_settings_formatter[formatter_name]
            ret=class_type(formatter_name,self._setting.create_sub(formatter_name),self._debug)
            self._formatter_map[formatter_name] = ret
        else:
            ret = self._formatter_map[formatter_name]       
        return ret
    
    def _get_custom_formatter(self,formatter_name :str)->CustomFormatter:
        full_formatter_name = f"custom.{formatter_name}"       
        
        if not self._debug and  full_formatter_name in self._formatter_map:             
            return self._formatter_map[full_formatter_name]
        
        config =self._setting.get(full_formatter_name)
        if not config:
            return None
        
        sub_reader=JsonSettingReader(config)
        ret :IBaseFormatter = CustomFormatter(formatter_name,sub_reader,self._debug)
        
        if not self._debug:
            self._formatter_map[full_formatter_name]=ret        
        return ret
        
    def format_text(self, file_type:EFileType, text:str) -> FormatResult:
        formatter_name:str=self._setting.get(f"file_type.{file_type.get_suffix()}")
        if not formatter_name:
            return FormatResult.fatal_error(f"{file_type.get_suffix()} is not support 1")

        if "." in formatter_name:
            return FormatResult.fatal_error(f"can't find the formatter ({formatter_name}) for {file_type.get_suffix()}")
        
        formatter:IBaseFormatter = self._get_custom_formatter(formatter_name)
        if formatter == None:       
            formatter= self._get_inner_formatter(formatter_name)
            if formatter is None:
                return FormatResult.fatal_error(f"can't find the formatter ({formatter_name}) for {file_type.get_suffix()} 2")
            elif self._debug:
                print(f"get formatter {formatter_name}")
        elif self._debug:
            print(f"get custom formatter custom.{formatter_name}")        

        if not formatter.is_support(file_type):
            return FormatResult.fatal_error(f"formatter ({formatter_name}) is not support {file_type.get_suffix()}")
        
        if self._debug:
            print(f"format file \"{file_type.get_suffix()}\" with formatter: \"{formatter.get_name()}\"")

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

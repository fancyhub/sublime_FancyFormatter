# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

import os
import re
import sys
import sublime
import sublime_plugin
from typing import Dict

from .fancy_formatter.base import *
from .fancy_formatter.FancyFormatter import FancyFormatter

 
_fancy_formatter:FancyFormatter = None
_setting_reader:JsonSettingReader =None
_syntax_map :Dict[str,EFileType]= {
    "c#": EFileType.CS,
    "php": EFileType.PHP,
    "javascript": EFileType.JS,
    "typescript": EFileType.TS,
    "python": EFileType.PY,
    "html": EFileType.HTML,
    "css": EFileType.CSS,
    "json": EFileType.JSON,
    "xml": EFileType.XML,
    "objectivе-c": EFileType.M,
    "objectivе-c++": EFileType.MM,
    "c": EFileType.C,
    "c++": EFileType.CPP,
    "go": EFileType.GO,
    "java": EFileType.JAVA,
    "less": EFileType.LESS,
    "scss": EFileType.SCSS,
    "sass": EFileType.SASS,
    "protobuf": EFileType.PROTO,
    "yaml": EFileType.YAML,
    "markdown": EFileType.MD,
}

def _get_setting_reader()->JsonSettingReader:
    global _setting_reader
    if _setting_reader is not None:
        return _setting_reader  
    _setting_reader = JsonSettingReader({})
    return _setting_reader

def _reload_setting_reader()->JsonSettingReader:    
    setting= sublime.load_settings('FancyFormatter.sublime-settings')
    key_value_map=setting.to_dict()     
    ret=_get_setting_reader()
    ret.reset_data(key_value_map)
    return ret

def _get_fancy_formatter()->FancyFormatter:
    global _fancy_formatter
    reader=_reload_setting_reader()
    if _fancy_formatter is not None:
        return _fancy_formatter
    
    _fancy_formatter= FancyFormatter(reader)
    return _fancy_formatter


def plugin_loaded():
    print('FancyFormatter: Plugin Initialized, ST version: ' + sublime.version() + " Python Version: " + sys.version)    
    
def _get_syntax(view)->str:
    pattern = re.compile(r'Packages/.*/(.+?).(?=tmLanguage|sublime-syntax)')
    m = pattern.search(view.settings().get('syntax'))
    found = ''
    if m and len(m.groups()) > 0:
        found = m.groups()[0]
    return found.lower()
 
def _show_error_dialog(text):
    msg=u'FancyFormatter\n\n%s' % text
    sublime.error_message(msg)
    print(msg)
 
class FancyFormatterCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view    
        if view.is_scratch():
            _show_error_dialog('File is scratch')
            return
        syntax = _get_syntax(view)
        global _syntax_map
        file_type = _syntax_map.get(syntax, EFileType.NONE)
        if file_type == EFileType.NONE:
            _show_error_dialog(f'Formatter for this file type ({syntax}) not found.')
            return 
        
        formatter= _get_fancy_formatter()
        file_text = sublime.Region(0, view.size())
        file_text_utf = view.substr(file_text)
        if (len(file_text_utf) == 0):
            return

        result= formatter.format_text(file_type,file_text_utf)
        if result.Code == EFormatResult.OK:
            view.replace(edit, file_text, result.Result)
            print("FancyFormatter: format succ")
        elif result.Code == EFormatResult.Fatal:
            _show_error_dialog('Format Error\n' + result.ErrorMsg)
        else:
            print(u'FancyFormatter\n\n%s' % result.ErrorMsg)
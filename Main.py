# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

import os
import re
import sys
import sublime
import sublime_plugin

from .fancy_formatter.base import *
from .fancy_formatter.FancyFormatter import FancyFormatter

 
_fancy_formatter:FancyFormatter = None
_setting_reader:JsonSettingReader =None

def _get_setting_reader()->JsonSettingReader:
    global _setting_reader
    if _setting_reader is not None:
        return _setting_reader
    setting= sublime.load_settings('FancyFormatter.sublime-settings')
    _setting_reader = JsonSettingReader(setting)
    return _setting_reader

def _reload_setting_reader()->JsonSettingReader:    
    _get_setting_reader().reset_data(sublime.load_settings('FancyFormatter.sublime-settings'))    

def _get_fancy_formatter()->FancyFormatter:
    global _fancy_formatter
    if _fancy_formatter is not None:
        _reload_setting_reader()
        return _fancy_formatter
    
    _fancy_formatter= FancyFormatter(_get_setting_reader())
    return _fancy_formatter


def plugin_loaded():
    print('FancyFormatter: Plugin Initialized, ST version: ' + sublime.version() + " Python Version: " + sys.version)    
    
def _get_syntax(view)->str:
    view.settings().get('syntax')
    pattern = re.compile(r'Packages/.*/(.+?).(?=tmLanguage|sublime-syntax)')
    m = pattern.search(view.settings().get('syntax'))
    found = ''
    if m and len(m.groups()) > 0:
        found = m.groups()[0]
    return found.lower()


def _syntax_to_file_type(syntax :str) ->FileType:
    if syntax== "c#":
        return FileType.CS
    elif syntax=="php":
        return FileType.PHP
    elif syntax=="javascript":
        return FileType.JS
    elif syntax=="typescript":  
        return FileType.TS
    elif syntax=="python":
        return FileType.PY
    elif syntax=="html":
        return FileType.HTML
    elif syntax=="css":
        return FileType.CSS
    elif syntax=="json":
        return FileType.JSON
    elif syntax=="xml":
        return FileType.XML
    elif syntax=="objectivе-c":
        return FileType.M
    elif syntax=="objectivе-c++":
        return FileType.MM
    elif syntax=="c":
        return FileType.C
    elif syntax=="c++":
        return FileType.CPP    
    elif syntax=="go":
        return FileType.GO
    elif syntax=="java":
        return FileType.JAVA
    elif syntax=="less":
        return FileType.LESS
    elif syntax=="scss":
        return FileType.SCSS
    elif syntax=="sass":
        return FileType.SASS
    elif syntax=="protobuf":
        return FileType.PROTO
    return FileType.NONE


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
        file_type = _syntax_to_file_type(syntax)
        if file_type == FileType.NONE:
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
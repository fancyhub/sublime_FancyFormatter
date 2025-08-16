# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

import os
import re
import sys
import sublime
import sublime_plugin
import webbrowser
from typing import Dict

from .fancy_formatter.base import *
from .fancy_formatter.FancyFormatter import FancyFormatter


_fancy_formatter:FancyFormatter = None
_setting_reader:JsonSettingReader =None
# _syntax_map :Dict[str,EFileType]= {
#     "c#": EFileType.CS,
#     "php": EFileType.PHP,
#     "javascript": EFileType.JS,
#     "typescript": EFileType.TS,
#     "python": EFileType.PY,
#     "html": EFileType.HTML,
#     "css": EFileType.CSS,
#     "json": EFileType.JSON,
#     "xml": EFileType.XML,
#     "objectivе-c": EFileType.M,
#     "objectivе-c++": EFileType.MM,
#     "c": EFileType.C,
#     "c++": EFileType.CPP,
#     "go": EFileType.GO,
#     "java": EFileType.JAVA,
#     "less": EFileType.LESS,
#     "scss": EFileType.SCSS,
#     "sass": EFileType.SASS,
#     "protobuf": EFileType.PROTO,
#     "yaml": EFileType.YAML,
#     "markdown": EFileType.MD,
# }

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
    sublime.error_message(f"FancyFormatter\n{text}")
    # print(f"FancyFormatter: {text}")
 
class FancyFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view    
        if view.is_scratch():
            _show_error_dialog('File is scratch')
            return
        syntax = _get_syntax(view)
        
        formatter= _get_fancy_formatter()
        file_text_region = sublime.Region(0, view.size())
        file_text = view.substr(file_text_region)
        if (len(file_text) == 0):
            return

        result= formatter.format_text(file_text,syntax)
        if result.Code == EFormatResult.OK:
            if file_text != result.Result:
                view.replace(edit, file_text_region, result.Result)
            print("FancyFormatter: format succ")
        elif result.Code == EFormatResult.Fatal:
            _show_error_dialog(result.ErrorMsg)
        else:
            print(f"FancyFormatter: {result.ErrorMsg}")


class FancyFormatterOpenUrlCommand(sublime_plugin.ApplicationCommand):
    re_pkgs = re.compile(r'^Packages')
    def run(self, url):
        if url.startswith('sub://Packages'):
            sublime.run_command('open_file', {"file": self.re_pkgs.sub('${packages}', url[6:])})
        else:
            webbrowser.open_new_tab(url)
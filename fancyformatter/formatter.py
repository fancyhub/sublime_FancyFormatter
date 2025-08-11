# @author             Avtandil Kikabidze
# @copyright         Copyright (c) 2008-2015, Avtandil Kikabidze aka LONGMAN (akalongman@gmail.com)
# @link             http://longman.me
# @license         The MIT License (MIT)

import os
import sys
import re
import sublime
from .phpformatter import PhpFormatter
from .jsformatter import JsFormatter
from .htmlformatter import HtmlFormatter
from .cssformatter import CssFormatter
from .scssformatter import ScssFormatter
# from .pyformatter import PyFormatter
from .vbscriptformatter import VbscriptFormatter
from .coldfusionformatter import ColdfusionFormatter
from .goformatter import GoFormatter
from .clangformatter import ClangFormatter


class Formatter:

    def __init__(self, view, syntax=None):

        self.platform = sublime.platform()
        self.classmap = {}

        self.file_name = view.file_name()
        self.settings = sublime.load_settings('FancyFormatter.sublime-settings')
        self.packages_path = sublime.packages_path()

        self.syntax_file = view.settings().get('syntax')
        self.syntax = syntax or self.get_syntax()

        # map of settings names with related class
        map_settings_formatter = [
            ('formatter_php_options', PhpFormatter),
            ('formatter_js_options', JsFormatter),
            ('formatter_css_options', CssFormatter),
            ('formatter_html_options', HtmlFormatter),
            # ('formatter_python_options', PyFormatter),
            ('formatter_vbscript_options', VbscriptFormatter),
            ('formatter_scss_options', ScssFormatter),
            ('formatter_coldfusion_options', ColdfusionFormatter),
            ('formatter_go_options', GoFormatter),
            ('formatter_clang_options', ClangFormatter),
        ]

        for name, _class in map_settings_formatter:
            syntaxes = self.settings.get(name, {}).get('syntaxes')
            if not syntaxes or not isinstance(syntaxes, str):
                continue
            for _formatter in syntaxes.split(','):
                self.classmap[_formatter.strip()] = _class

    def format(self, text):
        formatter = self.classmap[self.syntax](self)
        try:
            stdout, stderr = formatter.format(self.syntax,text)
        except Exception as e:
            stdout = ''
            stderr = str(e)

        return self.clean(stdout), self.clean(stderr)

    def exists(self):
        return self.syntax in self.classmap

    def get_syntax(self):
        pattern = re.compile(r'Packages/.*/(.+?).(?=tmLanguage|sublime-syntax)')
        m = pattern.search(self.syntax_file)
        found = ''
        if m and len(m.groups()) > 0:
            found = m.groups()[0]
        return found.lower()

    def format_on_save_enabled(self):
        if not self.exists():
            return False
        formatter = self.classmap[self.syntax](self)
        return formatter.format_on_save_enabled(self.file_name)

    def clean(self, string):
        if hasattr(string, 'decode'):
            string = string.decode('UTF-8', 'ignore')

        return re.sub(r'\r\n|\r', '\n', string)

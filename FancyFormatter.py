# @author             Avtandil Kikabidze
# @copyright         Copyright (c) 2008-2015, Avtandil Kikabidze aka LONGMAN (akalongman@gmail.com)
# @link             http://longman.me
# @license         The MIT License (MIT)

import os
import sys
import sublime
import sublime_plugin
from .fancyformatter.formatter import Formatter

 

def plugin_loaded():
    print('FancyFormatter: Plugin Initialized, ST version: ' + sublime.version() + " Python Version: " + sys.version)    
    
  

class FancyFormatterCommand(sublime_plugin.TextCommand):
    def run(self, edit, syntax=None, saving=None):                
        run_formatter(self.view, edit, syntax=syntax, saving=saving)


class FancyFormatterOpenTabsCommand(sublime_plugin.TextCommand):
    def run(self, edit, syntax=None):
        window = sublime.active_window()
        for view in window.views():
            run_formatter(view, edit, quiet=True)


class FancyFormatterEventListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        view.run_command('fancy_formatter', {'saving': True}) 

def run_formatter(view, edit, *args, **kwargs):

    if view.is_scratch():
        show_error('File is scratch')
        return

    # default parameters
    syntax = kwargs.get('syntax')
    saving = kwargs.get('saving', False)
    quiet = kwargs.get('quiet', False)

    formatter = Formatter(view, syntax)
    if not formatter.exists():
        if not quiet and not saving:
            show_error('Formatter for this file type ({}) not found.'.format(
                formatter.syntax))
        return

    if (saving and not formatter.format_on_save_enabled()):
        return

    file_text = sublime.Region(0, view.size())
    file_text_utf = view.substr(file_text).encode('utf-8')
    if (len(file_text_utf) == 0):
        return

    stdout, stderr = formatter.format(file_text_utf)

    if len(stderr) == 0 and len(stdout) > 0:
        view.replace(edit, file_text, stdout)
    elif not quiet:
        show_error('Format error:\n' + stderr)


def console_write(text, prefix=False):
    if prefix:
        sys.stdout.write('FancyFormatter: ')
    sys.stdout.write(text + '\n')


def debug_write(text, prefix=False):
    console_write(text, True)


def show_error(text):
    sublime.error_message(u'FancyFormatter\n\n%s' % text)

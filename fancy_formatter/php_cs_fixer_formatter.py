# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

import os
import re
import subprocess
from .base import *
import tempfile


class PhpCsFixerFormatter(IBaseFormatter):

    def __init__(self, setting:ISettingReader, debug : bool ):
        self._setting = setting
        self._debug = debug

    def get_support_file_type(self)->List[EFileType]:
        support_list= [EFileType.PHP]
        ret=[]
        for syntax in self._setting.get("syntaxes"):
            ft = EFileType.from_string(syntax)
            if ft in support_list:
                ret.append(ft)
        return ret

    def format_text(self, file_type:EFileType, text:str) -> FormatResult:
        php_path = 'php'
        if self._setting.get("php_path"):
            php_path = self._setting.get("php_path")
            if not os.path.exists(php_path) or not os.path.isfile(php_path):
                return FormatResult.fatal_error(f"Can't find php path: {php_path}")                

        if self._setting.get("php55_compat"):
            return self._format_with_php55(text,php_path)
        else:
            return self._format_text_with_cs_fixer(text,php_path)
    
    def _format_text_with_cs_fixer(self, text:str,php_path:str)->FormatResult:
        cmd = []
        cmd.append(str(php_path))       

        setting_reader = self._setting.create_sub("php_cs_fixer")
        formatter_path = setting_reader.get("path")
        if not os.path.exists(formatter_path) or not os.path.isfile(formatter_path):
            return FormatResult.fatal_error(f"Can't find php_cs_fixer.path: {formatter_path}")
        cmd.append(formatter_path)
        cmd.append("--quiet")
        cmd.append("--using-cache=no")
        cmd.append("fix")

        with tempfile.NamedTemporaryFile(mode='w', suffix=".php", delete=False) as temp_file:
            temp_file.write(text)
            temp_file_name = temp_file.name       

        cmd.append(temp_file_name)
        if self._debug:
            print(" ".join(cmd))
        try:            
            startupinfo = self._get_hidden_startupinfo()
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                startupinfo=startupinfo
                )           

            if result.returncode != 0:
                return FormatResult("",result.stderr)
            
            with open(temp_file_name, "r", encoding="utf-8") as f:
                return FormatResult(f.read())            
        except subprocess.CalledProcessError as e:
            return FormatResult.from_subprocess_exception(e)
        except Exception as e:
            return FormatResult.from_exception(e) 
        finally:
            if os.path.exists(temp_file_name):
                os.remove(temp_file_name)

    def _format_with_php55(self, text:str,php_path:str) -> FormatResult:
        cmd = []
        cmd.append(str(php_path))
        cmd.append('-ddisplay_errors=stderr')
        cmd.append('-dshort_open_tag=On')

        setting_reader = self._setting.create_sub("php55")

        formatter_path = setting_reader.get("path")
        if not os.path.exists(formatter_path) or not os.path.isfile(formatter_path):
            return FormatResult.fatal_error(f"Can't find fmt_pchar_path: {formatter_path}")
        cmd.append(formatter_path)

        if setting_reader.get("psr1"):
            cmd.append('--psr1')
        if setting_reader.get("psr1_naming"):
            cmd.append('--psr1-naming')
        if setting_reader.get("psr2"):
            cmd.append('--psr2')

        indent_with_space = setting_reader.get("indent_with_space")
        if indent_with_space is True:
            cmd.append('--indent_with_space')
        elif indent_with_space > 0:
            cmd.append('--indent_with_space=' + str(indent_with_space))

        if setting_reader.get("enable_auto_align"):
            cmd.append('--enable_auto_align')

        if setting_reader.get("visibility_order"):
            cmd.append('--visibility_order')

        if setting_reader.get("smart_linebreak_after_curly"):
            cmd.append('--smart_linebreak_after_curly')

        passes =setting_reader.get("passes")
        if len(passes) > 0:
            cmd.append('--passes=' + ','.join(passes))

        excludes =setting_reader.get("excludes")   
        if len(excludes) > 0:
            cmd.append('--exclude=' + ','.join(excludes))

        cmd.append('-')
        return execute_with_pipe(cmd,text)
    
    def _get_hidden_startupinfo(self):
        if os.name=="nt":
            startupinfo = subprocess.STARTUPINFO()
            # 设置窗口隐藏标志
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            return startupinfo
        return None

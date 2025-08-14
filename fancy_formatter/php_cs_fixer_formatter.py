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
        self._support_file_type_list :List[EFileType]= [EFileType.PHP]

    def get_support_file_type(self)->List[EFileType]:        
        return self._support_file_type_list 

    def format_text(self, file_type:EFileType, text:str) -> FormatResult:
        php_path = 'php'
        if self._setting.get("php_path"):
            php_path = self._setting.get("php_path")
            if not os.path.exists(php_path) or not os.path.isfile(php_path):
                return FormatResult.fatal_error(f"Can't find php path: {php_path}")                

        cmd = []
        cmd.append(str(php_path))
        cmd.append('-ddisplay_errors=stderr')
        cmd.append('-dshort_open_tag=On')

        formatter_path = self._setting.get("path")
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
    
    def _get_hidden_startupinfo(self):
        if os.name=="nt":
            startupinfo = subprocess.STARTUPINFO()
            # 设置窗口隐藏标志
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            return startupinfo
        return None

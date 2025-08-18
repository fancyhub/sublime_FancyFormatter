# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

from .base import *
from typing import Dict
import tempfile


class CustomFormatter(IBaseFormatter):
    _support_syntax_list: List[str] = None

    def __init__(self, name: str, setting: ISettingReader, debug: bool):
        super().__init__(name, setting, debug)
        self._placeholder_map:Dict[str,str]={}

    def is_support(self, syntax: str) -> bool:
        if self._support_syntax_list == None:
            self._support_syntax_list = []
            support_syntaxes: list[str] = self._setting.get("support_syntaxes")
            for item in support_syntaxes:
                temp = item.strip().lower()
                if temp:
                    self._support_syntax_list.append(temp)

        return syntax in self._support_syntax_list

    def get_name(self) -> str:
        return "custom." + self._name

    def format_text(self, text: str, syntax: str) -> FormatResult:
        # check exe path
        exe_path = self._setting.get("exe_path")
        if not exe_path:
            return FormatResult.fatal_error(f"Can't find formatter custom.{self._name}.exe_path: {exe_path}")

        # compose cmd
        cmd = []
        cmd.append(exe_path)
        args: List[str] = self._setting.get("args")
        for item in args:
            keywords= self._extract_keywords(item)
            for key_word in keywords:
                placeholder= self._get_placeholder(key_word,syntax)
                if placeholder == None:
                    return FormatResult.fatal_error(f"Can't find {key_word}.{syntax} in custom.{self._name}")
                else:
                    item = item.replace("{"+key_word+"}",placeholder)
            
            cmd.append(item)             

        # create temp file
        need_temp_file: bool = self._setting.get("need_create_template_file")
        result_from_file: bool = self._setting.get("result_from_template_file")
        temp_file_name: str = None
        if need_temp_file:
            file_ext = self._get_placeholder("file_ext",syntax)
            if file_ext == None:
                return FormatResult.fatal_error(f"Can't find file_ext.{syntax} in custom.{self._name}")
            with tempfile.NamedTemporaryFile(mode="w", suffix=f".{file_ext}", delete=False) as temp_file:
                temp_file.write(text)
                temp_file_name = temp_file.name
                cmd.append(temp_file_name)
        else:
            result_from_file = False

        # print cmd
        if self._debug:
            print("Exe: " + " ".join(cmd))

        try:
            result: subprocess.CompletedProcess = None
            if need_temp_file:
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    startupinfo=self._get_startupinfo(),
                )
            else:
                result = subprocess.run(
                    cmd,
                    input=text.encode("utf-8"),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    startupinfo=self._get_startupinfo(),
                )
            if result_from_file:
                stdout = None
                with open(temp_file_name, "r") as file:
                    stdout = file.read()
                stderr = result.stderr
                if hasattr(stderr, "decode"):
                    stderr = stderr.decode("UTF-8", "ignore")
                return FormatResult(stdout, stderr)
            else:
                return FormatResult.from_subprocess_result(result)
        except subprocess.CalledProcessError as e:
            return FormatResult.from_subprocess_exception(e)
        except FileNotFoundError as e:
            if e.filename:
                return FormatResult.fatal_error(f"{e.strerror} : {e.filename} {e.filename2}")
            else:
                return FormatResult.fatal_error(f"{e.strerror} : {cmd[0]} ?")
        except Exception as e:
            return FormatResult.from_exception(e)
        finally:
            if need_temp_file and self._setting.get("keep_template_file") != False and os.path.exists(temp_file_name):
                os.remove(temp_file_name)

    def _get_startupinfo(self):
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            return startupinfo
        else:
            return None
        
    def _extract_keywords(self,text)->List[str]:
        # 正则表达式：仅捕获 { 和 } 之间的内容（非贪婪模式）
        pattern = r"\{(.*?)\}"  # 括号 () 表示捕获组，只提取内部内容
        keywords = re.findall(pattern, text)
        return keywords
    
    def _get_placeholder(self, key:str,syntax:str) -> str:
        composed_key = f"{key}.{syntax}"
        if composed_key in self._placeholder_map:
            return self._placeholder_map[composed_key]
        
        key_value_map = self._setting.get(f"{key}")
        if not key_value_map:
            return None        
        
        if not isinstance(key_value_map, dict):
            return None
        if syntax not in key_value_map:
            return None

        value = key_value_map[syntax]
        value = str(value)
        self._placeholder_map[composed_key] =value
        return value
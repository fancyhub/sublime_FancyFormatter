# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

from .base import *
from typing import Dict



# https://prettier.io/
# https://prettier.io/docs/install
# https://prettier.io/playground/
class PrettierFormatter:

    def __init__(self, setting:ISettingReader, debug : bool ):
        self._setting = setting
        self._debug = debug
        self._parser_map :Dict[EFileType,str]= {
            EFileType.HTML: "html",

            EFileType.TS: "typescript",
            EFileType.JS: "javascript",
            EFileType.JSON: "json5",

            EFileType.MD:"markdown",

            EFileType.CSS:"css",
            EFileType.LESS:"less",
            EFileType.SCSS:"scss",

            EFileType.YAML:"yaml",
        }

    def get_support_file_type(self)->List[EFileType]:
        support_list= [
            EFileType.HTML,
            EFileType.TS,EFileType.JS,EFileType.JSON,
            EFileType.MD,
            EFileType.CSS,EFileType.LESS,EFileType.SCSS,
            EFileType.YAML]
        ret=[]
        for syntax in self._setting.get("syntaxes"):
            ft = EFileType.from_string(syntax)
            if ft in support_list:
                ret.append(ft)
        return ret

    def format_text(self, file_type:EFileType, text:str) -> Tuple[str,str]:

        cmd=[]
        if os.name == 'nt':
            cmd.append("prettier.cmd")
        else:
            cmd.append("prettier")
        cmd.append("--parser")
        cmd.append(self._parser_map[file_type])

        options_reader = self._setting.create_sub("option")
        for key in options_reader.get_keys():
            value = options_reader.get(key)            
            if isinstance(value, bool):
                if value:
                    cmd.append(f"--{camel_to_kebab(key)}")
            else:
                cmd.append(f"--{camel_to_kebab(key)}")
                cmd.append(str(value))

        if self._debug:
            print(" ".join(cmd))
        return execute_with_pipe(cmd, text)
        
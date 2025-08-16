# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

from .base import *
from typing import Dict



# https://prettier.io/
# https://prettier.io/docs/install
# https://prettier.io/playground/
class PrettierFormatter(IBaseFormatter):

    def __init__(self,  name: str,setting:ISettingReader, debug : bool ):
        super().__init__(name,setting,debug)
        self._parser_map :Dict[str,str]= {
            "xml": "html",             
            "json": "jsonc"
        }

        self._support_syntax_list :List[str]= [
            "html","xml",
            "typescript","javascript","json",
            "markdown",
            "css","less","scss",
            "yaml"]

    def is_support(self,syntax:str)->bool:         
        return syntax in self._support_syntax_list 

    def format_text(self, text:str,syntax:str) -> FormatResult:

        cmd=[]
        exe_path = self._setting.get("exe_path")
        if exe_path:
            if not os.path.exists(exe_path) or not os.path.isfile(exe_path):
                return FormatResult.fatal_error(f"Can't find prettier exe path: {exe_path}")
        else:
            if os.name == 'nt':
                exe_path="prettier.cmd"
            else:
                exe_path="prettier"

        
        cmd.append(exe_path)
        cmd.append("--parser")
        if syntax in self._parser_map:
            cmd.append(self._parser_map[syntax])
        else:
            cmd.append(syntax)

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
        
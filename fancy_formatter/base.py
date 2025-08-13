# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

from enum import Enum, auto, unique
from typing import List,Tuple
import subprocess
import os
import re

@unique
class FileType(Enum):
    NONE = 0    
    C = auto()
    CPP = auto()
    PHP = auto()
    JSON = auto()
    JS = auto()
    TS = auto()
    HTML=auto()
    XML=auto()
    ASP=auto()
    PY =auto()
    CSS = auto()
    LESS =auto()
    SCSS =auto()
    SASS =auto()
    CS =auto()
    PROTO=auto()
    GO =auto()
    JAVA=auto()
    M=auto()
    MM=auto()
    MAX = auto()


    @classmethod
    def from_string(cls, s: str):
        s_upper = s.upper()
        for member in cls.__members__:
            if member == s_upper:
                return cls[member]
        print(f"Invalid FileType: {s} ")
        return FileType.NONE    

    def get_suffix(self)->str:
        if self.value <= FileType.NONE.value or self.value >= FileType.MAX.value:
            return ""
        else:
            return self.name.lower()

class EFormatResult(Enum):
    OK = 0,
    ERROR = 1,
    Fatal = 2,

class FormatResult:
    def __init__(self, stdout:str="", stderr:str=""):
        self.Code : EFormatResult = EFormatResult.OK
        self.Result :str =stdout
        self.ErrorMsg :str =stderr
    
        if stderr:
            self.Code = EFormatResult.ERROR
            self.ErrorMsg = stderr

    def print(self):
        if self.Code == EFormatResult.OK:
            print(self.Result)
        elif self.Code == EFormatResult.ERROR:
            print(f"FancyFormatter Error:\n {self.ErrorMsg}")
        elif self.Code==  EFormatResult.Fatal:
            print(f"FancyFormatter Fatal: \n {self.ErrorMsg}")

    @classmethod
    def normal_error(cls:str,msg:str)->'FormatResult':
        return FormatResult(stderr=msg)
    
    @classmethod
    def fatal_error(cls:str,msg:str)->'FormatResult':
        result = FormatResult()
        result.Code = EFormatResult.Fatal
        result.ErrorMsg = msg
        return result

    @classmethod
    def from_subprocess_exception(cls:str,e:subprocess.CalledProcessError)->'FormatResult':
        result = FormatResult()
        result.Code = EFormatResult.Fatal
        stderr = e.stderr    
        if hasattr(stderr, 'decode'):
            stderr= stderr.decode('UTF-8', 'ignore')
        result.ErrorMsg = stderr
        return result

    @classmethod
    def from_exception(cls:str,e:Exception)->'FormatResult':
        result = FormatResult()
        result.Code = EFormatResult.Fatal
        result.ErrorMsg = f"{e.__class__.__name__}:{str(e)}"
        return result

    @classmethod
    def from_subprocess_result(cls:str,p:subprocess.CompletedProcess)->'FormatResult':  
        stdout = p.stdout
        if hasattr(stdout, 'decode'):
            stdout= stdout.decode('UTF-8', 'ignore')

        stderr = p.stderr        
        if hasattr(stderr, 'decode'):
            stderr= stderr.decode('UTF-8', 'ignore')

        return FormatResult(stdout,stderr)
    
    


def execute_with_pipe(args:List[str], text:str)->FormatResult:
    startupinfo=None
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()        
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
    try:
        p = subprocess.run(args,
            input=text.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            startupinfo=startupinfo
        )
        return FormatResult.from_subprocess_result(p)
    except subprocess.CalledProcessError as e:
        return FormatResult.from_subprocess_exception(e)        
    except Exception as e:
        return FormatResult.from_exception(e)        
    

class IBaseFormatter:
    def get_support_file_type(self)->List[FileType]:
        pass 

    def format_text(self, file_type:FileType,text:str) -> FormatResult:
        return "","error: not implemented"

    def format_file(self,file_type:FileType,file_path:str)->str:
        return "error: not implemented"

    

class ISettingReader:
    def create_sub(self, prefix:str)->'ISettingReader':
        pass
        
    def get(self, key:str, fall_back_key:str=None, defaultVal=""):
        pass 

class SubSettingReader(ISettingReader):
    def __init__(self, orig:ISettingReader,prefix:str):
        self._orig = orig
        self._prefix = prefix

    def create_sub(self, prefix:str)->ISettingReader:        
        return SubSettingReader(self,prefix)
        

    def get(self, key:str, fall_back_key:str=None, defaultVal=""):
        real_key= f"{self._prefix}.{key}"
        real_fall_back_key = None
        if fall_back_key:
            real_fall_back_key = f"{self._prefix}.{fall_back_key}"
        return self._orig.get(real_key, real_fall_back_key)


class JsonSettingReader(ISettingReader):
    def __init__(self, json_data:dict):
        self._json_data = json_data

    def reset_data(self,json_data:dict):
        self._json_data = json_data

    def create_sub(self, prefix:str)->ISettingReader:
       return SubSettingReader(self, prefix)

    def _is_empty_value(self,key:str)->bool:    
        if key not in self._json_data:
            return True
        
        value = self._json_data[key]
        if value is None:
            return True        
        
        if isinstance(value, str) and value == "":
            return True
        return False
    
    def get(self, key:str, fall_back_key:str=None,defaultVal=""):
        if not self._is_empty_value(key):
            return self._json_data[key]
                
        if fall_back_key and not self._is_empty_value(fall_back_key):
            return self._json_data[fall_back_key]
        return defaultVal
    

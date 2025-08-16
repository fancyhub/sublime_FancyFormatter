# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

from .base import *
import tempfile

class CustomFormatter(IBaseFormatter):
    _support_file_type_list :List[EFileType]=None

    def __init__(self,  name: str,setting:ISettingReader, debug : bool ):
        super().__init__(name,setting,debug)

    def is_support(self,file_type:EFileType)->bool:
        if self._support_file_type_list==None:
            self._support_file_type_list=[]
            for item in self._setting.get("file_types"):
                self._support_file_type_list.append(EFileType.from_suffix(item))

        return file_type in self._support_file_type_list 
    
    def get_name(self)->str:
        return "custom."+self._name
    
    def format_text(self, file_type:EFileType, text:str) -> Tuple[str,str]:

        # check exe path    
        exe_path = self._setting.get("exe_path")
        if not exe_path:
            return FormatResult.fatal_error(f"Can't find formatter custom.{self._name}.exe_path: {exe_path}")

        # compose cmd
        cmd=[]   
        cmd.append(exe_path)
        args:List[str]=self._setting.get("args")
        for item in args:
            cmd.append(item.replace("{file_type}",file_type.get_suffix()))
        

        # create temp file
        need_temp_file:bool= self._setting.get("need_create_template_file")
        result_from_file:bool= self._setting.get("result_from_template_file")
        temp_file_name:str=None
        if need_temp_file:
            with tempfile.NamedTemporaryFile(mode='w', suffix=f".{file_type.get_suffix()}", delete=False) as temp_file:
                temp_file.write(text)
                temp_file_name = temp_file.name
                cmd.append(temp_file_name)
        else:
            result_from_file=False

        # print cmd
        if self._debug:
            print("Exe: "+" ".join(cmd))

        try:
            result :subprocess.CompletedProcess=None
            if need_temp_file:
                result = subprocess.run(cmd,                    
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    startupinfo=self._get_startupinfo()
                )
            else:
                result = subprocess.run(cmd,
                    input=text.encode("utf-8"),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    startupinfo=self._get_startupinfo()
                )
            if result_from_file:
                stdout=None
                with open(temp_file_name, 'r') as file:
                    stdout = file.read()
                stderr = result.stderr    
                if hasattr(stderr, 'decode'):
                    stderr= stderr.decode('UTF-8', 'ignore')
                return FormatResult(stdout,stderr)
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
            if need_temp_file and not self._setting.get("keep_template_file")==False and os.path.exists(temp_file_name):
                os.remove(temp_file_name)     
        
    def _get_startupinfo(self):
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()        
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            return startupinfo
        else:
            return None

        
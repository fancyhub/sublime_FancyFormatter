# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

 
from .base import * 
directory = os.path.dirname(os.path.realpath(__file__))
libs_path = os.path.join(directory, 'lib')

if libs_path not in sys.path:
    sys.path.append(libs_path)

use_bs4 = True
try:
    from bs4 import BeautifulSoup
except:
    use_bs4 = False


class BeautifulSoupFormatter(IBaseFormatter):

    def __init__(self, setting:ISettingReader, debug : bool ):
        self._setting = setting
        self._debug = debug

    def get_support_file_type(self)->List[FileType]:
        if not use_bs4:
            return []
        
        support_list= [FileType.HTML,FileType.ASP,FileType.XML]
        ret=[]
        for syntax in self._setting.get("syntaxes"):
            ft = FileType.from_string(syntax)
            if ft in support_list:
                ret.append(ft)
        return ret    

    def format_text(self, file_type:FileType, text:str) -> FormatResult:
        p_indent_size = self._setting.get("indent_size")
        
        try:
            soup = BeautifulSoup(text, 'html.parser')
            return FormatResult(soup.prettify(formatter=None, indent_size=p_indent_size))
        except Exception as e:
            return FormatResult.from_exception(e)
     
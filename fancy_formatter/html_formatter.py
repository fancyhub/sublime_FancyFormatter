# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

 
from .base import * 
from .lib.htmlbeautifier import *

directory = os.path.dirname(os.path.realpath(__file__))
libs_path = os.path.join(directory, 'lib')

if libs_path not in sys.path:
    sys.path.append(libs_path)

use_bs4 = True
try:
    from bs4 import BeautifulSoup
except:
    use_bs4 = False


class HtmlFormatter(IBaseFormatter):

    def __init__(self, setting:ISettingReader, debug : bool ):
        self._setting = setting
        self._debug = debug

    def get_support_file_type(self)->List[FileType]:
        support_list= [
            FileType.HTML,FileType.ASP,FileType.XML]
        ret=[]
        for syntax in self._setting.get("syntaxes"):
            ft = FileType.from_string(syntax)
            if ft in support_list:
                ret.append(ft)
        return ret    

    def format_text(self, file_type:FileType, text:str) -> FormatResult:
        if self._setting.get("use_beautiful_soup"):           
            return self._format_with_bs4(text)            
        return self._format_with_beautifier(text)
    
    def _format_with_bs4(self, text:str)-> FormatResult:

        p_indent_size = self._setting.get("indent_size")
        
        try:
            soup = BeautifulSoup(text, 'html.parser')
            return FormatResult(soup.prettify(formatter=None, indent_size=p_indent_size))
        except Exception as e:
            return FormatResult.from_exception(e)
        
    def _format_with_beautifier(self, text:str)-> FormatResult:

        options=default_options()
        keys = [            
            'indent_size',
            'indent_char',
            'minimum_attribute_count',
            'first_attribute_on_new_line',
            'indent_with_tabs',
            'expand_tags',
            'reduce_empty_tags',
            'reduce_whole_word_tags',
            'exception_on_tag_mismatch',
            'custom_singletons',
            'format_on_save'
        ]

        bs_setting = self._setting.create_sub("beautiful_soup")
        for key in keys:             
            setattr(options, key, bs_setting.get(key))

        try:
            return FormatResult(beautify(text, options))
        except Exception as e:
            return FormatResult.from_exception(e)
 
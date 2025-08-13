# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)


from .lib.jsbeautifier import *
from .base    import * 

# https://pypi.org/project/jsbeautifier/
class JsBeautifierFormatter(IBaseFormatter):

    def __init__(self, setting:ISettingReader, debug : bool ):
        self._setting = setting
        self._debug = debug

    def get_support_file_type(self)->List[FileType]:
        support_list= [FileType.JS,FileType.JSON]
        
        ret=[]
        for syntax in self._setting.get("syntaxes"):
            ft = FileType.from_string(syntax)
            if ft in support_list:
                ret.append(ft)
        return ret

    def format_text(self, file_type:FileType, text:str) -> FormatResult:        
        options = default_options()
        keys=[
            'indent_size',
            'indent_char',
            'indent_with_tabs',
            'eol',
            'preserve_newlines',
            'max_preserve_newlines',
            'space_in_paren',
            'space_in_empty_paren',
            'e4x',
            'jslint_happy',
            'brace_style',
            'keep_array_indentation',
            'keep_function_indentation',
            'eval_code',
            'unescape_strings',
            'wrap_line_length',
            'break_chained_methods',
            'end_with_newline',
            'comma_first',
            'space_after_anon_function',
            'unindent_chained_methods',
            'operator_position'
        ]

        keys=[
            'indent_size',        
            'wrap_line_length',
            'end_with_newline',
        ]
        for key in keys:
            setattr(options, key, self._setting.get(key))
         
        try:
            return FormatResult(beautify(text, options))
        except Exception as e:
            return FormatResult.from_exception(e)
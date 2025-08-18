# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)

from .lib.cssbeautifier import *
from .base import *


class ScssbeautifierFormatter(IBaseFormatter):

    def __init__(self, name: str, setting: ISettingReader, debug: bool):
        super().__init__(name, setting, debug)
        self._support_syntax_list: List[str] = ["scss", "sass"]

    def is_support(self, syntax: str) -> bool:
        return syntax in self._support_syntax_list

    def format_text(self, text: str, syntax: str) -> FormatResult:

        options = default_options()
        option_reader = self._setting.create_sub("option")
        for key in option_reader.get_keys():
            setattr(options, key, option_reader.get(key))

        try:
            return FormatResult(beautify(text, options))
        except Exception as e:
            return FormatResult.from_exception(e)

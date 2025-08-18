# @author       Cunyu Fan
# @time         2025-08-13
# @license      The MIT License (MIT)


from .base import *

directory = os.path.dirname(os.path.realpath(__file__))
libs_path = os.path.join(directory, "lib")

if libs_path not in sys.path:
    sys.path.append(libs_path)

use_bs4 = True
try:
    from bs4 import BeautifulSoup
except:
    use_bs4 = False


class BeautifulSoupFormatter(IBaseFormatter):

    def __init__(self, name: str, setting: ISettingReader, debug: bool):
        super().__init__(name, setting, debug)
        self._support_syntax_list: List[str] = ["html", "xml"]

    def is_support(self, syntax: str) -> bool:
        if not use_bs4:
            return False
        return syntax in self._support_syntax_list

    def format_text(self, text: str, syntax: str) -> FormatResult:
        p_indent_size = self._setting.get("indent_size")

        try:
            soup = BeautifulSoup(text, "html.parser")
            return FormatResult(
                soup.prettify(formatter=None, indent_size=p_indent_size)
            )
        except Exception as e:
            return FormatResult.from_exception(e)

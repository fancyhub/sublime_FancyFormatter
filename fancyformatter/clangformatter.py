import re
import sys 
import os
import sublime
import subprocess
import tempfile

class ClangFormatter:

    def __init__(self, formatter):
        self.formatter = formatter
        self.opts = formatter.settings.get('formatter_clang_options')        

    def format(self, syntax, text):

       
        stderr = ''
        stdout = ''

        file_ext=".cs"
        if syntax == "c#":
            file_ext="cs"
        elif syntax == "java":
            file_ext="java"
        elif syntax == "javascript":
            file_ext="js"
        elif syntax == "typescript":
            file_ext="ts"
        elif syntax == "json":
            file_ext="json"
        elif syntax == "objective-c":
            file_ext="m"
        elif syntax == "objective-c++":
            file_ext="mm"
        if syntax == "c++":
            file_ext="cpp"
        elif syntax == "c":
            file_ext="c"
        

        style ="Microsoft"
        if ('style' in self.opts and self.opts['style']):
            style=self.opts['style']
        
        style_key=f'style_{file_ext}'        
        if (style_key in self.opts and self.opts[style_key]):
            style = self.opts[style_key]

        print(f"syntax {syntax}, style: {style}")
        text = text.decode('utf-8')
        with tempfile.NamedTemporaryFile(mode='w', suffix=f".{file_ext}", delete=False) as temp_file:
            temp_file.write(text)
            temp_file_name = temp_file.name

        try:
            startupinfo = self._get_hidden_startupinfo()
            result = subprocess.run(
                ["clang-format", f"-style={style}", temp_file_name],
                capture_output=True,
                text=True,
                check=True,
                startupinfo=startupinfo
                )             
            os.unlink(temp_file_name)

            return result.stdout, result.stderr
        except Exception as e:
            stderr = str(e)

        if (not stderr and not stdout):
            stderr = 'Formatting error!'

        return stdout, stderr

    def _get_hidden_startupinfo(self):
        if sys.platform.startswith('win32'):
            startupinfo = subprocess.STARTUPINFO()
            # 设置窗口隐藏标志
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            return startupinfo
        return None

    def format_on_save_enabled(self, _):
        format_on_save = False
        if ('format_on_save' in self.opts and self.opts['format_on_save']):
            format_on_save = self.opts['format_on_save']
        if (isinstance(format_on_save, str)):
            format_on_save = re.search(format_on_save, file_name) is not None
        return format_on_save
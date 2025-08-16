
if __name__ == "__main__":
    import json5 
    from typing import Dict
    from fancy_formatter.base import *
    from fancy_formatter.FancyFormatter import FancyFormatter

    def read_file_to_string(file_path):      
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return content
        except FileNotFoundError:
            print(f"Error: '{file_path}' not found")
        except PermissionError:
            print(f"Error: no read permission '{file_path}'")
        except UnicodeDecodeError:
            print(f"Error: '{file_path}' is not encoded with UTF-8")
        except Exception as e:
            print(f"Error: {str(e)}")
        return None

    def load_json_file(file_path):     
        try:            
            with open(file_path, 'r', encoding='utf-8') as file:
                json_data = json5.load(file)
                return json_data
        except FileNotFoundError:
            print(f"Error:  '{file_path}' not exist")
        except json5.JSONDecodeError:
            print(f"Error:  '{file_path}' is not a json file")
        except Exception as e:
            print(f"Error: {str(e)}")
        return None

    data = load_json_file("FancyFormatter.sublime-settings")
    data["debug"]=True
    reader = JsonSettingReader(data)
    formatter = FancyFormatter(reader)

    test_dict:Dict[str,str] = {
        # "css":"xxx.css",
        # "html":"xxx.html",
        # "xml":"xxx.xml",
        # "javascript":"xxx.js",
        # "typescript":"xxx.ts",
        # "json":"xxx.json",
        # "markdown":"xxx.md",
        # "yaml":"xxx.yaml",
        "python":__file__,
        "c#":r"C:\work\fancyhub\CmdLineGUI\CmdLineGUI\View\ExeView.cs",
    }

    for type, path in test_dict.items():
        content = read_file_to_string(path)
        result= formatter.format_text(type, content)
        print(f"Format: {type}")
        result.print()


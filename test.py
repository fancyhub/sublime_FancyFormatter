
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

    test_dict:Dict[EFileType,str] = {
        # EFileType.CSS:"xxx.css",
        # EFileType.HTML:"xxx.html",
        # EFileType.JS:"xxx.js",
        # EFileType.TS:"xxx.ts",
        # EFileType.JSON:"xxx.json",
        # EFileType.MD:"xxx.md",
        # EFileType.YAML:"xxx.yaml",
        # EFileType.LESS:"xxx.less",
        # EFileType.SCSS:"xxx.scss",  
        # EFileType.PY:__file__,
        EFileType.CS:r"C:\work\fancyhub\CmdLineGUI\CmdLineGUI\View\ExeView.cs",
    }

    for type, path in test_dict.items():
        content = read_file_to_string(path)
        result= formatter.format_text(type, content)
        print(f"Format: {type}")
        result.print()

    for type_name in EFileType.__members__:
        file_type =EFileType.from_suffix(type_name)
        if file_type == EFileType.NONE or file_type==EFileType.MAX:
            continue

        print(f"----------------- Format: {file_type} -----------------")
        result= formatter.format_text(file_type, " ")
        result.print()
        print("\n\n")


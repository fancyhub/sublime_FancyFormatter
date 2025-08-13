
if __name__ == "__main__":
    import json5 
    from fancy_formatter.base import *
    from fancy_formatter.FancyFormatter import FancyFormatter

    def read_file_to_string(file_path):
        """
        读取文件内容并返回为字符串
        
        参数:
            file_path (str): 文件的路径
            
        返回:
            str: 文件内容，如果出错则返回None
        """
        try:
            # 使用with语句打开文件，确保文件会被正确关闭
            with open(file_path, 'r', encoding='utf-8') as file:
                # 读取全部内容为字符串
                content = file.read()
                return content
        except FileNotFoundError:
            print(f"错误: 文件 '{file_path}' 未找到")
        except PermissionError:
            print(f"错误: 没有权限读取文件 '{file_path}'")
        except UnicodeDecodeError:
            print(f"错误: 文件 '{file_path}' 不是有效的UTF-8编码文件")
        except Exception as e:
            print(f"读取文件时发生错误: {str(e)}")
        return None

    def load_json_file(file_path):
        """
        加载并解析JSON文件
        
        参数:
            file_path (str): JSON文件的路径
            
        返回:
            dict: 解析后的JSON数据，如果出错则返回None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                # 加载并解析JSON数据
                json_data = json5.load(file)
                return json_data
        except FileNotFoundError:
            print(f"错误: 文件 '{file_path}' 不存在")
        except json5.JSONDecodeError:
            print(f"错误: 文件 '{file_path}' 不是有效的JSON格式")
        except Exception as e:
            print(f"加载JSON文件时发生错误: {str(e)}")
        return None

    data = load_json_file("FancyFormatter.sublime-settings")
    reader = JsonSettingReader(data)
    formatter = FancyFormatter(reader)

    content= read_file_to_string(r"C:\Users\cunyu.fan\Desktop\sublimetext-codeformatter-master\tests\data\css\test.css")
    content = read_file_to_string(__file__)
    content = read_file_to_string("Main.py")
    content = read_file_to_string(r"C:\Users\cunyu.fan\Downloads\FileReaderTest.php")
    unformatted_code = """
    def greet(name):
        return "Hello, " +name

    print( greet("World") )
    """
    result= formatter.format_text(FileType.HTML, content)
    result.print()
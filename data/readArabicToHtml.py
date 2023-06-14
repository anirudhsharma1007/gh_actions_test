
import os
import re

filesFolderPath = os.getcwd() + '\\data'

# def escape_special_characters(string):
#     special_characters = r"[!\"#$%&'()*+,\-.\/:;<=>?@\[\\\]^_`{|}~]"
#     escaped_string = re.sub(special_characters, lambda match: "\\" + match.group(0), string)
#     return escaped_string

def read_file_names(folder_path):
    file_names = []
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            file_names.append(str(file_name).split('.')[0].strip())
    return file_names

# Provide the folder path as an argument
# folder_path = "/path/to/folder"
folder_path = filesFolderPath
file_names = read_file_names(folder_path)

# Print the file names
for file_name in file_names:
    print(file_name)

def generate_file_list_html(folder_path):
    file_names = []
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            file_names.append(file_name)

    html_content = "<html>\n<body>\n<ul>\n"
    for file_name in file_names:
        file_path = os.path.join(folder_path, create_html_content(os.path.join(folder_path, file_name)))
        html_content += f"<li><a href='{file_path}'>{file_name}</a></li>\n"

    html_content += "</ul>\n</body>\n</html>"

    with open("file_list.html", "w") as html_file:
        html_file.write(html_content)
        
def create_html_content(file_name):
    
    html_content = "<html>\n<body>\n"

    with open(file_name,'r',encoding='utf-8') as read_file:
        data = read_file.read()
        html_content += data
    html_content += "\n</body>\n</html>"
    print(file_name.split('.')[0])
    with open(file_name.split('.')[0] + '.html','w',encoding='utf-8') as html_file:        
        html_file.write(html_content)
    return file_name.split('.')[0].split('\\')[-1] + '.html'


# Provide the folder path as an argument
# folder_path = "/path/to/folder"
generate_file_list_html(folder_path)

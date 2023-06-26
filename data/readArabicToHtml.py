
import os
import re
import arabic_reshaper
from bidi.algorithm import get_display

filesFolderPath = os.path.join(os.getcwd(),'data')

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
            if str(file_name).split('.')[-1] != 'html':
                file_names.append(file_name)

    html_content = "<html>\n<body>\n<ul>\n"
    for file_name in file_names:
        # file_path = os.path.join(folder_path, create_html_content(os.path.join(folder_path, file_name)))
        file_path = os.path.join(folder_path, create_html_content_with_h2_tag(os.path.join(folder_path, file_name)))
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
    html_content = re.sub(r"### |\s*\ (.+)", r"<h4>\1</h4>", html_content)
    print(file_name.split('.')[0])
    with open(file_name.split('.')[0] + '.html','w',encoding='utf-8') as html_file:        
        html_file.write(html_content)
    return file_name.split('.')[0].split('\\')[-1] + '.html'



def create_html_content_with_h2_tag(file_name):
    html_content = "<html>\n<body style=\"text-align: right;\">\n"

    with open(file_name, 'r', encoding='utf-8') as read_file:
        lines = read_file.readlines()

    arabic_h2 = True
    english_h3 = True
    citation_block = False
    citation_content = ''

    for line in lines:
        if line.startswith("#META#"):
            meta_line = line.lstrip("#META#").strip()
            if arabic_h2 and re.search("[\u0600-\u06FF]", meta_line):
                html_content += "<h1>" + meta_line + "</h1>"
                arabic_h2 = False
            elif english_h3 and re.search("[A-Za-z]", meta_line):
                html_content += "<h2>" + meta_line + "</h2>"
                english_h3 = False
        elif line.startswith("# @COMMENT:"):
            comment_text = line.lstrip("# @COMMENT:").strip()
            html_content += f"<button onclick=\"alert('{comment_text}')\">Comment</button>"
        elif re.search(r"# @[A-Za-z0-9_]+_BEG_", line):
            block_name = re.search(r"# @([A-Za-z0-9_]+)_BEG_", line).group(1)
            citation_block = True
            citation_content = ''
            words = line.strip().split()
            for i,word in enumerate(words):
                bidi_word = get_display(arabic_reshaper.reshape(word))
                citation_content += bidi_word + ' '
                if re.search(r"@"+block_name+"_END_", word):
                    citation_block = False
                    html_content += f"<button onclick=\"alert('{citation_content}');\">Citation ({block_name})</button>"
                    break
        
        elif citation_block:
            words = line.strip().split()
            for word in words:
                bidi_word = get_display(arabic_reshaper.reshape(word))
                citation_content += bidi_word + ' '
                if re.search(r"# @[A-Za-z0-9_]+_END_", word):
                    citation_block = False
                    html_content += f"<button onclick=\"displayCitation('{citation_content}');\">Citation ({block_name})</button>"
        elif line.startswith("### |||"):
            h6_line = line.lstrip("### |||").strip()
            html_content += "<h5>" + h6_line + "</h5>"
        elif line.startswith("### ||"):
            h5_line = line.lstrip("### ||").strip()
            html_content += "<h4>" + h5_line + "</h4>"
        elif line.startswith("### |"):
            h4_line = line.lstrip("### |").strip()
            html_content += "<h3>" + h4_line + "</h3>"
        else:
            html_content += line
    
    # html_content = re.sub(r"### |\s*\ (.+)", r"<h4>\1</h4>", html_content)
    html_content += "</p>\n</body>\n</html>"

    with open(file_name.split('.')[0] + '.html', 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    return file_name.split('.')[0].split('\\')[-1] + '.html'

# Provide the folder path as an argument
# folder_path = "/path/to/folder"
generate_file_list_html(folder_path)
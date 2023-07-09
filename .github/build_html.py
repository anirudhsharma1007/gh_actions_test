
import os
import re
import sys

import pandas as pd

tag_dict = {}
startTagDict = False

df = pd.read_excel(os.path.join(os.getcwd(),'Witness_list_sheet.xlsx'))
selected_columns = df[['Arabic name', 'Witness ']]
witness_dict = {}
for index, row in selected_columns.iterrows():
    key = row['Witness ']
    value = str(row['Arabic name'])
    witness_dict[key] = value


df = pd.read_excel(os.path.join(os.getcwd(),'Kevin Bibliography.xlsx'))
selected_columns = df[['ID', 'short_author', 'short_title']]
my_dict = {}
for index, row in selected_columns.iterrows():
    key = row['ID']
    value = str(row['short_author']) + ' , ' + str(row['short_title']) 
    my_dict[key] = value

patterns = {
    'prefix_pattern': r'V(\d+)',
    'suffix_pattern': r'P(\d+)([A-Z])'
}

filesFolderPath = os.path.join(os.getcwd(),'data')

# def escape_special_characters(string):
#     special_characters = r"[!\"#$%&'()*+,\-.\/:;<=>?@\[\\\]^_`{|}~]"
#     escaped_string = re.sub(special_characters, lambda match: "\\" + match.group(0), string)
#     return escaped_string

def read_file_names(folder_path):
    file_names = []
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            # file_names.append(str(file_name).split('.')[0].strip())
            file_names.append(str(file_name))
    return file_names

# Provide the folder path as an argument
# folder_path = "/path/to/folder"
folder_path = filesFolderPath
file_names = read_file_names(folder_path)

# # Print the file names
# for file_name in file_names:
#     print(file_name.encode('utf-8', errors='ignore').decode('utf-8'))


# def generate_file_list_html(folder_path):
#     file_names = []
#     for file_name in os.listdir(folder_path):
#         if os.path.isfile(os.path.join(folder_path, file_name)):
#             if str(file_name).split('.')[-1] != 'html':
#                 file_names.append(file_name)

#     html_content = "<html>\n<body>\n<ul>\n"
#     for file_name in file_names:
#         # file_path = os.path.join(folder_path, create_html_content(os.path.join(folder_path, file_name)))
#         file_path = os.path.join(folder_path, create_html_content_with_h2_tag(os.path.join(folder_path, file_name)))
#         html_content += f"<li><a href='{file_path}'>{file_name}</a></li>\n"

#     html_content += "</ul>\n</body>\n</html>"

#     with open("file_list.html", "w") as html_file:
#         html_file.write(html_content)
        
        
def generate_file_list_html(html_folder_path, relative_paths=True):
    """
    Create a html file that contains links to all converted text files
    
    Args:
        html_folder_path (str): path to folder containing generated html files
        relative_paths (bool): if False, absolute paths will be used
            for the links; this is useful for local testing.
            if True, relative paths will be used, which is 
            better for server/ GitHub Pages
    """
    # create a list of all html files in the html folder:
    file_names = []
    for file_name in os.listdir(html_folder_path):
        if os.path.isfile(os.path.join(html_folder_path, file_name)):
            if file_name.split('.')[-1] == 'html': 
                file_names.append(file_name)

    # initialize the content of the index.html file
    html_content = "<html>\n<header>\n</header>\n<body>\n<h1>Witnesses:</h1>\n<ul>\n" 

    # create a link to each html file:
    for file_name in file_names:
        if relative_paths:
            html_path = "html/"+file_name
        else:
            html_path = create_html_path(file_name, html_folder_path)
        html_content += f"<li><a href='{html_path}' target='_blank'>{file_name.split('.')[0]}</a></li>\n"

    html_content += "</ul>\n</body>\n</html>"

    root_folder = os.path.dirname(html_folder_path)
    index_fp = os.path.join(root_folder, "index.html")
    with open(index_fp, "w",encoding='utf-8') as html_file:
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
    startTagDict = False 
    html_content = "<html>\n<head>\n<style>\n"
    html_content += "body { text-align: right; background-color: #c2bcca;}\n"
    html_content += "h1 { color: #861; font-size: 24px; }\n"
    html_content += "h2 { color: #97926; font-size: 18px; }\n"
    html_content += "h3 { color: #4640c2; font-size: 16px; }\n"
    html_content += "h4 { color: #958427; font-size: 14px; }\n"
    html_content += "h5 { color: #1c201d; font-size: 12px; }\n"
    html_content += "</style>\n\n"

    with open(file_name, 'r', encoding='utf-8') as read_file:
    # with open("C:\\Users\\Anirudh Sharma\\Desktop\\testData.txt", 'r', encoding='utf-8') as read_file:
        lines = read_file.readlines()

    arabic_h2 = True
    english_h3 = True
    citation_block = False
    citation_content = ''

    for line in lines:
        if "#OpenITI-RKJ#" in line:
            continue
        line = re.sub(r"PageV(\d+)P(\d+)", r"<span title='vol \1 page \2'>§</span>", line)
        if line.startswith("#META#"):
            meta_line = line.lstrip("#META#").strip()
            if arabic_h2 and re.search("[\u0600-\u06FF]", meta_line):
                html_content += "<h1>" + meta_line + "</h1>"
                arabic_h2 = False
            elif english_h3 and re.search("[A-Za-z]", meta_line):
                html_content += "<h2>" + meta_line.replace("Transliterated Name:","") + "</h2>"
                english_h3 = False
        elif line.startswith("# @COMMENT:"):
            # comment_lines = line.lstrip("# @COMMENT:").strip()
            comment_lines = line.replace("# @COMMENT:", "").strip()
            comment_text = ''
            words = comment_lines.strip().split()
            for word in words:
                if word.startswith("#$"):
                    block_name = word[2:]
                    key = block_name[:4] 
                    remaining_tag = block_name[4:]
                    if key in my_dict:
                        value = my_dict[key]  # Get the corresponding value from the dictionary

                        # Replace the prefix pattern with 'volume <number>'
                        remaining_tag = re.sub(patterns['prefix_pattern'], r', vol. \1', remaining_tag)

                        # Replace the suffix pattern with 'page number <number><alphabet>'
                        remaining_tag = re.sub(patterns['suffix_pattern'], r', \1\2.', remaining_tag)

                        comment_text += value + remaining_tag + ' '
                    else:
                        comment_text += block_name + ' '
                elif word.startswith("wit_"):
                    key = word[4:9] 
                    if key in witness_dict:
                        value = witness_dict[key]  # Get the corresponding value from the dictionary

                        comment_text += value + ' '
                    else:
                        comment_text += word + ' '
                else:
                     comment_text += word + ' '
            html_content += f"<br><button onclick=\"alert('{comment_text}')\">Comment</button><br>"
        elif re.search(r"# @[A-Za-z0-9_]+_BEG_", line):
            block_name = re.search(r"# @([A-Za-z0-9_]+)_BEG_", line).group(1)
            key = block_name[:4] 
            remaining_tag = block_name[4:]

            citation_block = True
            citation_content = ''

            if key in my_dict:
                value = my_dict[key]  # Get the corresponding value from the dictionary

                # Replace the prefix pattern with 'volume <number>'
                remaining_tag = re.sub(patterns['prefix_pattern'], r', vol. \1', remaining_tag)

                # Replace the suffix pattern with 'page number <number><alphabet>'
                remaining_tag = re.sub(patterns['suffix_pattern'], r', \1\2.', remaining_tag)

                citation_content += value + remaining_tag
            else:
                citation_content += block_name

            quranCitation = False
            quranCitationContent = ''
            words = line.strip().split()
            for word in words:
                # bidi_word = get_display(arabic_reshaper.reshape(word))
                # html_content += bidi_word + ' '

                if word.startswith("VAR_"):
                    if startTagDict != True:
                        startTagDict = True
                        tag_dict[block_name] = ''
                    tag_dict[word[4:]] = ''

                if word.startswith("@QURS"):

                    if "_BEG" in word:
                        quranCitation = True
                        continue
                    elif "_END" in word:

                        vol_no = word[5:8]
                        col_no = word[9:12]
                        quranCitation = False
                        if block_name in tag_dict.keys():
                            tag_dict[block_name] += f"<span title=\"Qur\'an {vol_no}:{col_no}\"><u>{quranCitationContent}</u></span>"
                        html_content += f"<span title=\"Qur\'an {vol_no}:{col_no}\"><u>{quranCitationContent}</u></span>"
                        quranCitationContent = ''
                        continue


                if quranCitation:
                    quranCitationContent += word + ' '
                    continue
                if word.startswith("@TR"):
                    continue
                if re.search(r"@"+block_name+"_END_", word):
                    citation_block = False
                    if block_name in tag_dict.keys():
                        tag_dict[block_name] += f"<br><button onclick=\"alert('{citation_content}');\">Citation ({block_name})</button><br>"
                    html_content += f"<br><button onclick=\"alert('{citation_content}');\">Citation ({block_name})</button><br>"
                    break
                elif re.search(r"@"+block_name+"_BEG_", word):
                    continue
                elif re.search(r"@"+block_name+"_END_", word):
                    continue
                else:
                    if word != '#':
                        if block_name in tag_dict.keys():
                            tag_dict[block_name] += word + ' '
                        html_content += word + ' '
        
        elif citation_block:
            if word.startswith("VAR_"):
                    if startTagDict != True:
                        startTagDict = True
                        tag_dict[block_name] = ''
                    tag_dict[word[4:]] = ''
            if re.search(r"@"+block_name+"_END_", word):
                    citation_block = False
                    if block_name in tag_dict.keys():
                        tag_dict[block_name] += f"<br><button onclick=\"alert('{citation_content}');\">Citation ({block_name})</button><br>"
                    html_content += f"<br><button onclick=\"alert('{citation_content}');\">Citation ({block_name})</button><br>"
                    
            words = line.strip().split()
            for word in words:
                # bidi_word = get_display(arabic_reshaper.reshape(word))
                # html_content += bidi_word + ' '
                if word.startswith("@TR"):
                    continue
                if word.startswith("VAR_"):
                    if startTagDict != True:
                        startTagDict = True
                        tag_dict[block_name] = ''
                    tag_dict[word[4:]] = ''
                if re.search(r"@"+block_name+"_END_", word):
                    citation_block = False
                    if block_name in tag_dict.keys():
                        tag_dict[block_name] += f"<br><button onclick=\"alert('{citation_content}');\">Citation ({block_name})</button><br>"
                    html_content += f"<br><button onclick=\"alert('{citation_content}');\">Citation ({block_name})</button><br>"
                else:
                    if word != '#':
                        if block_name in tag_dict.keys():
                            tag_dict[block_name] += word + ' '
                        html_content += word + ' '

        elif line.startswith("### |||"):
            h6_line = line.lstrip("### |||").strip()
            
            match = re.search(r"\bSEE_\w+", h6_line)
            matched_citation_content = ''
            matchedWord = ''
            if match:
                matchedWord = match.group()
                key = matchedWord[4:8] 
                remaining_tag = matchedWord[8:]

                if key in my_dict:
                    value = my_dict[key]  # Get the corresponding value from the dictionary

                    # Replace the prefix pattern with 'volume <number>'
                    remaining_tag = re.sub(patterns['prefix_pattern'], r', vol. \1', remaining_tag)

                    # Replace the suffix pattern with 'page number <number><alphabet>'
                    remaining_tag = re.sub(patterns['suffix_pattern'], r', \1\2.', remaining_tag)

                    matched_citation_content += value + remaining_tag
                else:
                    matched_citation_content += matchedWord
            
            h6_line = re.sub(r"\bSEE_\w+", r"<span title='"+matched_citation_content+"'>"+matchedWord+"</span>", h6_line)
            html_content += "<h5>" + h6_line + "</h5>"
        elif line.startswith("### ||"):
            h5_line = line.lstrip("### ||").strip()
            match = re.search(r"\bSEE_\w+", h5_line)
            matched_citation_content = ''
            matchedWord = ''
            if match:
                matchedWord = match.group()
                key = matchedWord[4:8] 
                remaining_tag = matchedWord[8:]

                if key in my_dict:
                    value = my_dict[key]  # Get the corresponding value from the dictionary

                    # Replace the prefix pattern with 'volume <number>'
                    remaining_tag = re.sub(patterns['prefix_pattern'], r', vol. \1', remaining_tag)

                    # Replace the suffix pattern with 'page number <number><alphabet>'
                    remaining_tag = re.sub(patterns['suffix_pattern'], r', \1\2.', remaining_tag)

                    matched_citation_content += value + remaining_tag
                else:
                    matched_citation_content += matchedWord
            
            h5_line = re.sub(r"\bSEE_\w+", "<span title='"+matched_citation_content+"'>"+matchedWord+"</span>", h5_line)
            
            html_content += "<h4>" + h5_line + "</h4>"
        elif line.startswith("### |"):
            h4_line = line.lstrip("### |").strip()
            match = re.search(r"\bSEE_\w+", h4_line)
            matched_citation_content = ''
            matchedWord = ''
            if match:
                matchedWord = match.group()
                key = matchedWord[4:8] 
                remaining_tag = matchedWord[8:]

                if key in my_dict:
                    value = my_dict[key]  # Get the corresponding value from the dictionary

                    # Replace the prefix pattern with 'volume <number>'
                    remaining_tag = re.sub(patterns['prefix_pattern'], r', vol. \1', remaining_tag)

                    # Replace the suffix pattern with 'page number <number><alphabet>'
                    remaining_tag = re.sub(patterns['suffix_pattern'], r', \1\2.', remaining_tag)

                    matched_citation_content += value + remaining_tag
                else:
                    matched_citation_content += matchedWord
            
            h4_line = re.sub(r"\bSEE_\w+", "<span title='"+matched_citation_content+"'>"+matchedWord+"</span>", h4_line)
            
            html_content += "<h3>" + h4_line + "</h3>"
        else:
            html_content += line
    
    # html_content = re.sub(r"### |\s*\ (.+)", r"<h4>\1</h4>", html_content)
    html_content += "</p>\n</body>\n</html>"

    # with open(file_name.split('.')[0] + '.html', 'w', encoding='utf-8') as html_file:
    #     html_file.write(html_content)

    # return file_name.split('.')[0].split('\\')[-1] + '.html'
    return html_content

# Provide the folder path as an argument
# folder_path = "/path/to/folder"
# generate_file_list_html(folder_path)

def convert_to_html(text_file_path): 
    """
    Convert a single witness text file to html and store it in the html folder

    Args:
        text_file_path (str): path to a witness text file
    """

    # print("converting", text_file_path)
    
    # store the converted texts in a separate folder
    # (called "html", in the same parent folder as the data folder that contains the tex files)
    data_folder, text_file_name = os.path.split(text_file_path)
    parent_folder = os.path.dirname(data_folder)
    html_folder = os.path.join(parent_folder, "html")
    if not os.path.exists(html_folder):
        os.makedirs(html_folder)
    
    html_str = create_html_content_with_h2_tag(text_file_path)
    # save the witness html:
    html_fp = create_html_path(text_file_name, html_folder)
    with open(html_fp, mode="w", encoding="utf-8") as file:
        file.write(html_str)

    return html_fp

def create_html_path(file_name, html_folder):
    modifiedFileName = manual_transliterate(file_name)
    html_fn = modifiedFileName.split('.')[0] + '.html'
    html_path = os.path.join(html_folder, html_fn)
    return html_path

# def convert_file_name(file_name):
#     # Remove leading/trailing whitespaces
#     file_name = file_name.strip()
#     # Convert special characters to closest ASCII equivalent
#     file_name = unidecode(file_name)
#     # Replace spaces with hyphens
#     file_name = file_name.replace(' ', '-')
#     file_name = file_name.replace('.', '-')
#     return file_name

def manual_transliterate(string):
    special_characters = {
        'ā': 'a',
        'Á': 'A',
        'á': 'a',
        'Â': 'A',
        'â': 'a',
        'Ã': 'A',
        'ã': 'a',
        'Ä': 'A',
        'ä': 'a',
        'Å': 'A',
        'å': 'a',
        'Æ': 'AE',
        'æ': 'ae',
        'Ç': 'C',
        'ç': 'c',
        'È': 'E',
        'é': 'e',
        'É': 'E',
        'Ê': 'E',
        'ê': 'e',
        'Ë': 'E',
        'ë': 'e',
        'Ì': 'I',
        'í': 'i',
        'Í': 'I',
        'Î': 'I',
        'î': 'i',
        'Ï': 'I',
        'ï': 'i',
        'Ñ': 'N',
        'ñ': 'n',
        'Ò': 'O',
        'Ó': 'O',
        'ô': 'o',
        'Ô': 'O',
        'õ': 'o',
        'Õ': 'O',
        'Ö': 'O',
        'ö': 'o',
        'Ø': 'O',
        'ø': 'o',
        'Ù': 'U',
        'Ú': 'U',
        'Û': 'U',
        'ü': 'u',
        'Ý': 'Y',
        'ÿ': 'y',
        'ī': 'i',
        'ī': 'i',
        'ā': 'a'
        # Add more mappings as needed
    }
        # Replace special characters with their ASCII counterparts
    for char, repl in special_characters.items():
        string = string.replace(char, repl)
    
    # Replace spaces with hyphens
    string = string.replace(' ', '-')
    string = string.replace('.', '-')
    string = string.replace('\'', '-')
    string = re.sub(r'-+', '-', string)
    
    return string

def main():
    # get the file or folder path that is given as an argument in the module call
    # (see https://www.google.com/amp/s/www.geeksforgeeks.org/how-to-use-sys-argv-in-python/amp/)
    try:
        # path = sys.argv[1]
        path = filesFolderPath
    except:
        print("provide a path to a text file or the folder containing all text files")
        sys.exit(1) # abort the execution
    
    # Step 1: convert file(s) to html:
    if os.path.isdir(path):
        # if the argument is a folder, convert all files in it to html:
        for fn in os.listdir(path):
            fp = os.path.join(path, fn)
            html_path = convert_to_html(fp)
    elif os.path.isfile(path):
        # if the argument is a file, convert that file only:
        html_path = convert_to_html(path)
        
    else:
        print(path)
        print("is not a valid path to a file or folder")
        sys.exit(1) # abort the execution
        
    # Step 2: (re)generate the file containing links to all html files:
    html_folder = os.path.dirname(html_path)
    print("html_folder:", html_folder)
    generate_file_list_html(html_folder)
    
if __name__ == "__main__":
    main()
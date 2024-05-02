import re
from textnode import TextNode
from conversion import convert_type

valid_markdown = {
    "**": "bold",
    "*": "italic",
    "`": "code",
}


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    return_list = []
    

    for old_node in old_nodes:
        if old_node.text_type != valid_markdown["text_type_text"]:
            return_list.append(old_node)
        else:
            new_list = old_node.text.split(delimiter)
            for n,x in enumerate(new_list):
                if n % 2 == 0:
                    text_type_to_use = valid_markdown["text_type_text"]
                else:
                    text_type_to_use = text_type
                if x:
                    return_list.append(TextNode(x, text_type_to_use))

    return return_list


def extract_markdown_images(text) -> list[tuple[str,str]]:
    images_list = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return images_list

def extract_markdown_links(text) -> list[tuple[str,str]]:
    links_list = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return links_list

text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
text_2 = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
extract_markdown_images(text)
extract_markdown_links(text_2)
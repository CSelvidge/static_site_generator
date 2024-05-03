import re
from textnode import TextNode
from conversion import convert_type

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    return_list = []
    

    for old_node in old_nodes:
        if old_node.text_type != "text":
            return_list.append(old_node)
        else:
            new_list = old_node.text.split(delimiter)
            for n,x in enumerate(new_list):
                if n % 2 == 0:
                    text_type_to_use = "text"
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

def split_nodes_image(old_nodes) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            raise ValueError("Expecting a TextNode got {}".format(type(old_node)))
        
        if not extract_markdown_images(old_node.text):
            new_nodes.append(old_node)
        else:
            current_text = old_node.text
            while extract_markdown_images(current_text):
                image_list = extract_markdown_images(current_text)
                image_tup = image_list[0]
                node_list = current_text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
                if node_list[0] != "":
                    new_nodes.append(TextNode(node_list[0], old_node.text_type))
                new_nodes.append(TextNode(image_tup[0], convert_type("text_type_image"), image_tup[1]))
                current_text = node_list[1]
            if current_text:
                new_nodes.append(TextNode(current_text, old_node.text_type))
                


    return new_nodes

def split_nodes_link(old_nodes) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            raise ValueError("Expecting a TextNode got {}".format(type(old_node)))
            
        if not extract_markdown_links(old_node.text):
                new_nodes.append(old_node)
        else:
            current_text = old_node.text
            while extract_markdown_links(current_text):
                link_list = extract_markdown_links(current_text)
                link_tup = link_list[0]
                node_list = current_text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)
                if node_list[0] != "":
                    new_nodes.append(TextNode(node_list[0], old_node.text_type))
                new_nodes.append(TextNode(link_tup[0], convert_type("text_type_link"), link_tup[1]))
                current_text = node_list[1]
            if current_text:
                new_nodes.append(TextNode(current_text, old_node.text_type))


    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, convert_type("text_type_text"))]
    nodes = split_nodes_delimiter(nodes, "**", convert_type("text_type_bold"))
    nodes = split_nodes_delimiter(nodes, "*", convert_type("text_type_italic"))
    nodes = split_nodes_delimiter(nodes, "`", convert_type("text_type_code"))
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

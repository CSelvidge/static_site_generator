import re
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

def markdown_to_blocks(markdown) -> list[str]:
    markdown_list = markdown.split("\n\n")

    for i in reversed(range(len(markdown_list))):
        if markdown_list[i] == "":
            del markdown_list[i]
            continue
        markdown_list[i] = markdown_list[i].strip()

    return markdown_list

def block_to_block_type(block) -> str:
    
    if block.startswith("```") and block.endswith("```"):
        return "code_block"
    
    split_blocks = block.split("\n")
    
    if all(re.match(r"^#{1,6} \w", line) for line in split_blocks):
        return "heading"
    
    if all(re.match(r"^(?:\* |\- )", line) for line in split_blocks):
        return "unordered"
    
    if all(re.match(r"^>", line) for line in split_blocks):
        return "quote"
    
    is_ordered = True
    current_number = None
    
    for line in split_blocks:

        if current_number == None:
            match = re.match(r"^(\d+)", line)
            if match:
                current_number = int(match.group(1))
            else:
                is_ordered = False
                break
        else:
            expected_number = current_number + 1
            match = re.match(r"^(\d+)\. ", line)
            if match and int(match.group(1)) == expected_number:
                current_number += 1
            else:
                is_ordered = False
                break
        
    if is_ordered and current_number is not None:
            return "ordered"
    

    return "paragraph"

def block_lines_to_children(text) -> list[HTMLNode]:
    temporary_text_nodes = text_to_textnodes(text)
    children = []
    for node in temporary_text_nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children

def markdown_to_html_node(markdown) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node= block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)

    
def block_to_paragraph_html(block) -> HTMLNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = block_lines_to_children(paragraph)
    return ParentNode("p", children)

def block_to_heading_html(block) -> HTMLNode:
    match = re.match(r"(^#{1,6})", block) #This expression does not capture the trailing whitespace after the # to get the proper length of the matched group
    if match:

        heading_line = re.sub(r"(^#{1,6} )", "", block) #This expression captures and removes the trailing whitespace after the #

        children = block_lines_to_children(heading_line)

        return ParentNode(f"h{len(match.group())}", children)
    else:
        raise ValueError("Not a heading")

def block_to_code_html(block) -> HTMLNode:
    subbed_code = re.sub(r"^`{3}|`{3}$", "", block)
    split_code = subbed_code.split("\n")
    children = []

    for line in split_code:
        html_node = block_lines_to_children(line)
        children.append(ParentNode("code", html_node))

    return ParentNode("pre", children)

def block_to_quote_html(block) -> HTMLNode:
    quotes = block.split("\n")
    text_lines = []

    for quote in quotes:
        if not quote.startswith(">"):
            raise ValueError("Not a valid quote block")
        text_lines.append(quote.lstrip(">").strip())

    text = " ".join(text_lines)
    
    children = block_lines_to_children(text)

    return ParentNode("blockquote", children)

def block_to_ulist_html(block) -> HTMLNode:
    unordered_list = block.split("\n")
    list_list = []

    for list_element in unordered_list:
        listed_list_element = list_element[2:]
        children_list = block_lines_to_children(listed_list_element)
        list_list.append(ParentNode("li", children_list))

    return ParentNode("ul", list_list)

def block_to_olist_html(block) -> HTMLNode:
    ordered_list = block.split("\n")
    html_list = []

    for element in ordered_list:
        text = re.sub(r"^(\d+. )", "", element)
        html_element = block_lines_to_children(text)
        html_list.append(ParentNode("li", html_element))

    return ParentNode("ol", html_list)

HTML_NODE_DISPATCHER = {
    "code_block": block_to_code_html,
    "paragraph": block_to_paragraph_html,
    "heading": block_to_heading_html,
    "quote": block_to_quote_html,
    "ordered": block_to_olist_html,
    "unordered": block_to_ulist_html
    }

def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type in HTML_NODE_DISPATCHER:
        return HTML_NODE_DISPATCHER[block_type](block)
    else:
        raise ValueError("Not a valid block type")

from htmlnode import LeafNode

valid_types = {"text": lambda text_node: LeafNode(None, text_node.text), 
                    "bold": lambda text_node: LeafNode("b", text_node.text), 
                    "italic": lambda text_node: LeafNode("i", text_node.text), 
                    "code": lambda text_node: LeafNode("code", text_node.text), 
                    "link": lambda text_node: LeafNode("a",text_node.text, {"href": text_node.url}), 
                    "image": lambda text_node: LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
                    }

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other, *attributes):
        if not isinstance(other, type(self)):
            return NotImplemented
        if attributes:
            d = float('NaN')
            return all(self.__dict__.get(a, d) == other.__dict__.get(a, d) for a in attributes)
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def __str__(self):
        return f'"{self.text}" (Type: {self.text_type})'
    


def text_node_to_html_node(text_node):
        
    if text_node.text_type not in valid_types:
        raise Exception("Not a valid type of TextNode")
    return valid_types[text_node.text_type](text_node)
        
        
    
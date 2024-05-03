import re

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def __eq__(self, other, *attributes): 
        if not isinstance(other, type(self)):
            return NotImplemented
        if attributes:
            d = float('NaN')
            return all(self.__dict__.get(a, d) == other.__dict__.get(a, d) for a in attributes)
        return self.__dict__ == other.__dict__
    

    def __repr__(self) -> str:
        return f"HTMLNode(<{self.tag}>, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(value = value, tag = tag, props = props)
        

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("A leaf node requires a value")
        if self.tag is not None:
            attribute_str = self.generate_attributes_str()
            return f"<{self.tag}{attribute_str}>{self.value}</{self.tag}>"
        else:
            return f"{self.value}"
    
    def generate_attributes_str(self) -> str: #Does the same thing as the HTMLNode.props_to_html(), I just prefered it being here, will remove the tests that require props_to_html, and the function itself, when I refactor the tests later
        if not self.props:
            return ""
        attributes_str = ""
        for tag_attribute, value in self.props.items():
            attributes_str += f' {tag_attribute}="{value}"'
        return attributes_str
        
class ParentNode(HTMLNode):
    def __init__(self,tag,children):
        super().__init__(tag = tag, children = children)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node requires a tag")
        if self.children is None:
            raise ValueError("Parent nodes must have children")
        
        concatenated_str = ""

        for child in self.children:
            concatenated_str += child.to_html()
        
        return f"<{self.tag}>{concatenated_str}</{self.tag}>"

        

        

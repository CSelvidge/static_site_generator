"""
This entire first section exists because I disliked the lecture tests using variables such as "text_type_text",
Later i will replace all of the gross "conversion_type("text_type_text")"s in the test files with just "text",
leaving this code here after I do, incase the section gets updated, or I need to come back to it for whatever reason


"""


TYPE_MAPPING = {
        "valid_markdown":{

    "text_type_text": "text", 
    "text_type_bold": "bold", 
    "text_type_italic": "italic", 
    "text_type_code": "code", 
    "text_type_image": "image", 
    "text_type_link": "link" 
}
                        
            ,

        "valid_block_type": {

    "block_type_paragraph": "paragraph",
    "block_type_heading": "heading",
    "block_type_code": "code_block",
    "block_type_quote": "quote",
    "block_type_ulist": "unordered",
    "block_type_olist": "ordered"
}

}


def convert_type(argument_name) -> str:
    for x, inner_dictionary in TYPE_MAPPING.items():

        for key, value in inner_dictionary.items():
            if key == argument_name:
                return value
            
EXTENSION_CONVERSIONS = {#Silly to make a dictionary with one pair, but if this ever needed to convert more than one file type this would be an easy way to update
    ".md": ".html"
}

def convert_extension(file_tuple):
    if file_tuple[1] in EXTENSION_CONVERSIONS:
        return f"{file_tuple[0]}{EXTENSION_CONVERSIONS[file_tuple[1]]}"
import os
import re
import shutil
import datetime
from conversion import convert_extension
from markdown_blocks import markdown_to_html_node



def dir_transfer():
    source = "../static"
    target_dir = "../public"

    if not os.path.isdir("../public"):
        os.mkdir("../public")

    for item in os.listdir(target_dir): #Would be faster to just delete and remake the directory, but this way feels safer
        item_path = os.path.join(target_dir, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

    logging_path = create_log()

    if not os.path.isfile(logging_path):
        raise Exception("Logging file created incorrectly or failed to be created.")
    
    recursive_transfer(source, target_dir, logging_path)

def recursive_transfer(src, dst, logging_path):#Recursive, end case is when it can no longer find a unique file
    contents = os.listdir(src)

    for content in contents:
        content_path = os.path.join(src, content)
        dst_path = os.path.join(dst, content)
        try:
            if os.path.isfile(content_path):
                shutil.copy(content_path ,dst)
                dir_transfer_logging(content, src, dst, logging_path, True)
            elif os.path.isdir(content_path):
                if not os.path.isdir(dst_path):
                    os.mkdir(dst_path)
                recursive_transfer(content_path, dst_path, logging_path)
        except Exception as e:
            dir_transfer_logging(content, src, dst, logging_path, False, str(e))


def create_log():
    if not os.path.isdir("../logs"):
        os.mkdir("../logs")

    log_name = f"transferlog_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    log_path = rf"../logs/{log_name}"

    with open(log_path, "a") as current_file:
        pass

    return log_path

def dir_transfer_logging(file_name, src, dst, logging_path, success, error_message = None):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = "SUCCESS" if success else "FAILURE"

    log_message = f"[{current_time} {status}: {file_name} from {src} to {dst}.]\n"

    if not success:
        log_message += f"Error Message: {error_message}\n"
    with open(logging_path, "a") as current_file:
        current_file.write(log_message)


def extract_title(markdown):
    with open(markdown, "r") as current_file:
        lines = current_file.read().split("\n")

    for line in lines:
        if re.match(r"(^# )", line):
            return line[2:]
    raise ValueError("All pages need a title!")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    title = extract_title(from_path)

    with open(from_path, "r") as current_file:
        contents = current_file.read()

    variable = markdown_to_html_node(contents)
    variable_html = variable.to_html()
        
    
    with open(template_path, "r") as template_file:
        template_contents = template_file.read()

    replaced_title = re.sub(r"({{\s*Title\s*}})", title, template_contents)
    replaced_content = re.sub(r"({{\s*Content\s*}})", f"{variable_html}", replaced_title)

    with open(convert_extension(os.path.splitext(dest_path)), "x") as file:
        file.write(replaced_content)

def recursive_html(node):
    if not isinstance(node, list):
        node.to_html()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    current_content = os.listdir(dir_path_content)

    for content in current_content:
        
        content_path = os.path.join(dir_path_content, content)
        dst_path = os.path.join(dest_dir_path, content)

        if os.path.isfile(content_path):
            generate_page(content_path, template_path, dst_path)
        elif os.path.isdir(content_path):
            if not os.path.isdir(dst_path):
                os.mkdir(dst_path)
            generate_pages_recursive(content_path,template_path, dst_path)
    
    
dir_transfer()
generate_pages_recursive("../content", "../template.html","../public")
import os
import shutil
from markdown_blocks import markdown_to_html_node
from pathlib import Path

def copy_static_to_public(static_dir: str ,dest_path: str) -> None:
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    else:
        shutil.rmtree(dest_path)
        os.mkdir(dest_path)
        
    for item in os.listdir(static_dir):
        item_path = os.path.join(static_dir,item)
        item_dest_path = os.path.join(dest_path,item)
        if os.path.isdir(os.path.join(static_dir,item)):
            print("NEW DIR *",item_path,"--->",item_dest_path)
            copy_static_to_public(os.path.join(static_dir,item),os.path.join(dest_path,item))
            continue
        print("*",item_path,"--->",item_dest_path)
        shutil.copy(item_path,item_dest_path)


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    print(f"* Generating Page from {from_path} to {dest_path} using {template_path}")

    dest_path = Path(dest_path).with_suffix(".html")
    from_path_content = ""
    template_path_content = ""

    with open(from_path,'r') as f:
        from_path_content = f.read()
    with open(template_path,'r') as f:
        template_path_content = f.read()
    
    html = markdown_to_html_node(from_path_content).to_html()
    title = extract_title(from_path_content)

    template_path_content = template_path_content.replace("{{ Title }}", title)
    template_path_content = template_path_content.replace("{{ Content }}", html)
    template_path_content = template_path_content.replace('href="/', 'href="' + basepath)
    template_path_content = template_path_content.replace('src="/', 'src="' + basepath)

    with open(dest_path,"w") as f:
        f.write(template_path_content)

def generate_pages_recursive(from_path: str, template_path: str,dest_path: str, basepath: str) -> None:

    template_path: str = os.path.abspath(template_path)
    from_path_abs: str = os.path.abspath(from_path)
    dest_path_abs: str = os.path.abspath(dest_path)

    for content in os.listdir(from_path_abs):
        content_path: str = os.path.join(from_path_abs,content)
        dest_content_path: str = os.path.join(dest_path_abs,content)

        if os.path.isdir(content_path):
            if not os.path.exists(dest_content_path):
                print( "* Making Directory {dest_content_path}")
                os.mkdir(dest_content_path)

            generate_pages_recursive(content_path,template_path,dest_content_path,basepath)
            continue
        generate_page(content_path,template_path,dest_content_path,basepath)


def extract_title(markdown: str) -> str:
    title = markdown.split("\n")
    for line in title:
        if line.startswith("# "):
            return line[1:]
    raise Exception("Error")

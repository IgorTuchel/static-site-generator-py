import copystatic
import sys
import os
import shutil
dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"

def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    copystatic.copy_static_to_public(dir_path_static,dir_path_public)    
    copystatic.generate_pages_recursive(dir_path_content,template_path,dir_path_public,basepath)
    
if __name__ == "__main__":
    main()

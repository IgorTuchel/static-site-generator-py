import copystatic
import sys
import config

def main():
    args = config.set_parser()
    kwargs = dict((y,x) for y,x in [arg for arg in args._get_kwargs() if None not in arg])

    if kwargs.get("create"):
        config.create_config(**kwargs)
        sys.exit(0)
        
    if kwargs.get("update"):
        config.update(**kwargs)
        sys.exit(0)
    
    if kwargs.get("run"):
        if not config.config_exists():
            print("WARNING: No config exists")
            print("use --help to generate config")
            sys.exit(1)
        config_info = config.get_config()
        dir_path_static = config_info["Paths"]["static_path"]
        dir_path_public = config_info["Paths"]["public_path"]
        dir_path_content = config_info["Paths"]["content_path"]
        dir_path_template = config_info["Paths"]["template_path"]
        copystatic.copy_static_to_public(dir_path_static,dir_path_public)
        copystatic.generate_pages_recursive(dir_path_content,dir_path_template,dir_path_public,"/")
        sys.exit(0)
    print("Usage main.py --help")

if __name__ == "__main__":
    main()

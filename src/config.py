import configparser
import os
import argparse

def set_parser() -> None:
    parser = argparse.ArgumentParser(description='Example CLI with flags')
    parser.add_argument('--static_path',type=str,help="Set the Static Path for the SSG - Should contain elements such as images and css formats.")
    parser.add_argument('--public_path',type=str,help="Set the Public Path for the SSG - This is where the final generated HTML is stored.")
    parser.add_argument('--content_path',type=str,help="Set the Content Path for the SSG - Should contain the HTML.")
    parser.add_argument('--template_path',type=str, help="Set the Template Path for the SSG - Should contain the HTML template for the SSG.")
    parser.add_argument('--create',action='store_true', help="Used to create the config")
    parser.add_argument('--update',action='store_true', help="Used to update the config")
    parser.add_argument('--run',action='store_true', help="Used to run the SSG based on the config")
    return parser.parse_args()

def get_config() -> None:
    if not config_exists():
        return
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def make_config(static : str = "../bin/static",public : str ="../bin/public",content : str ="../bin/content", template : str ="../bin/template.html") -> None:
    config = configparser.ConfigParser()
    paths = [static,public,content]
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            print(f"* Making Directory {path}")
    if not os.path.exists(template):
        with open(template, "w") as f:
            print(f"* Making HTML Template {path}")
            f.write("""
                    <!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{{ Title }}</title>
    <link href="/index.css" rel="stylesheet" />
  </head>

  <body>
    <article>{{ Content }}</article>
  </body>
</html>
                    """)


    config['Paths'] = {
        'static_path': static,
        'public_path': public,
        'content_path': content,
        'template_path': template,
    }
    
    with open('config.ini', 'w') as f:
        config.write(f)

def create_config(**kwargs: dict[str:str]) -> None:
    if config_exists():
        print("WARNING: CONFIG EXISTS")
        while True:
            print("OVERWRITE CONFIG (y/n)")
            user_input = input()
            if user_input == "y":
                break
            elif user_input == "n":
                return
    make_config()
    update(**kwargs)

def update(**kwargs: dict[str:str]) -> None:
    print("\n*** Attempting Config Update\n")
    valid_opts = ["static_path","public_path","content_path","template_path"]
    if not config_exists():
        make_config()
    err = []
    for arg in kwargs:
        path = kwargs[arg]
        if not arg in valid_opts:
            continue
        if not os.path.exists(path):
            err.append(f"!!* [{arg}] Path {path} does not exist")
            continue
        if not os.path.isdir(path) and arg != "template_path":
            err.append(f"!!* [{arg}] Path {path} is not a valid directory")
            continue
        if os.path.isdir(path) and arg == "template_path":
            err.append(f"!!* [{arg}] Path {path} must be a file")
            continue
        update_config(arg, kwargs[arg])
    
    if err:
        print("\nErrors:\n")
        for e in err:
            print(e)

    print("\nUpdated Config File Content:\n")
    display_config()
    print("\n*** End of Config Update\n")

def update_config(opt: str, val: str) -> None:
    config = get_config()
    print(f"--* {config["Paths"][opt]} -> {val}")
    config["Paths"][opt] = val

    with open('config.ini', 'w') as f:
        config.write(f)

def config_exists() -> bool:
    return os.path.exists("./config.ini")

def display_config() -> None:
    config = get_config()
    for section in config.sections():
        print(f"[{section}]")
        for key, val in config.items(section):
            print(f"{key} = {val}")
    
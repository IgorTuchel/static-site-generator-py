from textnode import TextNode,TextType
import re
def split_nodes_delimiter(old_nodes : list[TextNode], delimiter : str, text_type : TextType):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue
            
        new_nodes = []
        text = node.text

        while (index := text.find(delimiter)) != -1:
            if index > 0:
                new_nodes.append(TextNode(text[:index],TextType.TEXT))
            text = text[index+len(delimiter):]
            index = text.find(delimiter)
            if index == -1:
                raise Exception('Markdown Text not properly closed')
            new_nodes.append(TextNode(text[:index],text_type))
            index += len(delimiter)
            if index + len(delimiter) > len(text):
                text = text[index:]
                break
            
            text = text[index:]

        if text:
            new_nodes.append(TextNode(text,TextType.TEXT))
        nodes.extend(new_nodes)
    return nodes

def split_nodes_image(old_nodes : list[TextNode]) -> list[TextNode]:
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue

        new_nodes = []
        text = node.text

        for img in extract_markdown_images(text):
            reconsturct = f"![{img[0]}]({img[1]})"
            index = text.find(reconsturct)
            if index > 0:
                new_nodes.append(TextNode(text[:index],TextType.TEXT))
            new_nodes.append(TextNode(img[0], TextType.IMAGE,img[1]))
            text = text[index+len(reconsturct):]
        if text:
            new_nodes.append(TextNode(text,TextType.TEXT))
        nodes.extend(new_nodes)
    return nodes

def split_nodes_link(old_nodes : list[TextNode]) -> list[TextNode]:
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue
            
        new_nodes = []
        text = node.text

        for img in extract_markdown_links(text):
            reconsturct = f"[{img[0]}]({img[1]})"
            index = text.find(reconsturct)
            if index > 0:
                new_nodes.append(TextNode(text[:index],TextType.TEXT))
            new_nodes.append(TextNode(img[0], TextType.LINK,img[1]))
            text = text[index+len(reconsturct):]
        if text:
            new_nodes.append(TextNode(text,TextType.TEXT))
        nodes.extend(new_nodes)
    return nodes

def extract_markdown_images(text : str) -> str:
    extract = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return extract
def extract_markdown_links(text : str) -> str:
    extract = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return extract


def text_to_textnodes(text: str) -> TextNode:
    delimiters = {TextType.BOLD: "**",
                  TextType.CODE: "`",
                  TextType.ITALIC: "_"}
    base_node = [TextNode(text,TextType.TEXT)]
    text_node = split_nodes_image(base_node)
    text_node = split_nodes_link(text_node)
    for delimiter in delimiters:
        text_node = split_nodes_delimiter(text_node,delimiters[delimiter],delimiter)
    
    return text_node
from enum import Enum
from functools import reduce
from htmlnode import HTMLNode,ParentNode,LeafNode
from textnode import text_node_to_html_node,TextNode,TextType
from inline import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = 'paragraph',
    HEADING = 'heading',
    CODE = 'code',
    QUOTE = 'quote',
    ULIST = 'unordered_list',
    OLIST = 'ordered_list'



def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    for item in markdown.split("\n\n"):
        if item:
            item = item.strip()
            blocks.append(item)
        
    return blocks

def block_to_block_type(block: str) -> BlockType:
    if block.startswith(("# ","## ","### ","#### ","##### ","###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split('\n')
    
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE 
    if all(line.startswith("- ") for line in lines):
        return BlockType.ULIST
    
    for i, line in enumerate(lines, 1):
        if not line.startswith(f"{i}. "):
            return BlockType.PARAGRAPH
    return BlockType.OLIST

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        html_node = get_html_node(block)
        html_nodes.append(html_node)

    return ParentNode("div",children=html_nodes)


def get_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html(block)
    if block_type == BlockType.HEADING:
        return heading_to_html(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html(block)
    if block_type == BlockType.CODE:
        return code_to_html(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html(block)
    if block_type == BlockType.OLIST:
        return olist_to_html(block)
    raise Exception("Block Type Not Recognised")


def text_to_children(text : TextNode) -> list[HTMLNode]:
    child_nodes = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        child_nodes.append(text_node_to_html_node(text_node))
    return child_nodes

def paragraph_to_html(block : str) -> ParentNode:
    joined_text = " ".join(block.split("\n"))
    child_nodes = text_to_children(joined_text)
    return ParentNode("p",children=child_nodes)
    
def heading_to_html(block: str) -> ParentNode:
    count = 0
    for i in range(len(block)):
        if block[i] == "#":
            count += 1
            continue
        break
    if count >= len(block) or count > 6:
        raise Exception("Invalid Heading Size")
    block = block[count + 1:]
    children = text_to_children(block)
    return ParentNode(f"h{count}",children)

def quote_to_html(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise Exception("Invalid Quote Block")
        new_lines.append(line.strip("> "))
    joined_text = " ".join(new_lines)
    child_nodes = text_to_children(joined_text)
    return ParentNode("blockquote",children=child_nodes)

def code_to_html(block: str) -> ParentNode:
    if not block.startswith("```") and not block.endswith("```"):
        raise Exception("Incorrect Code Block Syntax")
    block = block[4:-3]
    text_node = TextNode(block,TextType.TEXT)
    child_node = text_node_to_html_node(text_node)
    pre_tag = ParentNode("code",[child_node])
    return ParentNode("pre",[pre_tag])

def ulist_to_html(block: str) -> ParentNode:
    lines = block.split('\n')
    children = []

    for line in lines:
        line = line.lstrip("- ")
        node = text_to_children(line)
        list_node = ParentNode("li",children=node)
        children.append(list_node)
    return ParentNode("ul",children=children)

def olist_to_html(block: str) -> ParentNode:
    lines = block.split('\n')
    new_lines = []
    children = []
    for index in range(0,len(lines)):
        new_lines.append(lines[index].lstrip(f"{index + 1}. "))
    for line in new_lines:
        node = text_to_children(line)
        list_node = ParentNode("li",children=node)
        children.append(list_node)
    return ParentNode("ol",children=children)

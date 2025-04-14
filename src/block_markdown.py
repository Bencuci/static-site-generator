from htmlnode import HTMLNode
from enum import Enum
import re
from markdown import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode

def markdown_to_blocks(markdown):
  blocks = markdown.split("\n\n")
  filtered_blocks = []
  for block in blocks:
      if block == "":
          continue
      block = block.strip()
      filtered_blocks.append(block)
  return filtered_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if re.match(r"^#{1,6} ", lines[0]):
        return BlockType.HEADING
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UL
    if all(re.match(rf"^{i+1}\. ", lines[i]) for i in range(len(lines))):
        return BlockType.OL
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_node = ParentNode("div", [], None)

    for block in blocks:
        type = block_to_block_type(block)
        block_node = None

        if type == BlockType.PARAGRAPH:
            lines = [line.strip() for line in block.split("\n")]
            block_text = " ".join(line for line in lines if line)
            if block_text: 
                block_node = ParentNode("p", text_to_children(block_text), None)
        elif type == BlockType.HEADING:
            level = len(block) - len(block.lstrip("#"))
            content = block.lstrip("#").lstrip()
            block_node = ParentNode(f"h{level}", text_to_children(content), None)
        elif type == BlockType.CODE:
            lines = block.split("\n")
            if len(lines) >= 3: 
                content_lines = lines[1:-1]  
                non_empty_lines = [line for line in content_lines if line.strip()]
                if non_empty_lines:
                    min_indent = min(len(line) - len(line.lstrip()) for line in non_empty_lines)
                    content_lines = [line[min_indent:] if line.strip() else line for line in content_lines]
                    content = "\n".join(content_lines) + "\n"
                else:
                    content = ""
            else:
                content = block.strip("```").strip()
            text_node = LeafNode(None, content, None)
            code_node = ParentNode("code", [text_node], None)
            block_node = ParentNode("pre", [code_node], None)
        elif type == BlockType.QUOTE:
            cleaned_lines = []
            lines = block.split("\n")
            for line in lines:
                if line.startswith("> "):
                    cleaned_lines.append(line[2:])
                elif line.startswith(">"):
                    cleaned_lines.append(line[1:])
                else:
                    cleaned_lines.append(line)
            content = "\n".join(cleaned_lines)
            block_node = ParentNode("blockquote", text_to_children(content), None)
        elif type == BlockType.UL:
            list_items = []
            item_lines = block.split("\n")
            for item in item_lines:
                if item.strip(): 
                    item_content = item.lstrip("- ")
                    li_node = ParentNode("li", text_to_children(item_content), None)
                    list_items.append(li_node)
            block_node = ParentNode("ul", list_items, None)
        elif type == BlockType.OL:
            list_items = []
            item_lines = block.split("\n")
            for item in item_lines:
                if item.strip():
                    item_content = re.sub(r'^\d+\.\s+', '', item)
                    li_node = ParentNode("li", text_to_children(item_content), None)
                    list_items.append(li_node)
            block_node = ParentNode("ol", list_items, None)
        
        if block_node is not None: 
            parent_node.children.append(block_node)
    
    return parent_node


def text_to_children(text):
    if not text or text.isspace():
        return [LeafNode(None, "", None)]
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        if html_node is None:
            raise ValueError(f"Failed to convert text node to HTML node: {node}")
        html_nodes.append(html_node)
    if not html_nodes:
        return [LeafNode(None, "", None)]
    return html_nodes

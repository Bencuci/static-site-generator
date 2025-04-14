from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
  TEXT = "text"
  BOLD = "bold"
  ITALIC = "italic"
  CODE = "code"
  LINK = "link"
  IMAGE = "image"

class TextNode:
  def __init__(self, text, text_type, url=None):
    self.text = text
    self.text_type = text_type
    self.url = url
  
  def __eq__(self, Node2):
    text_equal = self.text == Node2.text
    type_equal = self.text_type == Node2.text_type
    url_equal = self.url == Node2.url
    if text_equal and type_equal and url_equal:
      return True
    return False

  def __repr__(self):
    return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
  if not isinstance(text_node.text_type, TextType):
    raise ValueError(f"Invalid text type: {text_node.text_type}")
  match text_node.text_type:
    case TextType.TEXT:
        return LeafNode(None, text_node.text)
    case TextType.BOLD:
        return LeafNode("b", text_node.text)
    case TextType.ITALIC:
        return LeafNode("i", text_node.text)
    case TextType.CODE:
        return LeafNode("code", text_node.text)
    case TextType.LINK:
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    case TextType.IMAGE:
        return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
    case _:
        raise ValueError(f"Unhandled text type: {text_node.text_type}")
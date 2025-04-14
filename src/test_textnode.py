import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(node, node2)

  def test_not_eq(self):
    node = TextNode("This is a italic text node", TextType.ITALIC)
    node2 = TextNode("This is a code text node", TextType.CODE)
    self.assertNotEqual(node, node2)

  def test_url_not_eq(self):
    with_url_node = TextNode("link node?", TextType.LINK, "boot.dev")
    without_url_node = TextNode("link node?", TextType.LINK)
    self.assertNotEqual(with_url_node, without_url_node)

class TestTextNodeToHtmlNode(unittest.TestCase):
  def test_text(self):
    text_node = TextNode("This is a text node", TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")

  def test_image(self):
    text_node = TextNode("This is an image", TextType.IMAGE, "boot.dev")
    html_node = text_node_to_html_node(text_node)
    self.assertEqual(html_node.tag, "img")
    self.assertEqual(html_node.value, "")
    self.assertEqual(html_node.props, {"src": "boot.dev", "alt": "This is an image"})
    

if __name__ == "__main__":
  unittest.main()
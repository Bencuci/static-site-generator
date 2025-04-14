import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
  def test_init(self):
    node = HTMLNode("p", "Hello, world!", [], {"class": "text"})
    self.assertEqual(node.tag, "p")
    self.assertEqual(node.value, "Hello, world!")
    self.assertEqual(node.children, [])
    self.assertEqual(node.props, {"class": "text"})

  def test_props_to_html(self):
    node = HTMLNode(props={"class": "header", "id": "main"})
    html = node.props_to_html()
    self.assertIn(" class='header'", html)
    self.assertIn(" id='main'", html)

  def test_repr(self):
    node = HTMLNode("div", "Hi", props={"class": "box"})
    expected = "HTMLNode(div, Hi, None, {'class': 'box'})"
    self.assertEqual(repr(node), expected)
  
  def test_leaf_to_html_no_prop(self):
    node = LeafNode("p", "Hello World!")
    self.assertEqual(node.to_html(), "<p>Hello World!</p>")

  def test_leaf_to_html_propped(self):
    node = LeafNode("i", "italic writing", {"class": "italic-text", "id": "first-italic"})
    self.assertEqual(node.to_html(), "<i class='italic-text' id='first-italic'>italic writing</i>")

  def test_leaf_to_html_no_tag(self):
    node = LeafNode(None, "Hello, world!")
    self.assertEqual(node.to_html(), "Hello, world!")

  def test_parent_node(self):
    node = ParentNode(
      "p",
      [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
      ],
    )
    self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    
  def test_parent_to_html_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(),
      "<div><span><b>grandchild</b></span></div>"
    )

class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props
  
  def to_html(self):
    raise NotImplementedError

  def props_to_html(self):
    if not self.props:
      return ""
    html_props = ""
    for attribute in self.props:
      html_props += f" {attribute}='{self.props[attribute]}'"
    return html_props

  def __repr__(self):
    return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
  def __init__(self, tag, value, props=None):
    super().__init__(tag, value, children=None, props=props)
  
  def to_html(self):
    if self.value == None:
      raise ValueError("leaf node has no value")
    if self.tag == None:
      return f"{self.value}"
    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

  def __repr__(self):
    return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag, value=None, children=children, props=props)

  def to_html(self):
    if not self.tag:
      raise ValueError("parent node has no tag")
    if not self.children:
      raise ValueError("parent node has no children")
    if self.children is None:
      raise ValueError("Child is None in ParentNode")
    html_inside = ""
    for children in self.children:
      html_inside += children.to_html()
    return f"<{self.tag}{self.props_to_html()}>{html_inside}</{self.tag}>"

  def __repr__(self):
    return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
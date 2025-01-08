

class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag, self.value, self.children, self.props = tag, value, children, props

  def to_html(self):
    return repr(self)

  def props_to_html(self):
    html = ""
    if self.props:
      for key in self.props.keys():
        html += f" {key}=\"{self.props[key]}\""
    return html

  def __repr__(self):
    open = ""
    close = ""
    value = ""
    if self.value:
      value = self.value
    if self.tag:
      open = f"<{self.tag}{self.props_to_html()}>"
      close = f"</{self.tag}>"
    childhtml = ""
    if self.children:
      for child in self.children:
        childhtml += repr(child)
    return f"{open}{value}{childhtml}{close}"
  
class LeafNode(HTMLNode):
  def __init__(self, tag=None, value=None, props=None):
    if value == None:
      raise ValueError("Can't construct a leaf node without a value")
    super().__init__(tag, value, None, props)

class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    if not tag:
      raise ValueError("Can't construct a parent node without a tag")
    if not children:
      raise ValueError("Can't construct a parent node without children")
    super().__init__(tag, None, children, props)
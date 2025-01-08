import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
  def test_null(self):
    node = HTMLNode()
    self.assertEqual(repr(node), "")
  
  def test_tag(self):
    node = HTMLNode("p")
    self.assertEqual(repr(node), "<p></p>")
  
  def test_prop(self):
    node = HTMLNode("a", "Google", None, {"href":"http://www.google.com"})
    self.assertEqual(repr(node), "<a href=\"http://www.google.com\">Google</a>")

  def test_childs(self):
    node = HTMLNode("table", None, [
      HTMLNode("tr", None, [HTMLNode("td", "1"), HTMLNode("td", "2"),]),
      HTMLNode("tr", None, [HTMLNode("td", "3"), HTMLNode("td", "4"),])
    ])
    self.assertEqual(repr(node), "<table><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>")

  def test_leaf_exception(self):
    with self.assertRaises(ValueError):
      LeafNode()
    with self.assertRaises(ValueError):
      LeafNode(None, None)

  def test_leaf_text(self):
    node = LeafNode(None, "Google")
    self.assertEqual(repr(node), "Google")

  def test_leaf_basic(self):
    node = LeafNode("a", "Google", {"href":"http://www.google.com"})
    self.assertEqual(repr(node), "<a href=\"http://www.google.com\">Google</a>")

  def test_parent_exception(self):
    with self.assertRaises(ValueError) as context:
      ParentNode(None, [])
    self.assertTrue("Can't construct a parent node without a tag" in repr(context.exception))
  
  def test_parent_children_exception(self):
    with self.assertRaises(ValueError) as context:
      ParentNode("p", None)
    self.assertTrue("Can't construct a parent node without children" in repr(context.exception))
  
  def test_parent_childs(self):
    node = ParentNode("table", [
      ParentNode("tr", [LeafNode("td", "1"), LeafNode("td", "2")]),
      ParentNode("tr", [LeafNode("td", "3"), LeafNode("td", "4")])
    ])
    self.assertEqual(repr(node), "<table><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>")

if __name__ == "__main__":
    unittest.main()
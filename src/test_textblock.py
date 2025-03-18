import unittest

from textblock import *

class TestTextBlock(unittest.TestCase):

  def test_markdown_to_blocks(self):
    text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
    blocks = markdown_to_blocks(text)
    self.assertEqual(len(blocks), 3)
    self.assertEqual(blocks, ["# This is a heading","This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                              """* This is the first list item in a list block
* This is a list item
* This is another list item"""])
    
  def test_block_to_block(self):
    text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

```This is 
a bunch
of code```

1. This is
2. An ordered
3. List

> This is
> A quote
"""
    blocks = markdown_to_blocks(text)
    types = []
    for block in blocks:
       types.append(block_to_block_type(block))
    self.assertEqual(types, [BlockType.HEADING, BlockType.PARAGRAPH, BlockType.UNORDERED_LIST, 
                             BlockType.CODE, BlockType.ORDERED_LIST, BlockType.QUOTE])

  def test_block_to_block_fail(self):
    text = """####### This is a failed heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a failed list block
- This is a list item
> This is another list item

``This is 
a failed bunch
of code```

1. This is
2. A failed ordered
2. List

> This is
- A failed quote
"""
    blocks = markdown_to_blocks(text)
    types = []
    for block in blocks:
       types.append(block_to_block_type(block))
    self.assertEqual(types, [BlockType.PARAGRAPH, BlockType.PARAGRAPH, BlockType.PARAGRAPH, 
                             BlockType.PARAGRAPH, BlockType.PARAGRAPH, BlockType.PARAGRAPH])

  def test_markdown_to_html(self):
    text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

```This is
a bunch
of code```

1. This is
2. An ordered
3. List

> This is
> A quote
"""
    html = markdown_to_html_node(text)
    expected = "<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul><pre><code>This is\na bunch\nof code</code></pre><ol><li> This is</li><li> An ordered</li><li> List</li></ol><blockquote>This is\nA quote</blockquote></div>"
    self.assertEqual(repr(html), expected)

  def test_extract_title(self):
    text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it."""
    self.assertEqual(extract_title(text), "This is a heading")

    text2 = """## This is a heading

# This is also a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it."""
    self.assertEqual(extract_title(text2), "This is also a heading")

    text3 = """## This is a heading"""
    with self.assertRaises(Exception) as e:
      extract_title(text3)
      self.assertEqual(e, Exception("No title found"))

if __name__ == "__main__":
    unittest.main()
import unittest

from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is also a text node", TextType.ITALIC, "http://google.com")
        node2 = TextNode("This is also a text node", TextType.ITALIC, "http://google.com")
        self.assertEqual(node, node2)
    
    def test_neq_1(self):
        node = TextNode("Third text node", TextType.CODE, "http://google.com")
        node2 = TextNode("Third text node", TextType.ITALIC, "http://google.com")
        self.assertNotEqual(node, node2)

    def test_neq_2(self):
        node = TextNode("A text node", TextType.BOLD)
        node2 = TextNode("A different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_neq_3(self):
        node = TextNode("A text node", TextType.BOLD)
        node2 = TextNode("A text node", TextType.BOLD, "http://google.com")
        self.assertNotEqual(node, node2)
    
    def test_text(self):
        node = TextNode("A text node", TextType.TEXT)
        self.assertEqual(repr(text_node_to_html_node(node)), "A text node")
    
    def test_bold(self):
        node = TextNode("A text node", TextType.BOLD)
        self.assertEqual(repr(text_node_to_html_node(node)), "<b>A text node</b>")

    def test_code(self):
        node = TextNode("def nothing():\n\tpass", TextType.CODE)
        self.assertEqual(repr(text_node_to_html_node(node)), "<code>def nothing():\n\tpass</code>")
    
    def test_image(self):
        node = TextNode("puppy", TextType.IMAGE, "https://en.wikipedia.org/wiki/Puppy#/media/File:Golde33443.jpg")
        self.assertEqual(repr(text_node_to_html_node(node)), "<img src=\"https://en.wikipedia.org/wiki/Puppy#/media/File:Golde33443.jpg\" alt=\"puppy\"></img>")
    
    def test_link(self):
        node = TextNode("Google", TextType.LINK, "https://www.google.com")
        self.assertEqual(repr(text_node_to_html_node(node)), "<a href=\"https://www.google.com\">Google</a>")

    def test_split_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        html = ""
        for node in new_nodes:
            html += repr(text_node_to_html_node(node))
        self.assertEqual(html, "This is text with a <code>code block</code> word")
    
    def test_split_nodes_all(self):
        node = TextNode("**This** *is* **text** *with* a `code block` *word*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        html = ""
        for node in new_nodes:
            html += repr(text_node_to_html_node(node))
        self.assertEqual(html, "<b>This</b> <i>is</i> <b>text</b> <i>with</i> a <code>code block</code> <i>word</i>")

    def test_split_nodes_fail(self):
        node = TextNode("This is text `with a `code block` word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_find_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_find_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("This is text with a link ", TextType.TEXT),
                    TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
                    ]
        self.assertEqual(new_nodes, expected)
    
    def test_extract_images(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("This is text with a ", TextType.TEXT),
                    TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
                    ]
        self.assertEqual(new_nodes, expected)

    def test_text_to_textnodes(self):
        node = TextNode("**text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT)
        nodes = text_to_textnodes(node)
        expected = [TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev")
                    ]
        self.assertEqual(nodes, expected)

    
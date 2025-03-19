import re
from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
	TEXT = "normal"
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
	
	def __eq__(self, other):
		return self.text == other.text and self.text_type == other.text_type and self.url == other.url

	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
	
def text_node_to_html_node(text_node):
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
			return LeafNode("a", text_node.text, {"href":text_node.url})
		case TextType.IMAGE:
			return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
		case _:
			raise ValueError("Text type not valid")
		
def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
		else:
			chunks = node.text.split(delimiter)
			if len(chunks) % 2 == 0:
				raise ValueError(f"Must have matching {delimiter}s!")
			parity = True
			for chunk in chunks:
				if parity:
						if len(chunk):
							new_nodes.append(TextNode(chunk, TextType.TEXT))
				else:
					new_nodes.append(TextNode(chunk, text_type))
				parity = not parity
	return new_nodes

def extract_images(node):
	if not node.text:
		return []
	if node.text_type != TextType.TEXT:
		return [node]
	images = extract_markdown_images(node.text)
	if not len(images):
		return [node]
	imagetext =f"![{images[0][0]}]({images[0][1]})"
	for i in range(len(node.text)):
		if node.text[i:i+len(imagetext)] == imagetext:
			ret = []
			ret.append(TextNode(node.text[:i], TextType.TEXT))
			ret.append(TextNode(images[0][0], TextType.IMAGE, images[0][1]))
			remainder = TextNode(node.text[i+len(imagetext):], TextType.TEXT)
			ret.extend(extract_images(remainder))
			return ret
	return []

def split_nodes_image(old_nodes):
	new_nodes = []
	for node in old_nodes:
		new_nodes.extend(extract_images(node))
	return new_nodes

def extract_links(node):
	if not node.text:
		return []
	if node.text_type != TextType.TEXT:
		return [node]
	links = extract_markdown_links(node.text)
	if not len(links):
		return [node]
	linktext =f"[{links[0][0]}]({links[0][1]})"
	for i in range(len(node.text)):
		if node.text[i:i+len(linktext)] == linktext:
			ret = []
			ret.append(TextNode(node.text[:i], TextType.TEXT))
			ret.append(TextNode(links[0][0], TextType.LINK, links[0][1]))
			remainder = TextNode(node.text[i+len(linktext):], TextType.TEXT)
			ret.extend(extract_links(remainder))
			return ret
	return []

def split_nodes_link(old_nodes):
	new_nodes = []
	for node in old_nodes:
		new_nodes.extend(extract_links(node))
	return new_nodes

def extract_markdown_images(text):
	return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
	return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def text_to_textnodes(text):
	nodes = split_nodes_image([text])
	nodes = split_nodes_link(nodes)
	nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
	nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
	nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
	nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
	return nodes

def text_to_html_nodes(text):
	#print("[TEXT]" + text + "[TEXT]")
	text_nodes = text_to_textnodes(TextNode(text, TextType.TEXT))
	#print(f"[TEXT NODES] {text_nodes} [TEXT_NODES]")
	html_nodes = []
	for node in text_nodes:
		html_nodes.append(text_node_to_html_node(node))
	return html_nodes



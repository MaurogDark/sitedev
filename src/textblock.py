from enum import Enum
from textnode import text_to_html_nodes
from htmlnode import HTMLNode, ParentNode

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"

class BlockNode:
	def __init__(self, text, block_type):
		self.text = text
		self.block_type = block_type
		

def check_hashes(text):
	words = text.split(" ")
	if not len(words[0]):
		return 0
	if words[0] == "#" * len(words[0]):
		if len(words[0]) > 6:
			return 0
		return len(words[0])
	return 0
		
def check_quotes(text):
	lines = text.split("\n")
	for line in lines:
		if len(line) < 1 or line[0:1] != ">":
			return False
	return True
		
def check_unordered_list(text):
	lines = text.split("\n")
	for line in lines:
		if len(line) < 2 or (line[0] != "*" and line[0] != "-") or line[1] != " ":
			return False
	return True
	
def check_ordered_list(text):
	lines = text.split("\n")
	count = 1
	for line in lines:
		words = line.split(" ")
		if not len(words):
			return False
		numbers = words[0].split(".")
		if not len(numbers):
			return False
		if not numbers[0].isnumeric():
			return False
		if not int(numbers[0]) == count:
			return False
		count += 1
	return True
		

def block_to_block_type(text):
	if check_hashes(text):
		return BlockType.HEADING
	if len(text) >= 6 and text[0:3] == "`" * 3 and text[-3:] == "`" * 3:
		return BlockType.CODE
	if check_quotes(text):
		return BlockType.QUOTE
	if check_unordered_list(text):
		return BlockType.UNORDERED_LIST
	if check_ordered_list(text):
		return BlockType.ORDERED_LIST
	return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
		blocks = []
		lines = markdown.split("\n")
		current_block = ""
		eat_blank_lines = True
		for line in lines:
				if not len(line) and not eat_blank_lines:
						blocks.append(current_block.strip())
						current_block = ""
						eat_blank_lines = True
				elif len(line):
						eat_blank_lines = False
						if len(current_block):
							current_block += "\n"
						current_block += line
		if len(current_block.strip()):
				blocks.append(current_block.strip())
		return blocks


def block_to_html_node(block):
	type = block_to_block_type(block)
	if type == BlockType.HEADING:
		n = check_hashes(block)
		return ParentNode(f"h{n}", text_to_html_nodes(block[n+1:]))
	elif type == BlockType.CODE:
		return ParentNode("pre", [ParentNode("code", text_to_html_nodes(block[3:-3]))])
	elif type == BlockType.QUOTE:
		quote = ""
		for line in block.split("\n"):
			if len(quote):
				quote += "\n"
			if len(line) > 2:
				quote += line[2:]
		return ParentNode("blockquote", text_to_html_nodes(quote))
	elif type == BlockType.UNORDERED_LIST:
		children = []
		for line in block.split("\n"):
			children.append(ParentNode("li", text_to_html_nodes(line[2:])))
		return ParentNode("ul", children)
	elif type == BlockType.ORDERED_LIST:
		children = []
		for line in block.split("\n"):
			dot_index = line.find(".")
			children.append(ParentNode("li", text_to_html_nodes(line[dot_index+2:])))
		return ParentNode("ol", children)
	return HTMLNode("p", None, text_to_html_nodes(block), None )
		

def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	children = []
	for block in blocks:
		children.append(block_to_html_node(block))
	return HTMLNode("div", None, children, None )

def extract_title(markdown):
	blocks = markdown_to_blocks(markdown)
	for block in blocks:
		if block_to_block_type(block) == BlockType.HEADING and check_hashes(block) == 1:
			return block[2:]
	raise Exception("No title found")
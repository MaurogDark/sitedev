import os, shutil, sys
from textblock import markdown_to_html_node, extract_title

def copy_files(source, target):
	if target:
		if os.path.exists(target):
			print(f"{target} exists, deleting...")
			shutil.rmtree(target)
		if os.path.isfile(source):
			print(f"Copying {source} to {target}")
			shutil.copy(source, target)
		else:
			print(f"Creating {target}")
			os.mkdir(target)
			children = os.listdir(source)
			for child in children:
				copy_files(os.path.join(source, child), os.path.join(target, child))

def generate_page(basepath, from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	markdown = open(from_path).read()
	template = open(template_path).read()
	html = markdown_to_html_node(markdown)
	title = extract_title(markdown)
	title_stitch = template.split("{{ Title }}")
	if len(title_stitch) != 2:
		raise("Template missing {{ Title }} placeholder!")
	template = title_stitch[0] + title + title_stitch[1]
	content_stitch = template.split("{{ Content }}")
	if len(content_stitch) != 2:
		raise("Template missing {{ Content }} placeholder!")
	content = repr(html)
	template = content_stitch[0] + content + content_stitch[1]
	template = template.replace("href=\"/", "href=\"" + basepath)
	template = template.replace("src=\"/", "src=\"" + basepath)
	
	dir = os.path.dirname(dest_path)
	if not os.path.exists(dir) or not os.path.isdir(dir):
		os.makedirs(dir)
	open(dest_path, "w").write(template)

def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
	print(f"generating {dest_dir_path} from {dir_path_content}")
	for entry in os.listdir(dir_path_content):
		source_path = os.path.join(dir_path_content, entry)
		print(f"entry is is {source_path}")
		if os.path.isfile(source_path) and len(entry) > 3 and entry[-3:] == ".md":
			target_path = os.path.join(dest_dir_path, entry[:-3]+".html")
			print(f"generating {target_path} from {source_path}")
			generate_page(basepath, source_path, template_path, target_path)
		elif os.path.isdir(source_path):
			target_path = os.path.join(dest_dir_path, entry)
			generate_pages_recursive(basepath, source_path, template_path, target_path)

def main():
	basepath = "/"
	if len(sys.argv) >= 2:
		basepath = sys.argv[1]
	copy_files("static", "docs")
	generate_pages_recursive(basepath, "content", "template.html", "docs")

	

main()

import os
import shutil
from textnode import TextNode, TextType
from block_markdown import markdown_to_html_node
from markdown import extract_title

def copy_to_dir(source_path, target_path):
  if not os.path.exists(source_path):
    raise Exception("Source directory's path is not existing")
  
  elif not os.path.exists(target_path):
    os.mkdir(target_path)
  
  elif os.path.isdir(target_path):
    for item in os.listdir(target_path):
      item_path = os.path.join(target_path, item)
      if os.path.isdir(item_path):
        shutil.rmtree(item_path)
      else:
        os.remove(item_path)

  sdir_files = os.listdir(source_path)
  tdir_files = os.listdir(target_path)

  for item in sdir_files:
    path_to_file = os.path.join(source_path, item)
    path_to_target = os.path.join(target_path, item)

    if os.path.isdir(path_to_file):
      copy_to_dir(path_to_file, path_to_target)
      continue
    
    elif os.path.isfile(path_to_file):
      shutil.copy(path_to_file, path_to_target)


def generate_page(from_path, template_path, dest_path):
  print(f"Generating page from ${from_path} to ${dest_path}, using ${template_path}.")

  with open(from_path, 'r') as from_file:
    from_content = from_file.read()
    
    with open(template_path, 'r') as template_file:
      template_content = template_file.read()

      from_node = markdown_to_html_node(from_content)
      from_html = from_node.to_html()
      title = extract_title(from_content)

      dest_dir = os.path.dirname(dest_path)
      if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

      with open(dest_path, 'w') as dest_file:
        page_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", from_html)
        dest_file.write(page_content)

def generate_pages(content_dir, template_path, public_dir):
  for root, dirs, files in os.walk(content_dir):
    for file in files:
      if file.endswith('.md'):
        md_path = os.path.join(root, file)
        rel_path = os.path.relpath(md_path, content_dir)
        
        if file == "index.md":
            dest_rel_path = os.path.join(os.path.dirname(rel_path), "index.html")
        else:
            dest_rel_path = rel_path.replace(".md", ".html")
        
        dest_path = os.path.join(public_dir, dest_rel_path)
        generate_page(md_path, template_path, dest_path)
  
def main():
  copy_to_dir("./static", "./public")
  generate_pages("./content", "./template.html", "./public")

if __name__ == "__main__":
  main()
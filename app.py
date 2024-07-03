import os
import markdownify
from pathlib import Path
from bs4 import BeautifulSoup
import ImageBlockConverter
from ImageBlockConverter import ImageBlockConverter
from utils import extract_frontmatter, emit_frontmatter

def md(html, **options):
    return ImageBlockConverter(**options).convert(html)



def transform_files(directory: str):
    
    if directory.strip() == "":
        print("Please enter a valid path to the directory containing the HTML files.")
        exit(1)

    directory_path = os.path.abspath(directory)
    # Get a list of all files in the directory
    files = os.listdir(directory_path)

    # Filter the list to only include HTML files
    html_files = [file for file in files if file.endswith('.html')]

    # Loop through each HTML file
    for html_file in html_files:
        file_type = None

        # Check if the file is a draft
        if html_file.startswith('draft_'):
            file_type = "drafts"

        # Open the file and read its content
        with open(os.path.join(directory_path, html_file), 'r', encoding='utf8') as file:
            content = file.read()

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')

            # If the file is not a draft, check if it's a story or a comment
            if file_type is None:
                if soup.find('h3') is not None:
                    file_type = "stories"
                else:
                    file_type = "comments"

            # Select the section with the attribute data-field="body"
            section = soup.select_one('section[data-field="body"]')

            if section:
                # If the directory for the file type doesn't exist, create it
                if not os.path.exists(os.path.join(directory_path,file_type)):
                    os.makedirs(os.path.join(directory_path,file_type))

                html_content = str(section)
                
                frontmatter = extract_frontmatter(content)

                # Convert the content of the section to Markdown
                ##markdown_content = markdownify.markdownify(str(section))
                markdown_content = md(html_content)

                # Create a new file name with the .md extension
                md_file = os.path.splitext(html_file)[0] + '.md'
                
                # Define the path where the Markdown file will be saved
                file_path = os.path.join(directory_path, file_type, md_file)

                # Open the Markdown file and write the content
                with open(os.path.join(directory_path, file_type, md_file), 'w', encoding='utf8') as md_file:
                    print(f"Adding <{html_file}> to the {file_type} subdirectory...")
                    md_file.write(emit_frontmatter(**frontmatter))
                    md_file.write("---\n")
                    md_file.write(markdown_content)

if __name__ == "__main__":
    directory = input("Enter the path to the directory containing the HTML files: ")
    transform_files(directory)
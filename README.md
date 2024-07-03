# medium-story-parser
Tool to help identify published stories and convert to Markdown

Forked from [jhsu98/medium-story-parser](https://github.com/jhsu98/medium-story-parser)

## Enhancments 

- Accept source directory path from commandline + basic validation
- Extract frontmatter metadata from Medium HTML file
- Emit frontmatter at start of markdown file
- Custom MarkdownExtractor to add two new lines when dealing with Image element
- Test folder with sample medium html files
- Added requirements.txt

Looks like this!
![With Frontmatter](/MarkdownMetadata.png)
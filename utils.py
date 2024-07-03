from datetime import date, datetime
from typing import List, Optional, Dict, Any
from bs4 import BeautifulSoup


def normalise_nbsp(content: str):
    return content.replace('\xa0', ' ')

def extract_fields_from_html(html_content: str, selectors: Dict[str, str]) -> Dict[str, Any]:
    """
    Extract fields from an HTML file using BeautifulSoup and provided selectors.
    
    :param html_content: Content of the HTML file
    :param selectors: Dictionary of field names and their corresponding CSS selectors
    :return: Dictionary of extracted fields
    """


    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Dictionary to store the extracted fields
    extracted_fields = {}

    # Extract fields based on provided selectors
    for field_name, selector in selectors.items():
      elements = soup.select(selector)
      if elements:
          if field_name.endswith('_href'):  # Special handling for href attributes
              extracted_fields[field_name] = elements[0].get('href')
          elif len(elements) > 1:
              extracted_fields[field_name] = [normalise_nbsp(element.get_text(strip=True)) for element in elements]
          else:
              extracted_fields[field_name] = normalise_nbsp(elements[0].get_text(strip=True))
      else:
          extracted_fields[field_name] = None
  
    return extracted_fields

def extract_frontmatter(content: str):
    selectors = {
        "title": "h3",
        "author": "a.p-author",
        "published_on": "time.dt-published",
        "published_at_href": "a.p-canonical",
        "tags": "ul.tags li",
    }
    
    extracted_data = extract_fields_from_html(content, selectors)
    return extracted_data

def emit_frontmatter(
    title: Optional[str] = None,
    author: Optional[str] = None,
    published_on: Optional[date] = None,
    published_at_href: Optional[datetime] = None,
    tags: Optional[List[str]] = None
) -> str:
    # convert string date to datetime and do isoformat
    
    frontmatter = [
        "---",
        f"title: {title or ''}",
        f"author: {author or ''}",
        f"published_on: {published_on if published_on else ''}",
        f"published_at_href: {published_at_href if published_at_href else ''}",
        f"tags: {', '.join(tags) if tags else ''}",
        "---"
    ]
    
    return "\n".join(frontmatter)
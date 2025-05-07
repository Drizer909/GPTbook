import cohere
import os
from ebooklib import epub
import base64
import requests
import json
import random
import ast

# Configure Cohere API
co = cohere.Client("3bCmq9kvPY6LLVjmtqUo2PXpZdZd1SHUz9QLjTbX")

# ClipDrop API key
clipdrop_api_key = "3f666650884ddc67da2cc6343097cdc08eebf59e4dea3731bc481499d2d4a83db46a48e42dd8f763b9a6c804ccd7e291"

def generate_cover_prompt(plot):
    response = co.generate(
        prompt=f"Plot: {plot}\n\n--\n\nDescribe the cover we should create, based on the plot. This should be two sentences long, maximum.",
        max_tokens=100,
        temperature=0.7,
        k=0,
        p=0.75,
        stop_sequences=[],
        return_likelihoods='NONE'
    )
    return response.generations[0].text

def create_cover_image(plot):
    plot = str(generate_cover_prompt(plot))
    
    r = requests.post('https://clipdrop-api.co/text-to-image/v1',
        files={
            'prompt': (None, plot, 'text/plain')
        },
        headers={
            'x-api-key': clipdrop_api_key
        }
    )
    
    if r.ok:
        with open("cover.png", 'wb') as f:
            f.write(r.content)
    else:
        raise Exception(f"Error generating image: {r.text}")

def create_epub(title, author, chapters, cover_image_path='cover.png'):
    book = epub.EpubBook()

    # Set metadata
    book.set_identifier('id123456')
    book.set_title(title)
    book.set_language('en')
    book.add_author(author)

    # Add cover image
    with open(cover_image_path, 'rb') as cover_file:
        cover_image = cover_file.read()
    book.set_cover('cover.png', cover_image)

    # Create chapters and add them to the book
    epub_chapters = []
    for i, chapter_dict in enumerate(chapters):
        full_chapter_title = list(chapter_dict.keys())[0]
        chapter_content = list(chapter_dict.values())[0]
        if ' - ' in full_chapter_title:
            chapter_title = full_chapter_title.split(' - ')[1]
        else:
            chapter_title = full_chapter_title

        chapter_file_name = f'chapter_{i+1}.xhtml'
        epub_chapter = epub.EpubHtml(title=chapter_title, file_name=chapter_file_name, lang='en')

        # Add paragraph breaks
        formatted_content = ''.join(f'<p>{paragraph.strip()}</p>' for paragraph in chapter_content.split('\n') if paragraph.strip())

        epub_chapter.content = f'<h1>{chapter_title}</h1>{formatted_content}'
        book.add_item(epub_chapter)
        epub_chapters.append(epub_chapter)

    # Define Table of Contents
    book.toc = (epub_chapters)

    # Add default NCX and Nav files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define CSS style
    style = '''
    @namespace epub "http://www.idpf.org/2007/ops";
    body {
        font-family: Cambria, Liberation Serif, serif;
    }
    h1 {
        text-align: left;
        text-transform: uppercase;
        font-weight: 200;
    }
    '''

    # Add CSS file
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    # Create spine
    book.spine = ['nav'] + epub_chapters

    # Save the EPUB file
    epub.write_epub(f'{title}.epub', book)

def write_fantasy_novel(prompt, num_chapters, writing_style):
    # Generate the plot and title in one call
    response = co.generate(
        prompt=f"""Based on this prompt: {prompt}
    
1. Write a detailed plot for a fantasy novel.
2. Give the novel a title.
3. Create a chapter outline with {num_chapters} chapters in this format:
[{{"Chapter 1 - TITLE": "OVERVIEW"}}, {{"Chapter 2 - TITLE": "OVERVIEW"}}, ...]

Format your response exactly as follows:
TITLE: <title>
PLOT: <plot>
CHAPTERS: [{{"Chapter 1 - TITLE": "OVERVIEW"}}, {{"Chapter 2 - TITLE": "OVERVIEW"}}]
""",
        max_tokens=1000,
        temperature=0.9,
        k=0,
        p=0.75,
        stop_sequences=[],
        return_likelihoods='NONE'
    )
    
    # Parse the response
    response_text = response.generations[0].text
    print("Debug - Full response:", response_text)  # Debug print
    
    try:
        title = response_text.split('TITLE:')[1].split('PLOT:')[0].strip()
        plot = response_text.split('PLOT:')[1].split('CHAPTERS:')[0].strip()
        chapters_json = response_text.split('CHAPTERS:')[1].strip()
        
        # Clean up the JSON string
        chapters_json = chapters_json.replace('\n', ' ').replace('  ', ' ')
        print("Debug - Chapters JSON:", chapters_json)  # Debug print
        
        chapter_titles = ast.literal_eval(chapters_json)
    except Exception as e:
        print(f"Error parsing response: {e}")
        # Fallback to manual parsing if JSON parsing fails
        lines = response_text.split('\n')
        title = ""
        plot = ""
        chapter_titles = []
        
        for line in lines:
            if line.startswith('TITLE:'):
                title = line.replace('TITLE:', '').strip()
            elif line.startswith('PLOT:'):
                plot = line.replace('PLOT:', '').strip()
            elif 'Chapter' in line and '-' in line:
                parts = line.split('-', 1)
                if len(parts) == 2:
                    chapter_num = parts[0].strip()
                    title_and_overview = parts[1].strip()
                    if ':' in title_and_overview:
                        chapter_title, overview = title_and_overview.split(':', 1)
                        chapter_titles.append({f"{chapter_num} - {chapter_title.strip()}": overview.strip()})
    
    novel = f"Title: {title}\nPlot: {plot}\n\n"
    chapters = []
    
    # Generate all chapters in one call
    chapter_prompts = []
    for i, chapter_dict in enumerate(chapter_titles):
        chapter_title = list(chapter_dict.keys())[0]
        chapter_overview = list(chapter_dict.values())[0]
        chapter_prompts.append(f"Chapter {i+1}: {chapter_title}\nOverview: {chapter_overview}")
    
    chapters_prompt = f"""Write {num_chapters} chapters for a fantasy novel with this plot: {plot}
Writing style: {writing_style}

Here are the chapter outlines:
{chr(10).join(chapter_prompts)}

Format each chapter as:
CHAPTER 1:
<chapter text>
CHAPTER 2:
<chapter text>
...and so on.
"""
    
    response = co.generate(
        prompt=chapters_prompt,
        max_tokens=2000,
        temperature=0.9,
        k=0,
        p=0.75,
        stop_sequences=[],
        return_likelihoods='NONE'
    )
    chapters_text = response.generations[0].text
    
    # Parse the chapters
    for i in range(num_chapters):
        chapter_marker = f"CHAPTER {i+1}:"
        next_chapter_marker = f"CHAPTER {i+2}:" if i < num_chapters - 1 else None
        
        if next_chapter_marker:
            chapter_content = chapters_text.split(chapter_marker)[1].split(next_chapter_marker)[0].strip()
        else:
            chapter_content = chapters_text.split(chapter_marker)[1].strip()
        
        novel += f"\n{chapter_marker}\n{chapter_content}\n"
        chapters.append(chapter_content)
    
    return novel, title, chapters, chapter_titles

# Example usage:
if __name__ == "__main__":
    prompt = "A kingdom hidden deep in the forest, where every tree is a portal to another world."
    num_chapters = 2  # Minimal test with just 2 chapters
    writing_style = "Clear and easily understandable, similar to a young adult novel. Highly descriptive and sometimes long-winded."
    novel, title, chapters, chapter_titles = write_fantasy_novel(prompt, num_chapters, writing_style)

    # Replace chapter descriptions with body text in chapter_titles
    for i, chapter in enumerate(chapters):
        chapter_number_and_title = list(chapter_titles[i].keys())[0]
        chapter_titles[i] = {chapter_number_and_title: chapter}

    # Create the cover
    create_cover_image(str(chapter_titles))

    # Create the EPUB file
    create_epub(title, 'AI', chapter_titles, 'cover.png') 
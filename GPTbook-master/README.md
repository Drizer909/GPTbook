# GPTBOOK

This project utilizes Cohere's AI API and Stable Diffusion to generate original fantasy novels. Users can provide an initial prompt and specify the number of chapters, and the AI will generate a complete novel, outputting an EPUB (Electronic Publication) file compatible with e-book readers.

## Features

- Generate complete fantasy novels from a simple prompt
- Customizable number of chapters
- AI-generated chapter titles and content
- Automatic cover image generation using ClipDrop API
- EPUB file output compatible with most e-readers

## Requirements

- Python 3.9+
- Cohere API key
- ClipDrop API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Drizer909/GPTbook.git
cd GPTbook
```

2. Install the required packages:
```bash
pip install cohere ebooklib requests
```

3. Set up your API keys:
- Get a Cohere API key from [Cohere's website](https://cohere.ai)
- Get a ClipDrop API key from [ClipDrop's website](https://clipdrop.co)

## Usage

1. Open `gpt_author_new.py`
2. Update the API keys:
```python
co = cohere.Client("YOUR_COHERE_API_KEY")
clipdrop_api_key = "YOUR_CLIPDROP_API_KEY"
```

3. Run the script:
```python
python gpt_author_new.py
```

4. The script will:
   - Generate a plot and title
   - Create chapter outlines
   - Write the content for each chapter
   - Generate a cover image
   - Package everything into an EPUB file

## Recent Updates

- Migrated from Google's Gemini API to Cohere's API for improved reliability
- Added better error handling for API responses
- Streamlined the novel generation process
- Reduced API calls for better efficiency

## Example Output

You can find example novels in the `example_novel_outputs` directory.

## Contributing

Feel free to open issues or submit pull requests for any improvements.

## License

This project is open source and available under the MIT License.





<p align="center">
<img width="453" alt="Screenshot 2023-07-02 at 2 33 27 PM" src="https://github.com/Drizer909/GPTbook/assets/100469278/2244b03c-125d-43b3-91ba-01b2cd9a5a86">
</p>

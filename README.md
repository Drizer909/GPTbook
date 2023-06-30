# gpt-author

This project utilizes a chain of GPT-4 and Stable Diffusion API calls to generate an original fantasy novel. Users can provide an initial prompt and enter how many chapters they'd like it to be, and the AI then generates an entire novel, outputting an EPUB file compatible with e-book readers.

## How It Works

The AI is asked to generate a list of potential plots based on a given prompt. It then selects the most engaging plot, improves upon it, and extracts a title. After that, it generates a detailed storyline with a specified number of chapters, and then tries to improve upon that storyline. Each chapter is then individually written by the AI, following the plot and taking into account the content of previous chapters. Finally, a prompt to design the cover art is generated, and the cover is created. Finally, it's all pulled together, and the novel is compiled into an EPUB file.



In Google Colab, simply open the notebook, add your API keys, and run the cells in order. 

If you are using a local Jupyter notebook, you will need to install the necessary dependencies. You can do this by running the following command in your terminal:

```bash
pip install openai ebooklib requests
```

In the last cell of the notebook, you can customize the prompt and the number of chapters for your novel. For example:
This will generate a novel based on the given prompt with 20 chapters. Note -- prompts with less than 7 chapters tend to cause issues.





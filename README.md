# ChatGUI
A light-weighted desktop software with unified and user-friendly interface to seamlessly interact with multiple large language models (LLMs)

# Table of Contents
- [ChatGUI](#chatgui)
- [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation and Run](#installation-and-run)

## Introduction
Large language models (LLMs) have gained significant attention for their ability to perform diverse tasks through natural language prompts. These models, trained on extensive datasets, provide an accessible interface for users to obtain results by simply describing their requirements. However, with various companies releasing different LLMs, selecting and utilizing the most suitable model has become a challenge. Performance varies across models—some excel in certain tasks while underperforming in others.

To address this, we propose **ChatGUI**, a lightweight desktop application with a unified, user-friendly interface for seamless interaction with multiple LLMs. Focusing on powerful models like GPT and Gemini, accessible via API keys, ChatGUI enables users to compare outputs across different models efficiently and choose the optimal one for their needs.

## Installation and Run

1. Set up a new conda environment
   ```Shell
    conda create -n chatgui python=3.10
    conda activate chatgui
   ```
2. Install the required packages:
   ```Shell
    cd ChatGUI
    pip install -r requirements.txt
   ```
3. Run the desktop app:
   ```Shell
    python main.py
   ```
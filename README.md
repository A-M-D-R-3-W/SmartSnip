# SmartSnip

SmartSnippingTool is a simple screenshot utility with the unique capability to interpret the content of the captured images and provide descriptions with the assistance of OpenAI's GPT-4 Vision (GPT-4V) and integrate text-to-speech functionality. This Python-based desktop application provides a user-friendly interface built using the Customtkinter GUI framework. The application offers various settings for customization and can be an excellent tool for visually impaired users or anyone who wants to extract text-based information from images quickly.

## Features
- **Screenshot Capture**: Allows users to take screenshots of their screen or selected areas.
- **OpenAI GPT-4 Vision Integration**: Analyzes the captured images with the help of GPT-4V for content comprehension and description.
- **Text-to-Speech**: Converts the generated descriptions from GPT-4V into audible speech.
- **Customizable Appearance**: Provides options to change appearance themes and text-to-speech voices.
- **Configuration via `.env` Files**: Utilizes a config.env file for storing user preferences and API keys.

## Installation

Before installing SmartSnippingTool, ensure you have Python installed on your system. Follow these steps:

1. Clone the repository or download the source code:

```bash
git clone https://github.com/<your-github-username>/SmartSnippingTool.git
```

2. Navigate to the cloned repository directory:

```bash
cd SmartSnippingTool
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

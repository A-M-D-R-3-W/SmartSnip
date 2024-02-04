# SmartSnip

SmartSnip is a simple screenshot utility with the capability to interpret the content of the captured images and provide descriptions with the assistance of OpenAI's GPT-4 Vision (GPT-4V) and integrate text-to-speech functionality. This Python-based desktop application provides a user-friendly interface built using the Customtkinter GUI framework. The application offers various settings for customization and can be an excellent tool for visually impaired users or anyone who wants to extract text-based information from images quickly.

## Features
- **Screenshot Capture**: Allows users to take screenshots of their screen or selected areas.
- **OpenAI GPT-4 Vision Integration**: Analyzes the captured images with the help of GPT-4V for content comprehension and description.
- **Text-to-Speech**: Converts the generated descriptions from GPT-4V into audible speech.
- **Customizable Appearance**: Provides options to change appearance themes and text-to-speech voices.
- **Configuration via `.env` Files**: Utilizes a config.env file for storing user preferences and API keys.

## Installation

Before installing SmartSnip, ensure you have Python installed on your system. Follow these steps:

1. Clone the repository or download the source code:

```bash
git clone https://github.com/A-M-D-R-3-W/SmartSnip.git
```

2. Navigate to the cloned repository directory:

```bash
cd SmartSnip
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Starting the Application

To start SmartSnip, use the following command from the root directory of the project:

```bash
python smartSnip.py
```
### Taking Screenshots

- Click the **New Snip** button to start the snipping tool.
- Select the area of the screen you want to capture.

### Interpreting Images

- After capturing the screenshot, use the **Interrogate** button to send the image for analysis.
- The response from GPT-4V will be shown in the text area.

### Text-to-Speech

- Once the analysis is done, click the **TTS** button to listen to the spoken version of the text.
- The button will become red to indicate that the speech is being generated. If the button is clicked again, the TTS will be canceled.

### Settings

To customize SmartSnippingTool:

- Click the **Settings** button to adjust appearance modes, themes, OpenAI API key, TTS voice, and TTS model.
- Changes will be saved automatically, though theme changes will require a restart to take effect.

### Resetting the Application

If you need to reset SmartSnippingTool to its initial state:

- Click the **Reset** button to clear all data and return to the start screen.

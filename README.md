***TO-DO:***

***- Add max tokens settings parameter***

# SmartSnip

SmartSnip is a simple screenshot utility with the capability to interpret the content of the captured images with the assistance of OpenAI's GPT-4 Vision (GPT-4V) and text-to-speech functionality. The main goal here is to provide an easier way to interact with GPT-4V.

⚠️ ***This is currently a work-in-progress, and has only been tested on Windows 11.*** ⚠️

## Demo

https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/297676ea-6182-4327-a588-81b536d3fb6e

## Installation

Before installing SmartSnip, ensure you have Python 3.10 installed on your system. Follow these steps:

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

Alternatively, on ***Windows***, you can run ***smartSnip.vbs***

⚠️ Upon the first open, your OpenAI API key ***must be changed***. This is located in the **Settings** window within the program, or can be accessed from **config.env**. An OpenAI API key can be acquired [Here](https://platform.openai.com/api-keys).

### Taking Screenshots

- Click the **New Snip** button to start the snipping tool.
- Select the area of the screen you want to capture (**ESC** can by clicked while dragging to cancel the snip).

### Interpreting Images

- Type your question in the text box at the top. If left empty, it will submit *"What is in this image?"* by default.
- After capturing the screenshot, use the **Send** button to send the image for analysis.
- The response from GPT-4V will be shown in the text area.

### Text-to-Speech

- Once the analysis is done, click the **TTS** button to listen to the spoken version of the text.
- The button will become red to indicate that the speech is being generated. If the button is clicked again, the TTS will be canceled.

### Settings

To customize SmartSnip:

- Click the **Settings** button to adjust appearance modes, themes, OpenAI API key, TTS voice, and TTS model.
- Changes will be saved automatically, though theme changes will require a restart to take effect. Also, saving your OpenAI API Key requires pressing the "Save" button on the right.
- Note: changes can also be made by adjusting **config.env** manually, though this is not recommended as all settings can be accessed from within the application (with the exception of the window icon).

### Resetting the Application

If you need to reset SmartSnippingTool to its initial state:

- Click the **Reset** button to clear all data and return to the start screen.

## Themes

|                |      blue      |     darkblue   |      green     |      coffee    |       rose     |      violet    |      marsh     |      carrot    |     sky        |      red       |     pink       |     metal      |
|     :---:      |     :---:      |     :---:      |     :---:      |     :---:      |     :---:      |     :---:      |     :---:      |     :---:      |     :---:      |     :---:      |     :---:      |     :---:      |
|     Light      |        ![blue-light](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/d6d9e6bf-3694-49ff-af26-451fdbcf4376)        |       ![darkblue-light](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/c97f3939-5b8e-473f-af5e-b35698df056a)         |        ![green-light](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/9a71b152-7db9-431e-bd5c-8efaee6dfa95)        |        ![coffee-light](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/ae99b767-9003-4773-8010-bd01a3ff9c4a)        |       ![rose-light](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/17dcc37f-3242-4262-8949-5ebf08e500e0)         |        ![violet-light](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/fa10a7c6-c961-4dcc-98c4-941b2c6de237)        |        ![marsh-light](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/d508bec8-d679-40ee-a0e2-9a14e921b17c)        |    ![carrot-light](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/7657516b-a304-4585-bb0b-cd6503df420c)            |       ![sky-light](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/5dab8eae-ebf1-4ec6-8fff-b6d5d0aea590)         |        ![red-light](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/99575cdd-b5a3-4a18-b5fc-e5b0c3211c99)        |         ![pink-light](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/3fa080f8-1355-4336-b0dd-03634015198b)       |        ![metal-light](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/f8ac2e74-b40d-4ce7-8a6c-a58d4677b905)        |
|     Dark       |       ![blue-dark](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/e71605db-3c75-415f-828e-153d51d67f24)         |      ![darkblue-dark](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/78ab13a1-0a84-4c3d-b5a7-c22e85f7343a)          |        ![green-dark](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/d684271c-cb2c-4192-8727-31790cf7b6ba)        |        ![coffee-dark](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/520c6f5f-9192-4131-b3db-57b713849155)        |       ![rose-dark](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/26cb2c69-2f2d-438b-8832-b4fd2b4b5a79)         |        ![violet-dark](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/01a2f8e4-7cf4-43ce-96cb-236c509b44e1)        |         ![marsh-dark](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/39017f98-7a5c-4095-8b64-a335198b7663)       |           ![carrot-dark](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/0c17cf5f-ceae-4ca2-91ec-74118779cf7f)     |       ![sky-dark](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/8e83fd7b-4fe6-468e-8880-e812aa810ad3)         |     ![red-dark](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/59cb6a8a-dd34-4223-890e-31de379a8766)           |          ![pink-dark](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/956ee354-5ed3-450c-96c6-ac824a3a94ef)       |         ![metal-dark](https://github.com/A-M-D-R-3-W/SmartSnip/assets/84816543/5e83f383-bcf0-4b83-a56e-406e117cc22d)       |


## Adding Custom Themes

Custom themes can be added by doing the following:

1. Drop your theme file (mytheme.json) into the **/themes** folder in the main directory.
2. Add the path to the **themeDict** dictionary within **smartSnip.py**. Follow the existing convention ('mytheme': 'themes/mytheme.json')
3. In order for the new theme to appear in the **Settings** window, **self.settings.theme_optionmenu** within the **settings_window** function must be modified to add the name you assigned it in the dictionary to the widget. (values=['blue', ...., 'mytheme'])

***I suggest creating new themes using [ctk_theme_builder](https://github.com/avalon60/ctk_theme_builder)***

## Contributing

This is very much a WIP, and as such contributions are greatly appreciated!

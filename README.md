# conversational-ai-forensic

## Overview 

Before using this project, you sould obtain the conversation data. There are several different method to obtain data depending on the service. 

### ChatGPT
``conversations.json`` from ChatGPT website (settings > data control > export data)

### Google Gemini
``MyActivity.json`` from Google Takeout Service (https://takeout.google.com/). You can obtain the data throught 'My Activity Log' in Google Takeout. Note that you must choose the JSON option when exporting the data. 

### Claude
``claude_chat_data.json`` from Chrome extensions
1. Download the folder /claude/chrome extensions
2. Open the Chrome browser and enter ``chrome://extensions`` into the URL bar
3. Activate ``Developer mode`` in the top right and click ``Load unpacked``
4. Select the folder you downloaded 
5. Go to ``claude.ai`` website and login
6. Launch ``Claude Export Conversation Data`` and click ``Download JSON`` on the list page (``claude.ai./chats``)

## Installation 

1. Clone this repository
```
git clone https://github.com/kninami/chatgptForensics.git
```

2. Create and activate a virtual environment (in root folder)
```
python -m venv venv
source venv/bin/activate
```

3. Install dependencies using pip
```
pip install -r requirements.txt
```

## Usage

1. **parsed_data.py** : Run this script to parse data and display it as forensic data. 
```
python parse_data.py /path/to/data.json 
```
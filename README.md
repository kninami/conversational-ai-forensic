# conversational-ai-forensic

## Overview 

This is a Python Project consisting of two scripts: one for parsing data and disaplying it as forensic data(including the hash value of each chat log), and another for drawing graphs based on the parsed data.

Before using this project, you sould obtain ``conversations.json`` from ChatGPT website (settings > data control > export data)

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
python parse_data.py /path/to/conversations.json 
```

2. **draw_graph.py** : Run this script to draw graphs based on the parsed data
```
python draw_graph.py /path/to/chatgpt_parsed_cat_log.csv 
```
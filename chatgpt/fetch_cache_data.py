import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
directory_path = os.path.expanduser('~/Library/Caches/com.openai.chat/fsCachedData')

saved_path = os.path.join(current_dir, 'chatlog')
os.makedirs(saved_path, exist_ok=True)

for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        data = {"content": content}
        
    json_filename = f"{os.path.splitext(filename)[0]}.json"
    json_path = os.path.join(saved_path, json_filename)

    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)
    
    print(f"Converted {filename} to {json_filename}")
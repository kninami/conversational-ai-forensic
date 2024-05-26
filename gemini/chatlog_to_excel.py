import sys
import json 
import pandas as pd

def main(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        convo_list = json.load(f)
        main_chat_array = []
        
        for convo in convo_list:
            #Null check
            if convo.get("safeHtmlItem") and len(convo["safeHtmlItem"]) > 0:
                html_content = convo["safeHtmlItem"][0].get("html", "")
            else:
                html_content = ""
            
            #Null check
            if convo.get("subtitles") and len(convo["subtitles"]) > 0:
                subtitle_name = convo["subtitles"][0].get("name", "")
            else:
                subtitle_name = ""

            #append data to array
            common_data = {
                "created_at": convo["time"],
                "prompt": convo["title"].replace("Prompted ", "", 1) if convo["title"].startswith("Prompted ") else convo["title"],
                "answer": html_content,
                "etc": subtitle_name
            }
            main_chat_array.append(common_data)
            
        df = pd.DataFrame(main_chat_array)

        #export to excel file
        with pd.ExcelWriter('gemini_parsed_data.xlsx') as writer:
            df.to_excel(writer, sheet_name='Conversation List', index=False)
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chatlog_to_excel.py </path/to/calude_chat_data.json>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
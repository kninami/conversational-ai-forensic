import sys
import json 
import re
import pandas as pd
from urllib.parse import urlparse

def extract_domains(html_content):
    url_pattern = r'(https?://[^\s]+)'
    urls = re.findall(url_pattern, html_content)
    
    domains = set() 
    for url in urls:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc  
        domains.add(domain)
        
    return list(domains)  

def main(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        convo_list = json.load(f)
        
        main_chat_array = []
        metadata_array = []
        
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
                        
            #append url data to array
            if 'http' in html_content:
                url_array = extract_domains(html_content)
                for url in url_array:
                    metadata_array.append({
                        "url": url,
                        **common_data,
                    }) 
            
            main_chat_array.append(common_data)

        df = pd.DataFrame(main_chat_array)
        webpage_df = pd.DataFrame(metadata_array)

        #export to excel file
        with pd.ExcelWriter('gemini_parsed_data.xlsx') as writer:
            df.to_excel(writer, sheet_name='Conversation List', index=False)
            webpage_df.to_excel(writer, sheet_name='Webpage List', index=False)
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chatlog_to_excel.py </path/to/calude_chat_data.json>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
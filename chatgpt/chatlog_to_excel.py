import sys
import json 
import pandas as pd
from datetime import datetime

def main(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        convo_list = json.load(f)
        
        main_chat_df_array = []
        attachment_df_array = []
        webpage_df_array = []

        for convo in convo_list:
            create_time = convert_unix_time_to_readable(convo["create_time"])
            update_time = convert_unix_time_to_readable(convo["update_time"])
            
            #parse conversation history to dataFrame
            message_list = convo["mapping"]
            
            main_chat_data = [] #for chat message
            attachment_data = [] #for attachment file
            metadata_list_data = [] #for url
            
            for uuid, info in message_list.items():
                message = info.get("message")                
                if(message is not None): 
                    #create main chat list 
                    common_data = {
                        "conversation_id": convo["conversation_id"],
                        "title": convo["title"],
                        "created_at": create_time,
                        "updated_at": update_time,
                        "message_id": uuid,
                        "message_created_at": convert_unix_time_to_readable(message.get("create_time")),
                        "author": message.get("author", {}).get("role"),
                        "part": message.get("content", {}).get("parts")
                    }
                    main_chat_data.append(common_data)
                    
                    #create attachments list 
                    attachment_array = message.get("metadata", {}).get("attachments", [])                     
                    if attachment_array:
                        for attachment in attachment_array:                        
                            attachment_data.append({
                                **common_data,
                                "id": attachment["id"],
                                "type": attachment["mime_type"],
                                "name": attachment["name"],
                                "size": attachment["size"],
                            })
                            
                    #create webpage list        
                    metadata_list_array = message.get("metadata", {}).get("_cite_metadata", {}).get("metadata_list", [])
                    if metadata_list_array:
                        for webpage_info in metadata_list_array:
                            metadata_list_data.append({
                                **common_data,
                                "url": webpage_info["url"],
                                "title": webpage_info["title"],
                                "text": webpage_info["text"],
                            })
                                        
            main_chat_df = pd.DataFrame(main_chat_data)
            main_chat_df_array.append(main_chat_df)
            
            attachment_df = pd.DataFrame(attachment_data)
            attachment_df_array.append(attachment_df)
            
            webpage_df = pd.DataFrame(metadata_list_data)
            webpage_df_array.append(webpage_df)
        
        #combine dataframe array        
        combined_df = pd.concat(main_chat_df_array, ignore_index=True)
        combined_attachment_df = pd.concat(attachment_df_array, ignore_index=True)
        combined_webpage_df = pd.concat(webpage_df_array, ignore_index=True)
        
        #export to excel file
        with pd.ExcelWriter('chatgpt_parsed_data.xlsx') as writer:
            combined_df.to_excel(writer, sheet_name='Conversation List', index=False)
            combined_attachment_df.to_excel(writer, sheet_name='Attachment List', index=False)
            combined_webpage_df.to_excel(writer, sheet_name='Webpage List', index=False)
     
#convert unix time to readable time              
def convert_unix_time_to_readable(unix_time):
    if (unix_time is not None):
        target_time = datetime.fromtimestamp(unix_time)
        dt_format_str = '%Y-%m-%d %H:%M:%S'
        return target_time.strftime(dt_format_str)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chatlog_to_excel.py </path/to/conversations.json>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
import sys
import json 
import pandas as pd

def main(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        convo_list = json.load(f)
        main_chat_df_array = []
        attachment_df_array = []
        
        for convo in convo_list:
            message_list = convo["chat_messages"]                
            main_chat_data = [] #for chat message
            attachment_data = [] #for attachment file # This should be outside the inner loop

            for message in message_list:
                common_data = {
                    "conversation_id": convo["uuid"],
                    "title": convo["name"],
                    "created_at": convo["created_at"],
                    "updated_at": convo["updated_at"],
                    "message_id": message["uuid"],
                    "message_created_at": message["created_at"],
                    "sender": message["sender"],
                    "text": message["text"]
                }
                main_chat_data.append(common_data)
            
                attachment_array = message.get("files", [])                     
                if attachment_array:
                    for attachment in attachment_array:
                        attachment_data.append({
                            **common_data,
                            "id": attachment["file_uuid"],
                            "thumbnail_url": attachment["thumbnail_url"],
                            "preview_url": attachment["preview_url"],
                        })
                        
            main_chat_df = pd.DataFrame(main_chat_data)
            main_chat_df_array.append(main_chat_df)
        
            attachment_df = pd.DataFrame(attachment_data)
            attachment_df_array.append(attachment_df)
        
    combined_df = pd.concat(main_chat_df_array, ignore_index=True)
    combined_attachment_df = pd.concat(attachment_df_array, ignore_index=True)
    
    #export to excel file
    with pd.ExcelWriter('claude_parsed_data.xlsx') as writer:
        combined_df.to_excel(writer, sheet_name='Conversation List', index=False)
        combined_attachment_df.to_excel(writer, sheet_name='Attachment List', index=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chatlog_to_excel.py </path/to/calude_chat_data.json>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
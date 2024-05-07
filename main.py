from skinport import SkinPort
import pandas as pd
from datetime import datetime
from google_sheets import GoogleSheets
import os
from dotenv import load_dotenv


load_dotenv()
int = SkinPort()
int.authenticate()

current_page=1
res = int.get_transactions(page=current_page)
# print(res["pagination"])

file_name = 'date.txt'
execute_time = datetime.now()

# Open the file in read mode
with open(file_name, 'r') as f:
    # Read the string from the file
    init_date = f.read()

date = datetime.strptime(init_date, "%Y-%m-%dT%H:%M:%S.%fZ")

is_date = False

data = []

while is_date == False:
    if datetime.strptime(res["data"][-1]["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ") > date:
        print(f"Searching page: {current_page}, Date: {res['data'][-1]['created_at']}")

        for item in res["data"]:
            data.append(item)
        
        if current_page + 1 <= res["pagination"]["pages"]:
            current_page += 1
            res = int.get_transactions(page=current_page)

    else:
        for item in res["data"]:
            # print(datetime.strptime(item["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"))
            if datetime.strptime(item["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ") > date:
                data.append(item)
            else:
                print(f"Object created at {item['created_at']}, ignoring next objects.")
                is_date = True
                break

exploded = []
if data:
    for item in data:
        if item["type"] == "purchase" and item["status"] != "canceled":
            for idx, gun in enumerate(item["items"]):
                exploded.append({
                    "id": item["id"],
                    "status": item["status"],
                    "amount": item["amount"],
                    "currency": item["currency"],
                    "sale_id": item["items"][idx]["sale_id"],
                    "market_hash_name": item["items"][idx]["market_hash_name"],
                    "item_amount": item["items"][idx]["amount"],
                    "created_at": item["created_at"],
                    "updated_at": item["updated_at"]
                })
else:
    print("Looks like no new updates, list is empty")


goog = GoogleSheets("./google_key.json")
goog.authenticate()

spreadsheet = goog.client.open_by_url(os.getenv("DRIVE_URL"))
worksheet = spreadsheet.worksheet("Purchases")

exploded_list = [list(item.values()) for item in exploded]
worksheet.append_rows(exploded_list)

with open(file_name, 'w') as f:
    # Write the string to the file
    formatted_datetime = execute_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-3] + 'Z'
    f.write(formatted_datetime)
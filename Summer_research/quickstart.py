from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'summer-research-2023-bf67a99398ee.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# If modifying these scopes, delete the file token.json.


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1M5cjRWLJ0Ef4CHCmB46yDDnxNB8-9zT5oipe4TT_W8s'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="m=7!V2:V6371").execute()
values = result.get('values', [])

print(values)

counter = 0
numval = 0

for i in range (6370):
    numval += 1
    if values[i] == ['TRUE']:
        counter += 1
    else:
        counter = counter

pertrue = 0.0
pertrue = (counter/numval)
print(pertrue)
print(counter)
print(numval)

test = [[pertrue]]

request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                range="m=7!W2", valueInputOption="USER_ENTERED", body={"values":test}).execute()



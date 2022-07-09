from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class Answer:
    def __init__(self, text, is_right):
        self.text = text
        self.is_right = is_right


class Question:
    def __init__(self, text, answers, question_type=''):
        self.text = text
        self.answers = answers
        self.question_type = question_type


def main(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('../token.json'):
        creds = Credentials.from_authorized_user_file('../token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.get(spreadsheetId=SAMPLE_SPREADSHEET_ID, ranges=SAMPLE_RANGE_NAME, includeGridData=True).execute()
    values = result['sheets'][0]['data'][0]['rowData']

    questions = []

    currentQuestion = None
    currentAnswers = []

    if not values:
        print('No data found.')
    else:
        for row in values:
            if 'userEnteredValue' in row['values'][0]:
                if currentQuestion:
                    currentQuestion.answers = currentAnswers
                    currentAnswers = []
                    questions.append(currentQuestion)
                currentQuestion = Question(text=row['values'][0]['userEnteredValue']['stringValue'], answers=[])
            if len(row['values']) > 1 and 'userEnteredValue' in row['values'][1]:
                color = row['values'][1]['effectiveFormat']['textFormat']['foregroundColor']
                print(row['values'][1]['userEnteredValue'])
                answer_value = row['values'][1]['userEnteredValue']['stringValue'] if 'stringValue' in row['values'][1][
                    'userEnteredValue'] else row['values'][1]['userEnteredValue']['numberValue'] if 'numberValue' in \
                                                                                                    row['values'][1][
                                                                                                        'userEnteredValue'] else \
                row['values'][1]['userEnteredValue']['boolValue']
                if answer_value:
                    answer = Answer(answer_value,
                                is_right=('red' in color and color['red'] == 1))
                    currentAnswers.append(answer)
        currentQuestion.answers = currentAnswers
        questions.append(currentQuestion)

        for i in range(len(questions)):
            count_right = len(list(filter(lambda x: x.is_right, questions[i].answers)))
            if count_right > 1:
                questions[i].question_type = 'checkbox'
            else:
                questions[i].question_type = 'radio'
        return questions
#try:
#main('1f8PXFOSG-hT6dbncYLvupvqolYEpjJS4n_Hkfyh6yXk', 'ИСТМ 2020!A1:C1215')
#except:
    #pass


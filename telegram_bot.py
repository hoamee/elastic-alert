import requests
from message_helper import resolveMessage
# -672756243

def postMessage(chat_id, message, token):
    rq = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', 
                  data={'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'})
    if(rq.status_code != 200):
        send_error(rq.text)
        print(message)

def send_message(message, token):
    postMessage('607758592', message, token)
   
    
def send_error(message, token):
    resolveMessage(message)
    postMessage('607758592', message, token)

def send_file(file_name, token):
    url = f'https://api.telegram.org/bot{token}/sendDocument'
    data={'chat_id': '607758592', 'parse_mode': 'HTML'}
    # Need to pass the document field in the files dict
    files = {
        'document': open(file_name, 'rb')
    }

    r = requests.post(url=url, data=data, files=files, stream=True)

# sample MarkdownV2 text
# *bold \*text*
# _italic \*text_
# __underline__
# ~strikethrough~
# ||spoiler||
# *bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold*
# [inline URL](http://www.example.com/)
# [inline mention of a user](tg://user?id=123456789)
# `inline fixed-width code`
# ```
# pre-formatted fixed-width code block
# ```
# ```python
# pre-formatted fixed-width code block written in the Python programming language
# ```
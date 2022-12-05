import requests
from message_helper import resolveMessage
# -672756243

def postMessage(chat_id, message):
    rq = requests.post('https://api.telegram.org/bot5942148992:AAFuDPwGt9ARdxHlyOuhQT0X3qBRdaDNJ-0/sendMessage', 
                  data={'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'})
    if(rq.status_code != 200):
        print(rq.text)
        print('-----------------')
        print(message)

def send_message(message):
    postMessage('607758592', message)
   
    
def send_error(message):
    resolveMessage(message)
    postMessage('607758592', message)


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
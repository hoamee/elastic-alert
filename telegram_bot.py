import requests
from datetime import datetime
# -672756243
def send_message(message):
    rq_prefix='https://api.telegram.org/bot5942148992:AAFuDPwGt9ARdxHlyOuhQT0X3qBRdaDNJ-0/sendmessage?chat_id=607758592&parse_mode=MarkdownV2&text='
    rq_prefix += message
    rq = requests.get(rq_prefix)
    if(rq.status_code != 200):
        print(rq.text)
        print('-----------------')
        print(rq_prefix)
    
def send_error(message):
    rq_prefix='https://api.telegram.org/bot5942148992:AAFuDPwGt9ARdxHlyOuhQT0X3qBRdaDNJ-0/sendmessage?chat_id=607758592&parse_mode=MarkdownV2&text='
    rq_prefix += message
    rq = requests.get(rq_prefix)

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
def resolveMessage(msg):
    return msg.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def generateIISMessage(ip, msg, trg_time, atk_type):
    msg = resolveMessage(msg)
    message = f'''<b>Phát hiện hành vi nghi ngờ tấn công {atk_type} ⚡️</b>

Host IP: <code>{ip}</code>

Log detail: <code>{msg}</code>

Trigger time: <b>{trg_time}</b> UTC±00:00'''
    
    return message

def generateANMMessage(ip, host_name, host_os, image, target_file, user, msg, trg_time, atk_type):
    msg = resolveMessage(msg)
    message = f'''<b>Phát hiện tiến trình {atk_type} với tham số nghi ngờ</b>

Host ip: <code>{ip}</code>
Host name : <code>{host_name}</code>
Host os: <code>{host_os}</code>
User: <code>{user}</code>

Image : <code>{image}</code>
Target file name: <code>{target_file}</code>

Log detail: <code>{msg}</code>
Trigger time: <b>{trg_time} UTC±00:00</b>'''
    
    return message

def generateMessage(log, atk_type, alert_type):
    rmsg = ''
    if alert_type == 'web-attack':
        msg = log['fields']['message'][0]
        msg_arr = msg.split(' ')
        trg_time = msg_arr[0] + ' ' + msg_arr[1]
        ip = msg_arr[2]
        rmsg = generateIISMessage(ip, msg, trg_time, atk_type)
        
    if alert_type == 'amn':
        msg = log['fields']['message'][0]
        trg_time = '-/-'
        ip = log['fields']['host.ip'][0]
        host_name = log['fields']['host.name'][0]
        host_os = f"{log['fields']['host.os.name'][0]} | {log['fields']['host.os.kernel'][0]}"
        image = log['fields']['winlog.event_data.Image'][0]
        target_file = log['fields']['winlog.event_data.TargetFilename'][0]
        user = log['fields']['winlog.event_data.User'][0]
        rmsg = generateANMMessage(ip, host_name, host_os, image, target_file, user, msg, trg_time, atk_type)
        
    return rmsg


# HTML Sample
# <b>bold</b>, <strong>bold</strong>
# <i>italic</i>, <em>italic</em>
# <u>underline</u>, <ins>underline</ins>
# <s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
# <span class="tg-spoiler">spoiler</span>, <tg-spoiler>spoiler</tg-spoiler>
# <b>bold <i>italic bold <s>italic bold strikethrough <span class="tg-spoiler">italic bold strikethrough spoiler</span></s> <u>underline italic bold</u></i> bold</b>
# <a href="http://www.example.com/">inline URL</a>
# <a href="tg://user?id=123456789">inline mention of a user</a>
# <code>inline fixed-width code</code>
# <pre>pre-formatted fixed-width code block</pre>
# <pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>


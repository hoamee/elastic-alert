def resolveMessage(msg):
    return msg.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def generateIISMessage(ip, msg, trg_time, atk_type):
    msg = resolveMessage(msg)
    message = f'''<b>Phát hiện hành vi nghi ngờ tấn công {atk_type} ⚡️</b>

Host IP: <code>{ip}</code>

Log detail: <code>{msg}</code>

Trigger time: <code>{trg_time} UTC±00:00</code>'''
    
    return message

def generateRdpMessage(host_ip, computer_name, target_user_name, target_domain_name, target_ip, event_created):
    message = f'''<b>Phát hiện hành vi RDP</b>

Event time: <code>{event_created}</code>

Dest IP: <code>{host_ip}</code>
Dest Name: <code>{computer_name}</code>

Domain: <code>{target_domain_name}</code>
User: <code>{target_user_name}</code>

Source IP: <code>{target_ip}</code>
'''
    
    return message

def generateANMMessage(ip, host_name, host_os, image, target_file, user, msg, trg_time, atk_type):
    msg = resolveMessage(msg)
    message = f'''<b>Phát hiện hành vi {atk_type}</b>

Host ip: <code>{ip}</code>
Host name : <code>{host_name}</code>
Host os: <code>{host_os}</code>
User: <code>{user}</code>

Image : <code>{image}</code>
Target file name: <code>{target_file}</code>

Log detail: <code>{msg}</code>
Trigger time: <code>{trg_time} UTC±00:00</code>'''
    
    return message

def generateDefaultMessage(log, spec):
    format = spec["display-fields"]
    message = f'''<b>{format['title']}</b>

'''
    for fo in format['fields']:        
        key = fo['key']
        value = ""
        if key == 'divider':
            message += f'''{fo['value']}
'''
        else:            
            try:
                value = log['fields'][fo['value']][0]
            except:
                value = ""       
            message += f'''{key}: <code>{value}</code>
'''
    return message

def generateMessage(log, spec):
    rmsg = ''
    atk_type = spec['query-name'], 
    alert_type = spec['query-type']
    if alert_type == 'web-attack':
        msg = log['fields']['message'][0]
        msg_arr = msg.split(' ')
        trg_time = msg_arr[0] + ' ' + msg_arr[1]
        ip = msg_arr[2]
        rmsg = generateIISMessage(ip, msg, trg_time, atk_type)
        
    if alert_type == 'anm':
        msg = log['fields']['message'][0]
        trg_time = '-/-'
        ip = '-/-'
        host_name = '-/-'
        host_os = '-/-'
        image = '-/-'
        target_file = '-/-'
        user = '-/-'
        
        try:
            trg_time = log['fields']['winlog.event_data.UtcTime'][0]          
        except:
            pass
        
        try:
            user = log['fields']['winlog.event_data.User'][0]
        except:
            pass
        
        try:
            host_name = log['fields']['host.name'][0]
        except:
            pass
        
        try:
            host_os = f"{log['fields']['host.os.name'][0]} | {log['fields']['host.os.kernel'][0]}"
        except:
            pass
        
        try:
            ip = log['fields']['host.ip'][0]
        except:
            pass
        
        try:            
            image = log['fields']['winlog.event_data.Image'][0]
        except:
            pass
        
        try:
            target_file = log['fields']['winlog.event_data.TargetFilename'][0]  
        except:
            pass
        
        rmsg = generateANMMessage(ip, host_name, host_os, image, target_file, user, msg, trg_time, atk_type)
    
    if alert_type == 'rdp':
        host_ip = '-/-'
        computer_name = '-/-'
        target_user_name = '-/-'
        target_domain_name = '-/-'
        target_ip = '-/-'
        event_created = '-/-'
        
        try:
            host_ip = log['fields']['host.ip'][0]
        except:
            pass
        
        try:
            computer_name = log['fields']['winlog.computer_name'][0]
        except:
            pass
        
        try:
            target_user_name = log['fields']['winlog.event_data.TargetUserName'][0]
        except:
            pass
        
        try:
            target_domain_name = log['fields']['winlog.event_data.TargetDomainName'][0]
        except:
            pass
        
        try:
            target_ip = log['fields']['winlog.event_data.IpAddress'][0]
        except:
            pass
        
        try:
            event_created = log['fields']['event.created'][0]
        except:
            pass
        
        rmsg = generateRdpMessage(host_ip, computer_name, target_user_name, target_domain_name, target_ip, event_created)
    
    if alert_type == 'default':
        rmsg = generateDefaultMessage(log, spec)
        
    return rmsg



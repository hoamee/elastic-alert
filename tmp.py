# s = '2022-12-05 10:17:27 10.20.26.34 GET /Pages/PhanAnhKienNghi.aspx Description=555&DiaChiFull=1&DiaChiSoNha=1&DoiTuong=1&DoiTuongsl=1&Email=sample%40email.tst&FullName=../../../../../../../../../../../../../../etc/passwd&Huyen=1&MaXacNhan=1&PhoneNumber=555-666-0606&Tinh=1&XaPhuong=1&chuDe=24;%23C%C3%A1c%20ho%E1%BA%A1t%20%C4%91%E1%BB%99ng%20li%C3%AAn%20quan%20%C4%91%E1%BA%BFn%20xu%E1%BA%A5t%20kh%E1%BA%A9u%2C%20nh%E1%BA%ADp%20kh%E1%BA%A9u%20h%C3%A0ng%20h%C3%B3a 443 - 10.20.26.43 Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/88.0.4298.0+Safari/537.36 https://bandt.vinhphuc.gov.vn/Pages/home.aspx 200 0 0 236'
# s = s.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
# print(s)
import requests

def resolveMessage(msg):
    return msg.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

s = '2022-12-05 11:44:38 10.20.26.34 GET /Pages/ChiTietPhanAnhKienNghi.aspx Address=3137%20Laguna%20Street&Email=sample%40email.tst&FileAttach=&HoTen=1&IDCauHoi=35&MaXacNhan=1&NoiDung=555&PhoneNumber=555-666-0606&listValueFileAttach=../../../../../../../../../../../../../../etc/passwd&listValueRemoveFileAttach=1 443 - 10.20.26.43 Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/88.0.4298.0+Safari/537.36 https://sotp.vinhphuc.gov.vn/Pages/home.aspx 200 0 0 278'


msg = f'''<b>Phát hiện hành vi nghi ngờ tấn công Directory traversal, RFI and LFI⚡️ </b>

Host IP: <code>10.20.26.34</code>

Log detail: <code>{s}</code>

Trigger time: <b>2022-12-05 11:44:38</b>'''

msg = resolveMessage(msg)

r = requests.post('https://api.telegram.org/bot5942148992:AAFuDPwGt9ARdxHlyOuhQT0X3qBRdaDNJ-0/sendMessage', 
                  data={'chat_id': '607758592', 'text': msg, 'parse_mode': 'HTML'})

print(r.text)
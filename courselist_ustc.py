import re
import urllib2, urllib, cookielib
import pytesseract
from PIL import Image

class mis(object):
    term = '20142'
    mis_path = 'http://mis.teach.ustc.edu.cn/'

    def __init__(self, usercode, password, image_path = 'img.jpg'):
        self.usercode = usercode
        self.password = password
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        opener.open(mis.mis_path + 'userinit.do?userbz=s')
        self.opener = opener
        self.path = image_path

    def get_image(self):
        img = self.opener.open(mis.mis_path + 'randomImage.do').read()
        f = open(self.path, 'wb')
        f.write(img)
        f.close()
        return self;

    def login(self, times = 16):
        for i in range(0, times):
            self.get_image()
            # To make it easy to recognize
            image = Image.open(self.path).point(lambda i: 255 if i > 127 else 0)
            # The verification code
            check = pytesseract.image_to_string(image, 'eng', False, '-psm 6').replace(' ', '')
            data = urllib.urlencode({'userbz': 's', 'hidjym': '', 'userCode': self.usercode, 'passWord': self.password, 'check': check})
            request = urllib2.Request(mis.mis_path + 'login.do')
            page = self.opener.open(request, data).read()
            # The page having tables is avaliable. 
            if page.find('table') != -1:
                return self;
        raise Exception, 'Login Failure! '

    def get_course_list(self):
        page = self.opener.open(mis.mis_path + 'kbcx.do?xklb=B&xq=' + mis.term).read()
        pattern = re.compile(
            r'<td[^>]*>\d*?</td>\s*'
            r'<td[^>]*>(.*?)</td>\s*'
            r'<td[^>]*><a[^>]*><font[^>]*>(.*?)</font></a></td>\s*'
            r'<td[^>]*>(.*?)</td>\s*'
            r'<td[^>]*>(.*?)</td>\s*'
            r'<td[^>]*>(.*?)</td>\s*'
            r'<td[^>]*>(.*?)</td>\s*'
            r'<td[^>]*>(.*?)</td>\s*'
            r'<td[^>]*>(.*?)</td>')
        return pattern.findall(page)

    def get_course_study_list_gc(self, course):
        pattern = re.compile(
            r'<td[^>]*>\d*?</td>\s*'
            r'<td[^>]*>(.*?)</td>\s*'
            r'<td[^>]*>(.*?)</td>\s*'
            r'<td[^>]*>(.*?)</td>\s*'
            r'<td[^>]*>(.*?)</td>\s*')
        page = self.opener.open(mis.mis_path + 'querystubykcbjh.do?tag=gc&xnxq=' + mis.term + '&kcbjh=' + course[0] + '&kczw=' + course[1]).read()
        if page.find('table') == -1:
            raise Exception, 'Login Failure! '
        return pattern.findall(page)
    
    def get_course_study_list_jg(self, course):
        pattern = re.compile(
            r'<td[^>]*>\d*?</td>\s*'
            r'<td[^>]*>(.*?)</td>\s*'
            r'<td[^>]*>(.*?)</td>\s*'
            r'<td[^>]*>(.*?)</td>\s*'
            r'<td[^>]*>(.*?)</td>\s*')
        page = self.opener.open(mis.mis_path + 'querystubykcbjh.do?tag=jg&xnxq=' + mis.term + '&kcbjh=' + course[0] + '&kczw=' + course[1]).read()
        if page.find('table') == -1:
            raise Exception, 'Login Failure! '
        return pattern.findall(page)
    

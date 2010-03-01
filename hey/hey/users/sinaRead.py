import re
import urllib

class SinaRead():
    def extract_links(self,html):
        blocks = re.findall(r'<ul class="list_009">.*?</ul>', html, re.S)
        links = []
        for b in blocks:
            links += re.findall(r'<a href="(\S+)"[^<>]*>([^<>]*)</a>', b)
        return links

    def extract_content(self,html):
        m = re.search('<div id="contTxt" class="contTxt1">.*<p class="pages"><script>', html, re.S)
        return m and self.html_to_text(m.group()) or ''

    def html_to_text(self,html):
        html = re.sub(r'<p>(.*?)</p>', r'\1\n', html)
        html = re.sub(r'<[^<>]*>', '', html)
        return "\n\n" + html.strip() + "\n\n"

    def url_get(self,url):
        u = urllib.urlopen(url)
        c = u.read()
        u.close()
        return c

    def download_book(self,urlindex, filename):
        links = self.extract_links(self.url_get(urlindex))

        fp = open(filename, 'w')
        for link in links:
            u = 'http://vip.book.sina.com.cn/book/' + link[0]
            title = link[1]
            fp.write(title)
            fp.write(self.extract_content(self.url_get(u)))
        fp.close()

#    download_book('http://vip.book.sina.com.cn/book/index_40980.html', '?????.txt')
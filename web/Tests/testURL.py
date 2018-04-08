import web.URL as URL


class TestUrl:
    def test_check(self):
        assert URL.check('http://www.baidu.com') == 'http://www.baidu.com/'
        assert URL.check('www.baidu.com') == 'http://www.baidu.com/'
        assert URL.check('baidu.com') == 'http://baidu.com/'

    def test_clean(self):
        assert URL.clean('http://www.baidu.com/') == 'www.baidu.com'
        assert URL.clean('http://www.baidu.com/s?wd=111&pn=10#ff') == 'www.baidu.com'

    def test_get_main_domain(self):
        assert URL.get_domain('http://www.baidu.com/s?wd=111&pn=10#ff') == 'baidu.com'

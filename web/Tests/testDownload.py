from web.downloads import Download


def test_download():
    print(Download('http://www.baidu.com'))
    print(Download('http://www.adasdasdasdasdasbaidu.com'))

import requests


class Scraper:
    API_DOMAIN = 'https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=no_test&TestID=no_test&appType=1&curr=rub&dest=-1257786&query={0}&resultset=catalog&sort=popular&spp=29&suppressSpellcheck=false'
    PRODUCT_DOMAIN = 'https://www.wildberries.ru/catalog/{0}/detail.aspx'

    def get_item(self, request: str, limit: int = 10) -> dict:
        try:
            tmp = []
            r = requests.get(self.API_DOMAIN.format(request))
            assert r, "bad req"
            items = dict(r.json())['data']['products'][0:limit]
            for i in items:
                tmp.append({'title': f"{i['name']} {i['brand']}", 'link': self.PRODUCT_DOMAIN.format(i['id'])})
            return tmp
        except Exception as e:
            return {'error': 'connection error'}

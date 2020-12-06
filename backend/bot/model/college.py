import requests
import tracemalloc
import asyncio
import re
from pyppeteer import launch
from bs4 import BeautifulSoup
tracemalloc.start()
class College:

    def __init__(self, name: str, site: str, location: str):
        self.name = name;
        self.site = site;
        self.location = location;
        self.page = self.get_page(self.site)

    def query_site(self):
        pass

    def get_page(self, site: str):
        request = requests.get(site)
        soup = BeautifulSoup(request.content, 'html.parser')
        return soup;

    def get_number_tests(self):
        pass

    def get_pos_cases(self):
        pass

    def get_iso(self):
        pass


class UIUC(College):
    def __init__(self):
        College.__init__(self, 'University of Illinois at Urbana Champaign',
                         'https://go.illinois.edu/COVIDTestingData',
                         'Urbana-Champaign, Illinois')

    async def go(self):
        browser = await launch()
        page = await browser.newPage()
        await page.goto(self.site, waitUntil='networkidle2')
        self.page = page
        # await page.screenshot({'path': 'example.png'})
        content = await page.evaluate('document.body.textContent', force_expr=True)
        testsData = re.findall("\\d*,\\d*", content)[1]
        testNum = int(testsData.replace(',',''))
        self.testNum = testNum
        await browser.close()

    def query_site(self):
        pass

    def get_page(self, site: str):
        asyncio.get_event_loop().run_until_complete(self.go())

    def get_number_tests(self):
        return self.testNum

    def get_number_tests(self):
        pass



class UNL(College):
    def __init__(self):
        College.__init__(self, 'University of Nebraska Lincoln',
                         'https://covid19.unl.edu/unl-covid-19-dashboard',
                         'Lincoln, Nebraska')

    async def go(self):
        browser = await launch()
        page = await browser.newPage()
        await page.goto(self.site)
        self.page = page
        element = await page.querySelector('#total-daily-test-total')
        total_str = await page.evaluate('(e) => e.textContent', element)
        total_tests = int(total_str.replace(',',''))
        self.total_tests = total_tests

        element = await page.querySelector('#recent-week-positivity-rate')
        pos_rate = await page.evaluate('(e) => e.textContent', element)
        pos_rate = float(pos_rate)
        self.pos_rate = pos_rate

        element = await page.querySelector('#total-daily-positive-tests')
        pos_cases = await page.evaluate('(e) => e.textContent', element)
        pos_cases = int(pos_cases.replace(',',''))
        self.pos_cases = pos_cases
        await browser.close()

    def query_site(self):
        return {
            'pos_cases': self.pos_cases,
            'total_tests': self.total_tests,
            'pos_rate': self.pos_rate
        }

    def get_page(self, site: str):
        asyncio.get_event_loop().run_until_complete(self.go())

    def get_number_tests(self):
        pass


import requests
from bs4 import BeautifulSoup

from proxy_manager.UrlParser import UrlParser




class UsProxyParser(UrlParser):
    def __init__(self, web_url, bandwithdh=None, timeout=None):
        UrlParser.__init__(self, web_url, bandwithdh, timeout)

    def parse_proxyList(self):
        curr_proxy_list = []
        response = requests.get(self.get_URl(), timeout=self.timeout)

        if not response.ok:
            print("Proxy Provider url failed: {}".format(self.get_URl()))
            return []

        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find("table").select("tbody")

        datasets = []
        for row in table[0].find_all("tr"):
            dataset = row.find_all("td")
            datasets.append(dataset[:2]+[dataset[6]])

        for dataset in datasets:
            proxy_straggler = False
            address = dataset[0].text+':'+dataset[1].text
            proxy = "https://" + address +','+ dataset[2].text
            curr_proxy_list.append(proxy.__str__())

        return curr_proxy_list

    def __str__(self):
        return "UsProxy Parser of '{0}' with required bandwidth: '{1}' KBs" \
            .format(self.url, self.minimum_bandwidth_in_KBs)

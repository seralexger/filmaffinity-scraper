# -*- encoding: utf-8 -*-

#########################################################
#
# Alejandro German
# 
# https://github.com/seralexger/filmaffinity-scraper
#
#########################################################

from proxy_manager.parsers.SslProxiesParser import SslProxiesParser
from proxy_manager.parsers.UsProxyParser import UsProxyParser

class ProxyManager():


    def generate_proxies(self, mode = 'https'):
        
        proxies_list = SslProxiesParser('https://www.sslproxies.org/', timeout=5).parse_proxyList()
        proxyAux =  UsProxyParser('https://www.us-proxy.org/', timeout=5).parse_proxyList()

        if mode == 'https':
            for item in proxyAux:
                item = item.split(',')
                if item[1] == 'yes':
                    proxies_list.append(item[0])

            return proxies_list

        elif mode == 'http':
            proxies_list = []
            for item in proxyAux:
                item = item.split(',')
                if item[1] == 'no':
                    proxies_list.append(item[0].replace('https', 'http'))

            return proxies_list



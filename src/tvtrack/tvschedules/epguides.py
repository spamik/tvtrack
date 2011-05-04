# -*- coding: utf-8 -*-

# plugin pro hledání programů na stránkách epguides.com

import httplib
import re
import datetime

def findNewProgram(program_name):
    # dostal jméno programu a zkusí nalézt nové vydání
    episodes = parseEpisodes(downloadProgramPage('/' + program_name + '/'))

def downloadProgramPage(url):
    # stáhne HTML dané stránky
    conn = httplib.HTTPConnection('epguides.com')
    conn.request('GET', url)
    req = conn.getresponse()
    data = req.read()
    req.close()
    return data

def parseEpisodes(page):
    # z raw stránky udělá seznam epizod - číslo a název epizody, prod # a air date
    lines = page.split('\n')
    content = []
    mode = 'start'
    for i in lines:
        if(mode == 'start' and i.find('<pre>') != -1):
            mode = 'content'
        elif(mode == 'content' and i.find('</pre>') != -1):
            break
        elif(mode == 'content'):
            content.append(i)
    episode_re = re.compile("[\d]+[\s]+(?P<episode>[\d]{1,2}\-[\d]{1,3})[\s]+[\w\d#]*[\s]+(?P<airdate>[\d]{2}/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Noc|Dec)/[\d]{2})[\s]+\<a href='.*'\>(?P<name>.*)\<\/a\>[\s]*$")
    episodes = []
    for i in content:
        m = episode_re.match(i)
        if(m):
            episodes.append(('S' + m.group('episode').replace('-', 'E'), m.group('name'), datetime.datetime.strptime(m.group('airdate'), "%d/%b/%y")))
    return episodes

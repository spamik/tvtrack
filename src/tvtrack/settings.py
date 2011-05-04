# -*- coding: utf-8 -*-

# třída pro načítání nastavení

from datetime import datetime
import os
import re

class TVTrackSettings:
    def __init__(self):
        # konstruktor - načteme konfigurační soubory
        dir = os.path.join(os.environ['HOME'], '.tvtrack')
        rc = os.path.join(dir, 'tvtrack.rc')
        programs = os.path.join(dir, 'programs.rc')
        if(not os.path.isfile(rc) or not os.path.isfile(programs)):
            # konfigurační soubory neexistují
            raise IOError("Please make first configuration files and then run tvtrack")
        self.rcsettings = {}
        self.programs = []
        self.parseRC(rc)
        self.parsePrograms(programs)
        # načtení data poslední kontroly
        last_check = os.path.join(dir, 'last_check')
        if(os.path.isfile(last_check)):
            # soubor existuje - načteme datum poslední kontroly
            f = open(last_check, 'r')
            date = f.readline()
            self.last_check = datetime.strptime(date, "%d/%b/%y")
            f.close()
        else:
            # nemáme datum poslední kontroly, použijeme 1.1.1970
            self.last_check = datetime.strptime("01/Jan/70", "%d/%b/%y")

    def parseRC(self, file):
        # rozparsuje rc soubor s hlavním nastavením
        f = open(file, 'r')
        r = re.compile("^(?P<key>[\w_]+)[\s]?=[\s]?(?P<val>[\w\d]+)$")
        lines = f.readlines()
        for i in lines:
            m = r.match(i)
            if(m):
                self.rcsettings[m.group('key')] = m.group['val']
        f.close()

    def parsePrograms(self, file):
        # rozparsuje soubor se sledovanými programy
        f = open(file, 'r')
        r = re.compile("^(?P<plugin>[\w]+):(?P<program>.*)$")
        lines = f.readlines()
        for i in lines:
            m = r.match(i)
            if(m):
                self.programs.append((m.group('plugin'), m.group('program')))
        f.close()

    def getPrograms(self):
        # vrátí seznam hlídaných programů
        return self.programs

    def getLastCheck(self):
        return self.last_check
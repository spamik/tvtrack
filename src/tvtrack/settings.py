# -*- coding: utf-8 -*-

# třída pro načítání nastavení

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
        self.parseRC(rc)
        self.parsePrograms(programs)
        self.rcsettings = {}
        self.programs = []

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


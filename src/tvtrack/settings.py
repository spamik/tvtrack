# -*- coding: utf-8 -*-

# třída pro načítání nastavení

from datetime import datetime
import os
import re

GLOBAL_RC_FILE = 'tvtrack.rc'
PROGRAM_RC_FILE = 'programs.rc'
LASTCHECK_FILE = 'last_check'
LASTCHECK_FORMAT = '%d/%b/%y'

class TVTrackSettings:
    def __init__(self):
        # konstruktor - načteme konfigurační soubory
        dir = self.getConfigDir()
        rc = os.path.join(dir, GLOBAL_RC_FILE)
        programs = os.path.join(dir, PROGRAM_RC_FILE)
        if(not os.path.isfile(rc) or not os.path.isfile(programs)):
            # konfigurační soubory neexistují
            raise IOError("Please make first configuration files and then run tvtrack")
        self.rcsettings = {}
        self.programs = []
        self.parseRC(rc)
        self.parsePrograms(programs)
        # načtení data poslední kontroly
        last_check = os.path.join(dir, LASTCHECK_FILE)
        if(os.path.isfile(last_check)):
            # soubor existuje - načteme datum poslední kontroly
            f = open(last_check, 'r')
            date = f.readline()
            self.last_check = datetime.strptime(date, LASTCHECK_FORMAT)
            f.close()
        else:
            # nemáme datum poslední kontroly, použijeme 1.1.1970
            self.last_check = datetime.strptime("01/Jan/70", LASTCHECK_FORMAT)

    def getConfigDir(self):
        # vrátí složku s konfigurací
        return os.path.join(os.environ['HOME'], '.tvtrack')

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
        r = re.compile("^(?P<plugin>[\w]+):\"(?P<program>[^\"]+)\":(?P<url>.*)$")
        lines = f.readlines()
        for i in lines:
            m = r.match(i)
            if(m):
                self.programs.append((m.group('plugin'), m.group('url'), m.group('program')))
        f.close()

    def getPrograms(self):
        # vrátí seznam hlídaných programů
        return self.programs

    def getLastCheck(self):
        return self.last_check

    def updateLastCheck(self):
        # nastaví poslední kontrolu na aktuální datum
        f = open(os.path.join(self.getConfigDir(), LASTCHECK_FILE), 'w')
        f.write(datetime.strftime(datetime.today(), LASTCHECK_FORMAT))
        f.close()

    def getSMTP(self):
        # vrátí SMTP server, přes který posílat zprávy
        return self.rcsettings['smtp_host']

    def getTo(self):
        # vrátí adresu kam posílat notifikace
        return self.rcsettings['to']

    def getFrom(self):
        # vrátí adresu od koho notifikace bude
        return self.rcsettings['from']

    def getSubject(self):
        # vrátí šablonu na předmět zprávy
        return self.rcsettings['subject']

    def getBody(self):
        # vrátí šablonu na tělo zprávy
        return self.rcsettings['body']

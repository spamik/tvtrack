#!/usr/bin/python
# -*- coding: utf-8 -*-

# TVTrack - nástroj pro automatické notifikace na nové seriály

from tvtrack.settings import TVTrackSettings
import imp
from datetime import datetime

def main():
    try:
        st = TVTrackSettings()
    except IOError:
        print "Konfiguracni soubory nebyly nalezeny. Vytvorte prosim napred konfiguraci."
    programs = st.getPrograms()
    new_epizodes = []
    for i in programs:
        f, file, desc = imp.find_module(i[0], ['tvtrack/tvschedules'])
        module = imp.load_module(i[0], f, file, desc)
        for i in module.findNewProgram(i[1], st.getLastCheck()):
            new_epizodes.append(i) # přidáme si do seznamu nové nalezené epizody
    for i in new_epizodes:
        print "Nalezena nova epizoda:", i['episode'], "(" + i['name'] + ")", "odvysilana", datetime.strftime(i['aired'], "%d.%m.%Y")

main()

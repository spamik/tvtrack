#!/usr/bin/python
# -*- coding: utf-8 -*-

# TVTrack - nástroj pro automatické notifikace na nové seriály

from tvtrack.settings import TVTrackSettings
import imp

def main():
    try:
        st = TVTrackSettings()
    except IOError:
        print "Konfiguracni soubory nebyly nalezeny. Vytvorte prosim napred konfiguraci."
    programs = st.getPrograms()
    for i in programs:
        f, file, desc = imp.find_module(i[0], ['tvtrack/tvschedules'])
        module = imp.load_module(i[0], f, file, desc)
        module.findNewProgram(i[1])

main()

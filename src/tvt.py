#!/usr/bin/python
# -*- coding: utf-8 -*-

# TVTrack - nástroj pro automatické notifikace na nové seriály

from tvtrack.settings import TVTrackSettings
import imp
from datetime import datetime

def fillTemplate(template, program, episode, episode_name, airdate, dateformat):
    # vyplní šablonu hodnotami
    s = template.replace('%n', program)
    s = s.replace('%e', episode)
    s = s.replace('%f', episode_name)
    s = s.replace('%a', datetime.strftime(airdate, dateformat))
    return s

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
        for j in module.findNewProgram(i[1], st.getLastCheck()):
            j['program'] = i[2]
            new_epizodes.append(j) # přidáme si do seznamu nové nalezené epizody
    for i in new_epizodes:
        subject = fillTemplate(st.getSubject(), i['program'], i['episode'], i['name'], i['aired'], st.getDateFormat())
        body = fillTemplate(st.getBody(), i['program'], i['episode'], i['name'], i['aired'], st.getDateFormat())
        print "Subject:", subject
        print ""
        print body
    st.updateLastCheck()

main()

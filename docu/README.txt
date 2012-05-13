TVTrack 0.1

TVTrack je jednoduchý program psaný v Pythonu pro sledování nových dílů
seriálů. Podle televizního programu zjišťuje, zda vyšel nový díl některého
ze sledovaných seriálů a v případě že ano, pošle e-mailovou notifikaci
podle nadefinované šablony. Jednotlivé televizní programy, ve kterých
se vyhledává, lze přidávat jako pluginy.


Požadavky

- Python verze 2.x
- Zkoušeno na Linuxu, pravděpodobně funguje i na Windows (jen je potřeba najít home)


Instalace

Archiv stačí kamkoliv rozbalit. Kontrola se spouští pomocí tvt.py (tedy udělat tvt.py
spustitelným anebo jej spustit jako "python tvt.py"). Před prvním spuštěním je třeba
tvtrack napřed nakonfigurovat.


Konfigurace

Program má dva konfigurační soubory:
- tvtrack.rc - slouží k nastavení samotného programu
- programs.rc - slouží k definici sledovaných seriálů

Oba dva konfigurační soubory se nacházejí ve složce .tvtrack, která je v home
adresáři uživatele, který tvtrack spouští. Složku je třeba napřed vytvořit.

Parametry souboru tvtrack.rc:

smtp_host = SMTP server, přes který se budou posílat e-maily s notifikací
to = E-mailová adresa, kam se notifikace posílají
from = E-mailová adresa, která bude v políčku From zaslané notifikace
subject = Předmět e-mailu s notifikací
body = Tělo e-mailu s notifikací
dateformat = formát data, v jakém se vloží do notifikace - formát jako pro datetime modul pythonu (např. %d.%m.%Y)

V nastaveních subject a body lze použít proměnné, které se nahrazují aktuálními informacemi podle
seriálu. Lze použít:
- %n - jméno seriálu
- %e - číslo epizody
- %f - jméno epizody
- %a - datum odvysílání (datum se formátuje podle hodnoty dateformat)

Soubor programs.rc už obsahuje samotné seriály, které se sledují. Má tento formát:
plugin_tv_programu:"jméno seriálu":identifikátor_seriálu

- jméno seriálu se použije jen v notifikaci (je to to, co se nahradí za proměnnou %n)
- identifikátor seriálu je to, co se předá pluginu a podle čeho to plugin musí najít

Řádek pro seriál How I Met Your Mother z programu epguides vypadá například takto:
epguides:"How I Met Your Mother":HowIMetYourMother


Rozšíření


Licence


--

Jan Krajdl aka SPM, spm@spamik.cz, 2012

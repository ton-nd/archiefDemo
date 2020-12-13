#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Zoeken

   Dit zoekprogramma is bedoeld voor intern gebruik en is alleen
   lokaal te raadplegen.

   De rijnummers in het overzicht komen niet helemaal overeen met de
   rijnummers in het Excelbestand omdat Excel begint met rijnummer 1
   en de module xlrd begint met rijnummer 0.
   Een Excel-rijnummer = xlrd-rijnummer + 1

   Gebruikte bestanden:

   ZoekenDemo.py
   zoeken_fotopresentatie16.py
   handleiding.txt
   opmerkingen.txt
   zoekenDemo.xlsx

   foto_presentatie is een list van alle gegevens + pad van
        afbeeldingen in de functie fotopresentatie

"""

import os
import sys
import glob
from tkinter import LabelFrame, Listbox, Entry, messagebox
from tkinter import Tk, Label, Button, Scrollbar, Menu, filedialog
import xlrd

from zoeken_fotopresentatie16d import fotopresentatie

global foto_presentatie

geg_dict = dict()  # In de dictionary D staan alle gegevens van een record

VERSIE = "Demo"  # datum: 12-12-2020  13:00


def zoekwoord_wissen():
    zoekwoord1_invoer.delete(0, 'end')
    zoekwoord1_invoer.focus()
    zoekwoord2_invoer.delete(0, 'end')


def overzicht_wissen():
    overzicht.delete(0, 'end')


def zoeken():
    """Zoek na aanklikken van knop Zoeken """
    overzicht_wissen()
    zoekwoord1 = zoekwoord1_invoer.get()
    zoekwoord2 = zoekwoord2_invoer.get()
    # Verwissel zoekwoorden als eerste zoekwoord niet opgegeven is.
    if zoekwoord1 == "" and zoekwoord2 != "":
        zoekwoord1 = zoekwoord2
        zoekwoord2 = ""
    # Aanhalingstekens verwijderen
    if zoekwoord1.find('"') != -1:
        zoekwoord1 = zoekwoord1.replace('"', '')
    if zoekwoord2.find('"') != -1:
        zoekwoord2 = zoekwoord2.replace('"', '')
    # ALS het eerste zoekwoord niet leeg is, ga zoeken.
    if zoekwoord1 != "":
        zoek_data(zoekwoord1, zoekwoord2)


def zoeken_enter(event):
    """Zoek na indrukken van de knop ENTER."""
    zoeken()


def print_kop(zoekwoord1, zoekwoord2):
    """Print zoekwoord(en) + info over '>' bovenaan overzicht """
    overzicht_wissen()
    overzicht.insert('end', " ")
    overzicht.insert(
        'end', " Zoekwoord(en): " + zoekwoord1 + " " + zoekwoord2, )


def print_regels(tekst, zoekresultaten):
    """Print kop boven de zoekresultaten van een categorie + resultaten """
    if zoekresultaten:
        overzicht.insert('end', " ")
        overzicht.insert('end', " " + tekst + " - "
                         + str(len(zoekresultaten)))
        overzicht.insert('end', " ")
        for i in zoekresultaten:
            overzicht.insert('end', i)


def verzamel_gegevens(categorie, rowidx):
    """Vul dictionary D met gegevens van 1 Excelrecord """
    sheet = workbook.sheet_by_name(categorie)
    # gegevens = []
    # gebruik data uit Excel-bestand ecal
    nummer = str(sheet.cell_value(rowidx, 0))
    datering = str(sheet.cell_value(rowidx, 11))
    # jaartallen worden als 'float' geïnterpreteerd
    if datering[-2:] == ".0":
        datering = datering[:-2]
    huisnummer = str(sheet.cell_value(rowidx, 15))
    if huisnummer[-2:] == ".0":
        huisnummer = huisnummer[:-2]
    geg_dict[nummer] = {'beschrijving': str(sheet.cell_value(rowidx, 1)),
                        'voornaam': sheet.cell_value(rowidx, 2),
                        'tussenvoegsel': sheet.cell_value(rowidx, 3),
                        'achternaam': sheet.cell_value(rowidx, 4),
                        'patroniem': sheet.cell_value(rowidx, 5),
                        'geboorteplaats': sheet.cell_value(rowidx, 6),
                        'geboortedatum': sheet.cell_value(rowidx, 7),
                        'overlijdensplaats': sheet.cell_value(rowidx, 8),
                        'geslacht': sheet.cell_value(rowidx, 9),
                        'beroep': sheet.cell_value(rowidx, 10),
                        'datering': datering,
                        'gemeente': sheet.cell_value(rowidx, 12),
                        'plaats': sheet.cell_value(rowidx, 13),
                        'straatnaam': sheet.cell_value(rowidx, 14),
                        'huisnummer': huisnummer,
                        'toevoeging': sheet.cell_value(rowidx, 16),
                        'fotograaf': sheet.cell_value(rowidx, 17),
                        'copyright_': sheet.cell_value(rowidx, 18),
                        'notabene': sheet.cell_value(rowidx, 19),
                        'orig_vorm': sheet.cell_value(rowidx, 20),
                        'uiterl_vorm': sheet.cell_value(rowidx, 21),
                        'archief': sheet.cell_value(rowidx, 22),
                        'groep': sheet.cell_value(rowidx, 23),
                        'oude_nr': sheet.cell_value(rowidx, 24),
                        'code': sheet.cell_value(rowidx, 25),
                        # 'pad': sheet.cell_value(rowidx, 26)}
                        'pad': PAD_BESTANDEN + "afbeeldingen/" + nummer \
                            + ".jpg"
                        }
    data = ""
    for i in range(26):
        data = data + str(sheet.cell_value(rowidx, i)) + " "
    return data, nummer


def zoek_in_afbeeldingen(zoekw1, zoekw2):
    global foto_presentatie
    zoekresultaten = []
    foto_presentatie = []
    sheet = workbook.sheet_by_name("afbeeldingen")
    for rowidx in range(3, sheet.nrows):
        data, fotonr = verzamel_gegevens("afbeeldingen", rowidx)
        # alleen zoeken naar trefwoord
        if zoekw1[0] == "#":
            data = geg_dict[fotonr]['groep']
            zoekwoord1 = " " + zoekw1[1:]
        else:
            zoekwoord1 = zoekw1
        if zoekwoord1.lower() in data.lower() \
                and zoekw2.lower() in data.lower():
            # nr, beschrijving, datum foto
            pad = geg_dict[fotonr]['pad']
            if os.path.isfile(pad):
                zoekresultaten.append(
                    ("12_" + str(rowidx) + ",").ljust(12)
                    + fotonr.ljust(20)
                    + geg_dict[fotonr]['beschrijving']
                    + "  " + geg_dict[fotonr]['datering'])
                # Als scan aanwezig is, voeg scan toe aan fotopresentatie
                foto_presentatie.append(fotonr)
            else:
                foutmelding(fotonr)
    return zoekresultaten


def zoek_in_documenten(zoekw1, zoekw2):
    zoekresultaten = []
    sheet = workbook.sheet_by_name("documenten")
    for rowidx in range(1, sheet.nrows):
        nr = str(sheet.cell_value(rowidx, 0)).strip()
        jaar = str(sheet.cell_value(rowidx, 1))  # ivm float
        beschrijving = sheet.cell_value(rowidx, 2)
        categorie = sheet.cell_value(rowidx, 3)
        verzameling = sheet.cell_value(rowidx, 4)
        if jaar[-2:] == ".0":
            jaar = jaar[:-2]
        data = ""
        for k in range(6):
            data += " " + str(sheet.cell_value(rowidx, k))
        #  ALS de zoekwoorden voorkomen,
        if zoekw1.lower() in data.lower() and zoekw2.lower() in data.lower():
            mapnaam = str(sheet.cell_value(rowidx, 0))[0:3]
            # EN als de pdf bestaat:
            # Return a possibly-empty list of path names that match pathname,
            # which must be a string containing a path specification.
            pad = glob.glob(os.path.join(PAD_BESTANDEN + "documenten/"
                                         + mapnaam + "*/" + nr + "*.pdf"))
            gevonden = 0
            # zoek in list naar item dat pad naar record bevat
            for i in pad:
                if os.path.isfile(i):
                    zoekresultaten.append(
                        ("4_" + str(rowidx) + ",").ljust(12) + nr.ljust(12)
                        + jaar.ljust(11) + beschrijving.ljust(130) + " cat: "
                        + categorie + " verz: " + verzameling)
                    gevonden = 1
            #  anders is het een NIET gescand document:
            if gevonden == 0:
                zoekresultaten.append(
                    (">_" + str(rowidx) + ",").ljust(12) + nr.ljust(12)
                    + jaar.ljust(11) + beschrijving.ljust(130))
    return zoekresultaten


def zoek_in_geboorteakten(zoekw1, zoekw2):
    zoekresultaten = []
    sheet = workbook.sheet_by_name("geboorteakten")
    for rowidx in range(1, sheet.nrows):
        nummer = sheet.cell_value(rowidx, 0)
        vader = sheet.cell_value(rowidx, 1)
        moeder = sheet.cell_value(rowidx, 2)
        code = sheet.cell_value(rowidx, 3)
        if zoekw2 == "vader" or zoekw2 == "moeder":
            zoekw1, zoekw2 = zoekw2, zoekw1
        if zoekw1 == "vader":
            data = nummer + " " + vader + " " + code
        elif zoekw1 == "moeder":
            data = nummer + " " + moeder + " " + code
        else:
            data = nummer + " " + vader + " " + moeder + " " + code
        data = data.lower()
        zoekw1 = zoekw1.lower()
        zoekw2 = zoekw2.lower()
        if (zoekw1 == "vader" or zoekw1 == "moeder") and zoekw2 in data:
            zoekresultaten.append(
                ("8_" + str(rowidx) + ",").ljust(12) + nummer[8:].ljust(8)
                + vader.ljust(30) + moeder)
        elif zoekw1 in data and zoekw2 in data:
            zoekresultaten.append(
                ("8_" + str(rowidx) + ",").ljust(12) + nummer[8:].ljust(8)
                + vader.ljust(30) + moeder)
    return zoekresultaten


def zoek_in_trouwakten(zoekw1, zoekw2):
    zoekresultaten = []
    sheet = workbook.sheet_by_name("trouwakten")
    for rowidx in range(1, sheet.nrows):
        nummer = sheet.cell_value(rowidx, 0)
        aktenr = str(sheet.cell_value(rowidx, 1))[:-2]  # eindigt op .0
        bruidegom = sheet.cell_value(rowidx, 2)
        bruid = sheet.cell_value(rowidx, 3)
        code = sheet.cell_value(rowidx, 4)
        if zoekw2 == "bruid" or zoekw2 == "bruidegom":
            zoekw1, zoekw2 = zoekw2, zoekw1
        if zoekw1 == "bruidegom":
            data = nummer + " " + bruidegom + " " + code
        elif zoekw1 == "bruid":
            data = nummer + " " + bruid + " " + code
        else:
            data = nummer + " " + aktenr + " " + bruidegom + " " \
                   + bruid + " " + code
        data = data.lower()
        zoekw1 = zoekw1.lower()
        zoekw2 = zoekw2.lower()
        if (zoekw1 == "bruidegom" or zoekw1 == "bruid") and zoekw2 in data:
            zoekresultaten.append(
                ("9_" + str(rowidx) + ",").ljust(12) + aktenr.ljust(8)
                + bruidegom.ljust(30) + bruid)
        elif zoekw1 in data and zoekw2 in data:
            zoekresultaten.append(
                ("9_" + str(rowidx) + ",").ljust(12) + aktenr.ljust(8)
                + bruidegom.ljust(30) + bruid)
    return zoekresultaten


def zoek_data(zoekw1, zoekw2):
    """Zoekfunctie
    Zoek in de database in elke categorie naar regels met de
    zoekwoorden en stuur de zoekresultaten als list van te printen
    regels naar de funtie print_regels.
    """
    print_kop(zoekw1, zoekw2)
    # Demonstratie van het programma thuis met "demo-database"
    print_regels("Foto's", zoek_in_afbeeldingen(zoekw1, zoekw2))
    print_regels("Documenten", zoek_in_documenten(zoekw1, zoekw2))
    print_regels(
        "Geboorte-".ljust(11) + "aktenr" + "  vader      ".ljust(30)
        + "  moeder       ", zoek_in_geboorteakten(zoekw1, zoekw2))
    print_regels(
        ("Trouw-".ljust(11) + "aktenr" + "  bruidegom    ".ljust(30)
         + "  bruid         "), zoek_in_trouwakten(zoekw1, zoekw2))
    overzicht.insert('end', " ")
    overzicht.insert('end', " Einde overzicht")
    overzicht.insert('end', " ")
    for i in range(10):
        overzicht.insert('end', " ")  # veiligheidsmarge + 10


# functies die ervoor zorgen dat scans worden getoond

def toon_scan(scan, pad):
    """Start programma om foto of pdf te tonen """
    if os.path.isfile(pad):
        # Als de scan aanwezig is, toon scan
        if scan == "foto":
            # diavoorstelling(scan_nr, foto_presentatie) in 'toon_foto'
            pass
        elif scan == "pdf":
            # document, Old Nee in standaard pdf-reader
            os.startfile("%s" % pad)
        elif scan == "tekst":
            # prive archief
            os.startfile("%s" % pad)
        else:
            # krant, geboorteakte, trouwakte, kadaster in fotoviewer
            os.startfile("%s" % pad)
    else:
        messagebox.showwarning("Foto/document tonen", "Geen scan aanwezig")


def bepaal_rijnr(index_overzicht):
    # rijnummer staat achter de underscore
    undersc = index_overzicht.find("_")
    return int(index_overzicht[undersc + 1:])


def lees_gegevens(index_overzicht):
    # index_overzicht: 3_339
    # voor underscore: bladnr van Excelbestand
    # achter underscore: Excel-rijnummer = rijnummer in overicht + 1!
    if index_overzicht[0:2] == "12":
        sheet = workbook.sheet_by_name("afbeeldingen")
        rijnr = bepaal_rijnr(index_overzicht)
        # Bepaal het bestandsnummer van de foto
        scan_nr = sheet.cell_value(rijnr, 0)  #
    return scan_nr


def toon_foto(index_overzicht):
    scan_nr = lees_gegevens(index_overzicht)
    # scan_nr = naam/nummer van de foto
    index_diav = fotopresentatie(scan_nr, foto_presentatie, geg_dict)
    regelnummer = index_diav + 5
    # scroll het overzicht zodat gewijzigde regel zichtbaar wordt + 10 regels
    overzicht.see(regelnummer + 10)
    # selecteer de gewijzigde regel
    overzicht.activate(regelnummer)


def toon_document(index_overzicht):
    sheet = workbook.sheet_by_name("documenten")
    rijnr = bepaal_rijnr(index_overzicht)
    # Bepaal het bestandsnummer van de pdf
    scan_nr = sheet.cell_value(rijnr, 0)  # 073-06_03
    mapnaam = scan_nr[:3]
    """
    De mapnaam van een document kan uit een nummer bestaan (073),
    maar ook uit een nummer + een beschrijving (073 textiel).
    In de zoekregel op het scherm staat alleen het mapnummer.
    Datzelfde geldt voor de pdf's. Ook die hebben alleen een nummer
    (073-06_03) of een nummer met daarachter een korte beschrijving
    (022-03_01 Artikelcodes).
    Dankzij de glob.glob routine wordt nu toch het volledige pad
    gevonden.
    """
    # Return a possibly-empty list of path names that match pathname,
    # which must be a string containing a path specification.
    pad = glob.glob(os.path.join(PAD_BESTANDEN + "documenten/" + mapnaam
                                 + "*/" + scan_nr + "*.pdf"))
    if os.path.isfile(pad[0]):
        toon_scan("pdf", pad[0])


def toon_krant(index_overzicht):
    sheet = workbook.sheet_by_name("kranten")
    rijnr = bepaal_rijnr(index_overzicht)
    # pdf's: 1980_362, 1980_370, 1982-2_257, 1988-2_830
    scan_nr = sheet.cell_value(rijnr, 0)  # 1925-1970_012a
    underscore = scan_nr.find("_")
    pad = PAD_BESTANDEN + "kranten/" + scan_nr[0:underscore] + "/" \
        + scan_nr + ".jpg"
    if os.path.isfile(pad):
        toon_scan("krant", pad)
    else:
        pad = PAD_BESTANDEN + "kranten/" + scan_nr[0:underscore] + "/" \
              + scan_nr + ".pdf"
        toon_scan("pdf", pad)


def toon_geboorteakte(index_overzicht):
    sheet = workbook.sheet_by_name("geboorteakten")
    rijnr = bepaal_rijnr(index_overzicht)
    scan_nr = sheet.cell_value(rijnr, 0)  # 1811_22-044
    mapnaam = scan_nr[0:4]
    pad = PAD_BESTANDEN + "geboorteakten/" + mapnaam + "/" + scan_nr[:-4] \
        + ".jpg"
    toon_scan("akte", pad)


def toon_trouwakte(index_overzicht):
    sheet = workbook.sheet_by_name("trouwakten")
    rijnr = bepaal_rijnr(index_overzicht)
    scan_nr = sheet.cell_value(rijnr, 0)  # H1811_17
    mapnaam = scan_nr[0:5]
    pad = PAD_BESTANDEN + "trouwakten/" + mapnaam + "/" + scan_nr + ".jpg"
    toon_scan("akte", pad)


def toon_oldnee(index_overzicht):
    undersc = index_overzicht.find("_")
    scan_nr = index_overzicht[undersc + 1:]
    pad = PAD_BESTANDEN + "oldnee/" + scan_nr + ".pdf"
    toon_scan("pdf", pad)


def toon_kadaster(index_overzicht):
    sheet = workbook.sheet_by_name("kadaster")
    rijnr = bepaal_rijnr(index_overzicht)
    scan_nr = sheet.cell_value(rijnr, 1)
    pad = PAD_BESTANDEN + "/kadaster/boek/" + scan_nr + ".jpg"
    # toon de bladzijde uit het boek
    toon_scan("jpg", pad)
    scan_nr = sheet.cell_value(rijnr, 2)
    # toon de kaart
    pad = PAD_BESTANDEN + "/kadaster/kaarten/" + scan_nr + ".jpg"
    toon_scan("jpg", pad)


def foto_of_pdf_tonen(event):
    """Toon foto of pdf na dubbelklikken op resultaatregel op scherm """
    index = overzicht.curselection()
    gezochte_regel = overzicht.get(index[0], index[0])
    # gezochte_regel (zoekresultaat op scherm) is bijv:
    # '6_241,  1962-04-04  Twee koninklijke onderscheidingen - Personen'
    # categorie: 6 (krantenartikel), regel in Excelblad: 241
    komma = gezochte_regel[0].find(",")
    index_overzicht = gezochte_regel[0][0:komma]  # categoriecode + rijnr
    undersc = index_overzicht.find("_")
    categorie_code = gezochte_regel[0][0:undersc]

    # document
    if categorie_code == "4":
        toon_document(index_overzicht)
    # krantenartikel
    elif categorie_code == "6":
        toon_krant(index_overzicht)
    # geboorteakte
    elif categorie_code == "8":
        toon_geboorteakte(index_overzicht)
    # trouwakte
    elif categorie_code == "9":
        toon_trouwakte(index_overzicht)
    # OLD NEE
    elif categorie_code == "10":
        toon_oldnee(index_overzicht)
    # kadaster
    elif categorie_code == "11":
        toon_kadaster(index_overzicht)
    # afbeeldingen
    elif categorie_code == "12":
        toon_foto(index_overzicht)
    # witregel of -
    elif gezochte_regel[0][0] == " ":
        pass
    else:
        messagebox.showwarning("Foto/Pdf tonen", "Geen scan aanwezig")


# controle-functie -----------------------------------------------------

def foutmelding(nummer):
    """Fotonummers van foto's die wel in het Excel bestand staan,
    maar die niet in de fotomap staan, worden genoteerd in
    opmerkingen.txt.
    """
    with open(PAD_BESTANDEN + "opmerkingen.txt", "a") as myfile:
        myfile.write("FOUTMELDING: " + nummer
                     + ".jpg staat niet in de map.\n\n")


# overige functies -----------------------------------------------------

def lees_versienummer():
    """Wanneer is het Excelbestand voor het laatst gewijzigd?"""
    sheet = workbook.sheet_by_name("versie")
    versie = str(sheet.cell_value(0, 0))  # bevat datum laatste wijziging
    return versie


def info_programma_weergeven():
    """Zeer korte handleiding """
    overzicht_wissen()
    try:
        handleiding = open(PAD_BESTANDEN + "handleiding.txt", "r")
        for regel in handleiding:
            overzicht.insert('end', regel[:-1])
        handleiding.close()
    except FileNotFoundError:
        messagebox.showwarning("Zoeken", "Kan handleiding niet vinden")


def overzicht_openen():
    """Open opgeslagen overzicht of bestand met opmerkingen """
    overzicht_wissen()
    # selecteer het tekst-bestand
    pad = filedialog.askopenfilename(initialdir=PAD_BESTANDEN,
                                     title="Selecteer tekstbestand",
                                     filetypes=(("txt", "*.txt"),
                                                ("alle bestanden",
                                                 "*.*")))
    os.startfile("%s" % pad)


def overzicht_opslaan():
    """Sla zoekresultaten in overzicht op als tekstdocument """
    list_gevonden_documenten = overzicht.get(0, 'end')
    if list_gevonden_documenten:
        name = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text files", ".txt"),
                                                ("Word files", ".doc")],
            initialdir=PAD_BESTANDEN, title="Opslaan als")
        list_gevonden_documenten = overzicht.get(0, 'end')
        with open(name, "w") as data:
            for j in list_gevonden_documenten:
                data.write(j + '\n')
    else:
        messagebox.showwarning("Overzicht opslaan",
                               "Er zijn geen zoekresultaten.")


def programma_afsluiten():
    sys.exit()


def opmerkingen_lezen():
    """Tijdens de fotopresentatie kunnen opmerkingen over de foto
    worden toegevoegd. Deze worden opgeslagen in opmerkingen.txt,
    evenals foutmeldingen.
    """
    pad = PAD_BESTANDEN + "opmerkingen.txt"
    if os.path.exists(pad):
        os.startfile("%s" % pad)
    else:
        messagebox.showwarning("Opmerkingen",
                               "Er zijn nog geen opmerkingen opgeslagen.")


# schijfletter lezen en pad bepalen ------------------------------------

PAD_BESTANDEN = os.getcwd() + "/"
print(PAD_BESTANDEN)

try:
    print("")
    print("De database wordt geladen. Even geduld a.u.b.")
    # Lees data uit de database
    workbook = xlrd.open_workbook(PAD_BESTANDEN + 'zoekenDemo.xlsx')
except FileNotFoundError:
    messagebox.showwarning("Zoeken", "Excelbestand niet gevonden in "
                           + PAD_BESTANDEN)

# bouw GUI -------------------------------------------------------------

master = Tk()
master.geometry('1280x700+0+0')

# menubalk
menubar = Menu(master, relief='flat')

beheer_menu = Menu(menubar, tearoff=0)
beheer_menu.add_command(label="Afsluiten", command=programma_afsluiten)
menubar.add_cascade(label="Beheer", menu=beheer_menu)

overzicht_menu = Menu(menubar, tearoff=0)
overzicht_menu.add_command(label="Overzicht_openen",
                           command=overzicht_openen)
overzicht_menu.add_command(label="Opslaan als...",
                           command=overzicht_opslaan)
overzicht_menu.add_command(label="Wissen", command=overzicht_wissen)
menubar.add_cascade(label="Overzicht", menu=overzicht_menu)

menubar.add_command(label="Opmerkingen", command=opmerkingen_lezen)

menubar.add_command(label="Help", command=info_programma_weergeven)

master.config(menu=menubar)

# zoekwoorden
hoogte = 8  # ruimte onder menubalk

label = Label(master, text="Zoekwoord(en):")
label.place(x=10, y=hoogte)

zoekwoord1_invoer = Entry(master, width=21, bg="white")
zoekwoord1_invoer.bind('<Return>', zoeken_enter)
zoekwoord1_invoer.place(x=130, y=hoogte)
zoekwoord1_invoer.focus()

zoekwoord2_invoer = Entry(master, width=21, bg="white")
zoekwoord2_invoer.bind('<Return>', zoeken_enter)
zoekwoord2_invoer.place(x=310, y=hoogte)
zoekwoord2_invoer.focus()

knop_zoeken = Button(master, text="Zoeken", width=10, command=zoeken)
knop_zoeken.place(x=500, y=hoogte - 2)

knop_zoekwoord_wissen = Button(master, text="Wissen", width=10,
                               command=zoekwoord_wissen)
knop_zoekwoord_wissen.place(x=620, y=hoogte - 2)

# frame overzicht
overzicht_frame = LabelFrame(master, text="Overzicht",
                             width=1250, height=480)
overzicht_frame.place(x=10, y=40)

# listbox schuifbalken
yscrollbar = Scrollbar(overzicht_frame)
yscrollbar.pack(side='right', fill='y')

xscrollbar = Scrollbar(overzicht_frame, orient='horizontal')
xscrollbar.pack(side='bottom', fill='x')

# overzicht voor resultaten van de zoekopdracht en controles
overzicht = Listbox(overzicht_frame, font=("Courier", 12),
                    width=124, height=29, bg="white",
                    yscrollcommand=yscrollbar.set,
                    xscrollcommand=xscrollbar.set)
overzicht.place(x=210, y=12)
overzicht.pack(side='left', fill='both')
overzicht.bind('<Double-Button-1>', foto_of_pdf_tonen)

yscrollbar.config(command=overzicht.yview)
xscrollbar.config(command=overzicht.xview)

VERSIE_NUMMER = lees_versienummer()
master.title("HKN - zoeken in archief - versie {0}  -  database: {1} "
             .format(VERSIE, VERSIE_NUMMER))

# GUI voltooid ----------------------------------------------------------------

info_programma_weergeven()

master.mainloop()

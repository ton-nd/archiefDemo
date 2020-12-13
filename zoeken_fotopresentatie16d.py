#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
from tkinter import LabelFrame, Entry, messagebox, Canvas
from tkinter import Radiobutton, IntVar, Text, Frame, Toplevel
from tkinter import Label, Button, Scrollbar, Menu
from PIL import ImageTk, Image

global index_diavoorst
global richting

VERSIE = "fotopresentatie 16d"  # datum: 13-12-2020 17:42

# Bepaal het pad van de programma's en bestanden

PADNAAM = os.getcwd() + "/"


# ---------------------- Functies ---------------------------------------

def fotopresentatie(foto, gegevens, geg_dict):
    """ Toont foto in een fotovenster
        Nummers foto's staan in de lijst 'gegevens'
    """
    global index_diavoorst

    def wis_invoervelden():
        invoer_nummer.delete('0', 'end')
        # invoer_beschrijving
        invoer_voornaam.delete('0', 'end')
        invoer_tussenvoegsel.delete('0', 'end')
        invoer_achternaam.delete('0', 'end')
        invoer_patroniem.delete('0', 'end')
        invoer_geboorteplaats.delete('0', 'end')
        invoer_geboortedatum.delete('0', 'end')
        invoer_overlijdensplaats.delete('0', 'end')
        invoer_geslacht.delete('0', 'end')
        invoer_beroep.delete('0', 'end')
        invoer_datering.delete('0', 'end')
        invoer_gemeente.delete('0', 'end')
        invoer_plaats.delete('0', 'end')
        invoer_straatnaam.delete('0', 'end')
        invoer_huisnummer.delete('0', 'end')
        invoer_toevoeging.delete('0', 'end')
        invoer_fotograaf.delete('0', 'end')
        invoer_copyright.delete('0', 'end')
        var.set(2)  # orig_vorm: standaard digitaal
        invoer_vorm.delete('0', 'end')
        invoer_archief.delete('0', 'end')
        invoer_groep.delete('0', 'end')
        invoer_oude_nr.delete('0', 'end')
        invoer_code.delete('0', 'end')

    def toon_gegevens_foto(fotonr):
        wis_invoervelden()
        invoer_nummer.insert('0', fotonr)
        invoer_voornaam.insert('0', geg_dict[fotonr]['voornaam'])
        invoer_tussenvoegsel.insert('0', geg_dict[fotonr]['tussenvoegsel'])
        invoer_achternaam.insert('0', geg_dict[fotonr]['achternaam'])
        invoer_patroniem.insert('0', geg_dict[fotonr]['patroniem'])
        invoer_geboorteplaats.insert('0', geg_dict[fotonr]['geboorteplaats'])
        invoer_geboortedatum.insert('0', geg_dict[fotonr]['geboortedatum'])
        invoer_overlijdensplaats.insert('0', geg_dict[fotonr]
                                        ['overlijdensplaats'])
        invoer_geslacht.insert('0', geg_dict[fotonr]['geslacht'])
        invoer_beroep.insert('0', geg_dict[fotonr]['beroep'])
        datering = str(geg_dict[fotonr]['datering'])
        # Jaartallen worden als 'float' geïnterpreteerd
        if datering[-2:] == ".0":
            datering = datering[:-2]  # Verwijder '.0' achter datum
        invoer_datering.insert('0', datering)
        invoer_gemeente.insert('0', geg_dict[fotonr]['gemeente'])
        invoer_plaats.insert('0', geg_dict[fotonr]['plaats'])
        invoer_straatnaam.insert('0', geg_dict[fotonr]['straatnaam'])
        invoer_huisnummer.insert('0', geg_dict[fotonr]['huisnummer'])
        invoer_toevoeging.insert('0', geg_dict[fotonr]['toevoeging'])
        invoer_fotograaf.insert('0', geg_dict[fotonr]['fotograaf'])
        invoer_copyright.insert('0', geg_dict[fotonr]['copyright_'])
        if (geg_dict[fotonr]['orig_vorm']) == "analoog":
            orig_vorm_a.select()
        elif (geg_dict[fotonr]['orig_vorm']) == "digitaal":
            orig_vorm_d.select()
        # invoer_vorm.insert('0', geg_dict[fotonr]['orig_vorm'])
        invoer_archief.insert('0', geg_dict[fotonr]['archief'])
        invoer_groep.insert('0', geg_dict[fotonr]['groep'])
        invoer_oude_nr.insert('0', geg_dict[fotonr]['oude_nr'])
        invoer_code.insert('0', geg_dict[fotonr]['code'])
        # Plaats bijschriften
        invoer_beschrijving.delete('1.0', 'end')
        invoer_beschrijving.insert('insert', geg_dict[fotonr]['beschrijving'])
        invoer_notabene.delete('1.0', 'end')
        invoer_notabene.insert('insert', geg_dict[fotonr]['notabene'])

    def open_in_fotoprogramma():
        os.startfile("%s" % pad)

    def opmerkingen():
        if os.path.exists(PADNAAM + "opmerkingen.txt"):
            os.startfile("%s" % PADNAAM + "opmerkingen.txt")
        else:
            messagebox.showwarning("Opmerkingen",
                                   "Er zijn nog geen opmerkingen opgeslagen.")

    # Functies knoppen fotopresentatie

    def foto_volgende():
        global index_diavoorst
        global richting
        richting = "vooruit"
        index_diavoorst += 1
        foto_venster.quit()

    def foto_vorige():
        global index_diavoorst
        global richting
        richting = "terug"
        index_diavoorst -= 1
        foto_venster.quit()

    def foto_stoppen():
        global richting
        richting = "stoppen"
        foto_venster.quit()

    def sel_orig_vorm():
        pass

    # Plaats fotovenster, frame en fotocanvas

    foto_venster = Toplevel()
    foto_venster.title(VERSIE)
    foto_venster.geometry("1280x675+0+0")

    foto_frame = Frame(foto_venster, bd=0, relief='flat')
    foto_frame.place(x=3, y=0)  # x=10
    xscrollbar2 = Scrollbar(foto_frame, orient='horizontal')
    xscrollbar2.pack(side='bottom', fill='x')
    yscrollbar2 = Scrollbar(foto_frame, orient='vertical')
    yscrollbar2.pack(side='right', fill='y')

    br_invoer = 30  # breedte invoervelden subject

    subject_frame = LabelFrame(foto_venster, bd=1, text='subject',
                               relief='ridge', width=818, height=150)
    subject_frame.place(x=10, y=530)

    label_voornaam = Label(subject_frame)
    label_voornaam["text"] = "voornaam:"
    label_voornaam.place(x=10, y=10)

    invoer_voornaam = Entry(subject_frame, width=br_invoer, bg="white",
                            relief='flat')
    invoer_voornaam.place(x=10, y=35)

    label_tussenvoegsel = Label(subject_frame)
    label_tussenvoegsel["text"] = "tussenvoegsel:"
    label_tussenvoegsel.place(x=200, y=10)

    invoer_tussenvoegsel = Entry(subject_frame, width=8, bg="white",
                                 relief='flat')
    invoer_tussenvoegsel.place(x=200, y=35)

    label_achternaam = Label(subject_frame)
    label_achternaam["text"] = "achternaam:"
    label_achternaam.place(x=310, y=10)

    invoer_achternaam = Entry(subject_frame, width=br_invoer,
                              bg="white", relief='flat')
    invoer_achternaam.place(x=310, y=35)

    label_patroniem = Label(subject_frame)
    label_patroniem["text"] = "patroniem:"
    label_patroniem.place(x=510, y=10)

    invoer_patroniem = Entry(subject_frame, width=br_invoer, bg="white",
                             relief='flat')
    invoer_patroniem.place(x=510, y=35)

    y2 = 65
    y4 = 93
    label_geboorteplaats = Label(subject_frame)
    label_geboorteplaats["text"] = "geboorteplaats:"
    label_geboorteplaats.place(x=10, y=y2)

    invoer_geboorteplaats = Entry(subject_frame, width=br_invoer,
                                  bg="white", relief='flat')
    invoer_geboorteplaats.place(x=10, y=y4)

    label_geboortedatum = Label(subject_frame)
    label_geboortedatum["text"] = "geb.datum:"
    label_geboortedatum.place(x=200, y=y2)

    invoer_geboortedatum = Entry(subject_frame, width=12, bg="white",
                                 relief='flat')
    invoer_geboortedatum.place(x=200, y=y4)

    label_overlijdensplaats = Label(subject_frame)
    label_overlijdensplaats["text"] = "overlijdensplaats:"
    label_overlijdensplaats.place(x=310, y=y2)

    invoer_overlijdensplaats = Entry(subject_frame, width=br_invoer,
                                     bg="white", relief='flat')
    invoer_overlijdensplaats.place(x=310, y=y4)

    label_beroep = Label(subject_frame)
    label_beroep["text"] = "beroep:"
    label_beroep.place(x=510, y=y2)

    invoer_beroep = Entry(subject_frame, width=br_invoer, bg="white",
                          relief='flat')
    invoer_beroep.place(x=510, y=y4)

    label_geslacht = Label(subject_frame)
    label_geslacht["text"] = "M/V:"
    label_geslacht.place(x=700, y=y2)

    invoer_geslacht = Entry(subject_frame, width=2, bg="white",
                            relief='flat')
    invoer_geslacht.place(x=707, y=y4)

    # invoervelden aan de rechterzijde van het scherm

    # Plaats labels, invoervelden en knop
    x_fotobz = 840  # linkerkantlijn van labels
    y_fotobz = 0  # y-positie van begin invoervelden
    x_invoer = x_fotobz + 80  # linkerkantlijn van invoervelden
    tussenruimte_y = 27  # aantal pixels witregel tussen invoervelden

    breedte_invoer_foto_info = 58  # breedte invoervelden rechterzijde

    label_nummer = Label(foto_venster)
    label_nummer["text"] = "nummer:"
    label_nummer.place(x=x_fotobz, y=y_fotobz)

    invoer_nummer = Entry(foto_venster, width=30, bg="white",
                          relief='flat')  # bg=defaultbg
    invoer_nummer.place(x=x_invoer, y=y_fotobz)

    y_fotobz += tussenruimte_y
    label_beschrijving = Label(foto_venster)
    label_beschrijving["text"] = "beschrijving:"
    label_beschrijving.place(x=x_fotobz, y=y_fotobz)

    y_fotobz += tussenruimte_y - 5
    invoer_beschrijving = Text(foto_venster, width=53, height=3, bd=0,
                               bg="white", relief='sunken', wrap='word',
                               padx=4, pady=5)
    invoer_beschrijving.place(x=x_fotobz, y=y_fotobz)

    y_fotobz += 60
    label_notabene = Label(foto_venster)
    label_notabene["text"] = "notabene:"
    label_notabene.place(x=x_fotobz, y=y_fotobz)

    y_fotobz += tussenruimte_y
    invoer_notabene = Text(foto_venster, width=53, height=6, bd=0,
                           bg="white", relief='sunken', wrap='word', padx=5,
                           pady=5)
    invoer_notabene.place(x=x_fotobz, y=y_fotobz)

    y_fotobz += 125
    label_datering = Label(foto_venster)
    label_datering["text"] = "datering:"
    label_datering.place(x=x_fotobz, y=y_fotobz)

    invoer_datering = Entry(foto_venster,
                            width=breedte_invoer_foto_info, bg="white",
                            relief='flat')
    invoer_datering.place(x=x_invoer, y=y_fotobz - 1)

    y_fotobz += tussenruimte_y
    label_gemeente = Label(foto_venster)
    label_gemeente["text"] = "gemeente:"
    label_gemeente.place(x=x_fotobz, y=y_fotobz)

    invoer_gemeente = Entry(foto_venster,
                            width=breedte_invoer_foto_info, bg="white",
                            relief='flat')
    invoer_gemeente.place(x=x_invoer, y=y_fotobz - 1)

    y_fotobz += tussenruimte_y
    label_plaats = Label(foto_venster)
    label_plaats["text"] = "plaats:"
    label_plaats.place(x=x_fotobz, y=y_fotobz)

    invoer_plaats = Entry(foto_venster, width=breedte_invoer_foto_info,
                          bg="white", relief='flat')
    invoer_plaats.place(x=x_invoer, y=y_fotobz - 2)

    y_fotobz += tussenruimte_y
    label_straatnaam = Label(foto_venster)
    label_straatnaam["text"] = "straatnaam:"
    label_straatnaam.place(x=x_fotobz, y=y_fotobz)

    invoer_straatnaam = Entry(foto_venster,
                              width=breedte_invoer_foto_info, bg="white",
                              relief='flat')
    invoer_straatnaam.place(x=x_invoer, y=y_fotobz - 2)

    y_fotobz += tussenruimte_y
    label_huisnummer = Label(foto_venster)
    label_huisnummer["text"] = "huisnr:"
    label_huisnummer.place(x=x_fotobz, y=y_fotobz)

    invoer_huisnummer = Entry(foto_venster, width=10, bg="white",
                              relief='flat')
    invoer_huisnummer.place(x=x_invoer, y=y_fotobz - 2)

    label_toevoeging = Label(foto_venster)
    label_toevoeging["text"] = "toevoeging:"
    label_toevoeging.place(x=x_fotobz + 200, y=y_fotobz)

    invoer_toevoeging = Entry(foto_venster, width=5, bg="white",
                              relief='flat')
    invoer_toevoeging.place(x=x_invoer + 220, y=y_fotobz - 2)

    y_fotobz += tussenruimte_y
    label_fotograaf = Label(foto_venster)
    label_fotograaf["text"] = "fotograaf:"
    label_fotograaf.place(x=x_fotobz, y=y_fotobz)

    invoer_fotograaf = Entry(foto_venster,
                             width=breedte_invoer_foto_info, bg="white",
                             relief='flat')
    invoer_fotograaf.place(x=x_invoer, y=y_fotobz - 1)

    y_fotobz += tussenruimte_y
    label_copyright = Label(foto_venster)
    label_copyright["text"] = "copyright:"
    label_copyright.place(x=x_fotobz, y=y_fotobz)

    invoer_copyright = Entry(foto_venster,
                             width=breedte_invoer_foto_info, bg="white",
                             relief='flat')
    invoer_copyright.place(x=x_invoer, y=y_fotobz - 1)

    y_fotobz += tussenruimte_y
    label_orig_vorm = Label(foto_venster)
    label_orig_vorm["text"] = "orig. vorm:"
    label_orig_vorm.place(x=x_fotobz, y=y_fotobz)

    var = IntVar()
    orig_vorm_a = Radiobutton(foto_venster, text="analoog", variable=var,
                              value=1, command=sel_orig_vorm)
    orig_vorm_a.place(x=x_invoer, y=y_fotobz - 1)
    orig_vorm_d = Radiobutton(foto_venster, text="digitaal",
                              variable=var, value=2, command=sel_orig_vorm)
    orig_vorm_d.place(x=x_invoer + 100, y=y_fotobz - 1)

    y_fotobz += tussenruimte_y
    label_vorm = Label(foto_venster)
    label_vorm["text"] = "uiterl. vorm:"
    label_vorm.place(x=x_fotobz, y=y_fotobz)

    invoer_vorm = Entry(foto_venster, width=breedte_invoer_foto_info,
                        bg="white", relief='flat')
    invoer_vorm.place(x=x_invoer, y=y_fotobz - 1)

    y_fotobz += tussenruimte_y
    label_archief = Label(foto_venster)
    label_archief["text"] = "uit archief:"
    label_archief.place(x=x_fotobz, y=y_fotobz)

    invoer_archief = Entry(foto_venster, width=breedte_invoer_foto_info,
                           bg="white", relief='flat')
    invoer_archief.place(x=x_invoer, y=y_fotobz - 1)

    y_fotobz += tussenruimte_y
    label_groep = Label(foto_venster)
    label_groep["text"] = "groep:"
    label_groep.place(x=x_fotobz, y=y_fotobz)

    invoer_groep = Entry(foto_venster, width=breedte_invoer_foto_info,
                         bg="white", relief='flat')
    invoer_groep.place(x=x_invoer, y=y_fotobz - 1)

    y_fotobz += tussenruimte_y
    label_oude_nr = Label(foto_venster)
    label_oude_nr["text"] = "oude nr:"
    label_oude_nr.place(x=x_fotobz, y=y_fotobz)

    invoer_oude_nr = Entry(
        foto_venster, width=27, bg="white", relief='flat')
    invoer_oude_nr.place(x=x_invoer, y=y_fotobz - 1)

    label_code = Label(foto_venster)
    label_code["text"] = "code:"
    label_code.place(x=x_fotobz + 330, y=y_fotobz)

    invoer_code = Entry(
        foto_venster, width=7, bg="white", relief='flat')
    invoer_code.place(x=x_invoer + 296, y=y_fotobz - 1)

    y_fotobz += tussenruimte_y

    label_opmerkingen = Label(foto_venster)
    label_opmerkingen["text"] = "opmerkingen:"
    label_opmerkingen.place(x=x_fotobz, y=y_fotobz + 3)

    y_fotobz += tussenruimte_y + 5
    opmerking_text = Text(foto_venster, width=53, height=2, bd=0,
                          bg="white", relief='sunken', wrap='word', padx=5,
                          pady=5)
    opmerking_text.place(x=x_fotobz, y=y_fotobz)
    opmerking_text.delete('1.0', 'end')

    x_knoppen = 310
    y_knoppen = 523

    knop_volgende_foto = Button(
        foto_venster, width=6, text=">", command=foto_volgende)
    knop_volgende_foto.place(x=x_knoppen + 162, y=y_knoppen)
    knop_vorige_foto = Button(
        foto_venster, width=6, text="<", command=foto_vorige)
    knop_vorige_foto.place(x=x_knoppen, y=y_knoppen)
    knop_stoppen = Button(
        foto_venster, width=14, text="Overzicht",
        command=foto_stoppen)
    knop_stoppen.place(x=x_knoppen + 53, y=y_knoppen)

    # menubalk
    menubar = Menu(foto_venster, relief='flat')

    foto_menu = Menu(menubar, tearoff=0)
    foto_menu.add_command(
        label="Toon foto in foto-editor",
        command=open_in_fotoprogramma)
    # foto_menu.add_separator()
    menubar.add_cascade(label="Foto", menu=foto_menu)
    menubar.add_command(label="Opmerkingen", command=opmerkingen)
    foto_venster.config(menu=menubar)

    # -------------------------------------------------------------------------
    for i in range(len(gegevens)):  # i = volgnr diavoorstelling
        # zoek het indexnr van de geselecteerde foto in de diavoorstelling
        # break is nodig omdat bij gelijksoortige foto's (01a06616, 01a06616a)
        # de laatste foto wordt geselecteerd ipv de eerste
        # ----- de lijst gegevens moet straks alleen uit fotonummers bestaan
        if foto in gegevens[i]:
            index_diavoorst = i
            break

    # Start de diavoorstelling ------------------------------------------------
    old_label_image = None  # er staat nog geen foto in het canvas
    doorgaan = 1
    while doorgaan == 1:
        # Plaats het canvas waar foto straks in geplakt wordt
        canvas_image = Canvas(foto_frame, bd=0, width=810, height=500,
                              scrollregion=(0, 0, 5000, 3500),
                              xscrollcommand=xscrollbar2.set,
                              yscrollcommand=yscrollbar2.set)
        canvas_image.pack()
        xscrollbar2.config(command=canvas_image.xview)
        yscrollbar2.config(command=canvas_image.yview)
        # lees pad van foto
        pad = (geg_dict[gegevens[index_diavoorst]]['pad'])
        #  Plaats foto op canvas
        image1 = ImageTk.PhotoImage(Image.open(pad))
        canvas_image.create_image(5, 0, image=image1, anchor="nw")
        # Plaats de gegevens van de foto er rechts naast
        toon_gegevens_foto(gegevens[index_diavoorst])
        # Verwijder vorige foto (als die er staat)
        if old_label_image is not None:
            old_label_image.destroy()
        old_label_image = canvas_image

        foto_venster.mainloop()

        if richting == "vooruit":
            if index_diavoorst == len(gegevens):
                foto_venster.destroy()
                doorgaan = 0
        if richting == "terug":
            if index_diavoorst == -1:
                foto_venster.destroy()
                doorgaan = 0
        if richting == "stoppen":
            foto_venster.destroy()
            doorgaan = 0
    return index_diavoorst

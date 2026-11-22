#Importeren van Tkinter en Module.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Module as db

#Hoofdvenster aanmaken

root = tk.Tk()
root.title("Biker Haaglanden - Beheersysteem")
root.geometry("950x650")

#Tabs  aanmaken

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# De 4 tabbladen aanmaken

tab_klanten = tk.Frame(notebook)
tab_verhuur = tk.Frame(notebook)
tab_voorraad = tk.Frame(notebook)
tab_verkoop = tk.Frame(notebook)

notebook.add(tab_klanten, text="Klantenbestand")
notebook.add(tab_verhuur, text="Huurbestand")
notebook.add(tab_voorraad, text="Voorraadbestand")
notebook.add(tab_verkoop, text="Verkoop")

#dropdown en refresh bij tiepen

def maak_zoekbaar(combobox, volledige_lijst):
    """Filtert de dropdown-opties zodra je iets typt."""
    def filter_lijst(event):
        getypt = combobox.get().lower()
        if getypt == "":
            combobox["values"] = volledige_lijst
        else:
            gefilterd = []
            for item in volledige_lijst:
                if getypt in item.lower():
                    gefilterd.append(item)
            combobox["values"] = gefilterd

    combobox.bind("<KeyRelease>", filter_lijst)


def ververs_dropdowns():
    """Haalt de nieuwste klanten, fietsen en verhuren op voor alle dropdowns."""
    
    #Klanten lijst
    
    klanten_opties = []
    for k in db.haal_klanten_op():
        klanten_opties.append(f"{k.klant_id} - {k.naam}")

    combo_beheer_klant["values"] = klanten_opties
    maak_zoekbaar(combo_beheer_klant, klanten_opties)

    combo_huur_klant["values"] = klanten_opties
    maak_zoekbaar(combo_huur_klant, klanten_opties)

    combo_koop_klant["values"] = klanten_opties
    maak_zoekbaar(combo_koop_klant, klanten_opties)

    #Beschikbare fietsen lijst

    fietsen_opties = []
    for f in db.haal_voorraad_op():
        if f.status == "beschikbaar":
            fietsen_opties.append(f"{f.serial_code} - {f.soort}")

    combo_huur_serial["values"] = fietsen_opties
    maak_zoekbaar(combo_huur_serial, fietsen_opties)

    combo_koop_serial["values"] = fietsen_opties
    maak_zoekbaar(combo_koop_serial, fietsen_opties)

    #Actieve verhuren lijst

    verhuur_opties = []
    for v in db.haal_verhuur_op():
        if v.status == "actief":
            verhuur_opties.append(f"{v.huur_id} - Klant ID:{v.klant_id} ({v.serial_code})")

    combo_stop_huur["values"] = verhuur_opties
    maak_zoekbaar(combo_stop_huur, verhuur_opties)


def ververs_alles():
    toon_klanten()
    toon_verhuur()
    toon_voorraad()
    toon_verkoop_voorraad()
    ververs_dropdowns()

#Klantenbestand

frame_klant_nieuw = tk.LabelFrame(tab_klanten, text="Nieuwe klant aanmaken", padx=10, pady=10)
frame_klant_nieuw.pack(fill="x", padx=10, pady=5)

tk.Label(frame_klant_nieuw, text="Naam:").grid(row=0, column=0, sticky="w")
entry_klant_naam = tk.Entry(frame_klant_nieuw, width=25)
entry_klant_naam.grid(row=0, column=1, padx=5)

tk.Label(frame_klant_nieuw, text="Telefoon:").grid(row=0, column=2, sticky="w")
entry_klant_tel = tk.Entry(frame_klant_nieuw, width=20)
entry_klant_tel.grid(row=0, column=3, padx=5)

var_vaste_klant = tk.BooleanVar()
check_vaste_klant = tk.Checkbutton(frame_klant_nieuw, text="Vaste klant (10% korting)", variable=var_vaste_klant)
check_vaste_klant.grid(row=0, column=4, padx=5)

tk.Label(frame_klant_nieuw, text="Notities:").grid(row=1, column=0, sticky="w", pady=5)
entry_klant_notitie = tk.Entry(frame_klant_nieuw, width=60)
entry_klant_notitie.grid(row=1, column=1, columnspan=4, sticky="w", padx=5, pady=5)

def klik_klant_toevoegen():
    naam = entry_klant_naam.get()
    tel = entry_klant_tel.get()
    vast = var_vaste_klant.get()
    notitie = entry_klant_notitie.get()

    if naam == "" or tel == "":
        messagebox.showwarning("Fout", "Vul naam en telefoonnummer in.")
        return

    gelukt, bericht = db.voeg_klant_toe(naam, tel, vast, notitie)
    messagebox.showinfo("Info", bericht)

    entry_klant_naam.delete(0, tk.END)
    entry_klant_tel.delete(0, tk.END)
    entry_klant_notitie.delete(0, tk.END)
    var_vaste_klant.set(False)
    ververs_alles()

btn_klant_toevoegen = tk.Button(frame_klant_nieuw, text="Klant Opslaan", command=klik_klant_toevoegen)
btn_klant_toevoegen.grid(row=2, column=1, sticky="w", pady=5)

#Klant blokkeren/deblokkeren

frame_klant_beheer = tk.LabelFrame(tab_klanten, text="Klant blokkeren of notitie wijzigen", padx=10, pady=10)
frame_klant_beheer.pack(fill="x", padx=10, pady=5)

tk.Label(frame_klant_beheer, text="Klant ID:").grid(row=0, column=0, sticky="w")
combo_beheer_klant = ttk.Combobox(frame_klant_beheer, width=22)
combo_beheer_klant.grid(row=0, column=1, padx=5)

tk.Label(frame_klant_beheer, text="Reden / Nieuwe notitie:").grid(row=0, column=2, sticky="w")
entry_beheer_reden = tk.Entry(frame_klant_beheer, width=40)
entry_beheer_reden.grid(row=0, column=3, padx=5)

def klik_blokkeer():
    keuze = combo_beheer_klant.get()
    reden = entry_beheer_reden.get()
    if keuze == "":
        messagebox.showwarning("Fout", "Kies of typ een Klant ID.")
        return
    klant_id = keuze.split(" - ")[0]
    gelukt, bericht = db.wijzig_blokkade_klant(klant_id, True, reden)
    messagebox.showinfo("Info", bericht)
    ververs_alles()

def klik_deblokkeer():
    keuze = combo_beheer_klant.get()
    reden = entry_beheer_reden.get()
    if keuze == "":
        messagebox.showwarning("Fout", "Kies of typ een Klant ID.")
        return
    klant_id = keuze.split(" - ")[0]
    gelukt, bericht = db.wijzig_blokkade_klant(klant_id, False, reden)
    messagebox.showinfo("Info", bericht)
    ververs_alles()

btn_blokkeer = tk.Button(frame_klant_beheer, text="Blokkeer Klant", command=klik_blokkeer)
btn_blokkeer.grid(row=1, column=1, pady=5)

btn_deblokkeer = tk.Button(frame_klant_beheer, text="Deblokkeer Klant", command=klik_deblokkeer)
btn_deblokkeer.grid(row=1, column=2, pady=5)

#Tabel klanten

kolommen_klanten = ("id", "naam", "telefoon", "vaste_klant", "status", "notities")
tabel_klanten = ttk.Treeview(tab_klanten, columns=kolommen_klanten, show="headings", height=14)

tabel_klanten.heading("id", text="ID")
tabel_klanten.heading("naam", text="Naam")
tabel_klanten.heading("telefoon", text="Telefoon")
tabel_klanten.heading("vaste_klant", text="Vaste Klant")
tabel_klanten.heading("status", text="Status")
tabel_klanten.heading("notities", text="Notities")

tabel_klanten.column("id", width=40)
tabel_klanten.column("naam", width=150)
tabel_klanten.column("telefoon", width=110)
tabel_klanten.column("vaste_klant", width=100)
tabel_klanten.column("status", width=100)
tabel_klanten.column("notities", width=350)

tabel_klanten.pack(fill="both", expand=True, padx=10, pady=5)

def toon_klanten():
    for rij in tabel_klanten.get_children():
        tabel_klanten.delete(rij)

    klanten = db.haal_klanten_op()
    for k in klanten:
        vast_tekst = "Ja (10%)" if k.vaste_klant else "Nee"
        blok_tekst = "GEBLOKKEERD" if k.geblokkeerd else "Actief"
        tabel_klanten.insert("", tk.END, values=(k.klant_id, k.naam, k.telefoon, vast_tekst, blok_tekst, k.notities))

#Huurbestand

frame_huur_nieuw = tk.LabelFrame(tab_verhuur, text="Nieuwe verhuur aanmaken", padx=10, pady=10)
frame_huur_nieuw.pack(fill="x", padx=10, pady=5)

tk.Label(frame_huur_nieuw, text="Klant ID:").grid(row=0, column=0, sticky="w")
combo_huur_klant = ttk.Combobox(frame_huur_nieuw, width=22)
combo_huur_klant.grid(row=0, column=1, padx=5)

tk.Label(frame_huur_nieuw, text="Fiets Serial Code:").grid(row=0, column=2, sticky="w")
combo_huur_serial = ttk.Combobox(frame_huur_nieuw, width=24)
combo_huur_serial.grid(row=0, column=3, padx=5)

tk.Label(frame_huur_nieuw, text="Aantal dagen:").grid(row=0, column=4, sticky="w")
entry_huur_dagen = tk.Entry(frame_huur_nieuw, width=10)
entry_huur_dagen.grid(row=0, column=5, padx=5)

label_prijs_voorbeeld = tk.Label(frame_huur_nieuw, text="Prijsindicatie: -")
label_prijs_voorbeeld.grid(row=1, column=0, columnspan=6, sticky="w", pady=5)

def klik_bereken_prijs():
    k_keuze = combo_huur_klant.get()
    s_keuze = combo_huur_serial.get()
    dagen = entry_huur_dagen.get()

    if k_keuze == "" or s_keuze == "" or dagen == "":
        messagebox.showwarning("Fout", "Vul Klant ID, Serial Code en Dagen in.")
        return

    k_id = k_keuze.split(" - ")[0]
    serial = s_keuze.split(" - ")[0]

    info = db.bereken_huurprijs(serial, k_id, dagen)
    if info is None:
        label_prijs_voorbeeld.config(text="Klant of fiets niet gevonden!")
    else:
        tekst = f"Huur: €{info['basis_huur']} | Korting: -€{info['korting']} | Borg: €{info['borg']} | TOTAAL: €{info['totaal']}"
        label_prijs_voorbeeld.config(text=tekst)

def klik_verhuur_aanmaken():
    k_keuze = combo_huur_klant.get()
    s_keuze = combo_huur_serial.get()
    dagen = entry_huur_dagen.get()

    if k_keuze == "" or s_keuze == "" or dagen == "":
        messagebox.showwarning("Fout", "Vul alle velden in.")
        return

    k_id = k_keuze.split(" - ")[0]
    serial = s_keuze.split(" - ")[0]

    gelukt, bericht = db.maak_verhuur_aan(k_id, serial, dagen)
    messagebox.showinfo("Verhuur", bericht)
    combo_huur_serial.set("")
    ververs_alles()

btn_bereken = tk.Button(frame_huur_nieuw, text="Bereken Prijs", command=klik_bereken_prijs)
btn_bereken.grid(row=2, column=1, pady=5)

btn_verhuur = tk.Button(frame_huur_nieuw, text="Fiets Verhuren", command=klik_verhuur_aanmaken)
btn_verhuur.grid(row=2, column=3, pady=5)

#Verhuur annuleren/retour melden
frame_huur_stop = tk.LabelFrame(tab_verhuur, text="Verhuur annuleren of fiets retour melden", padx=10, pady=10)
frame_huur_stop.pack(fill="x", padx=10, pady=5)

tk.Label(frame_huur_stop, text="Huur ID:").grid(row=0, column=0, sticky="w")
combo_stop_huur = ttk.Combobox(frame_huur_stop, width=28)
combo_stop_huur.grid(row=0, column=1, padx=5)

def klik_annuleer_huur():
    keuze = combo_stop_huur.get()
    if keuze == "":
        return
    h_id = keuze.split(" - ")[0]
    gelukt, bericht = db.stop_verhuur(h_id, "geannuleerd")
    messagebox.showinfo("Info", bericht)
    combo_stop_huur.set("")
    ververs_alles()

def klik_retour_huur():
    keuze = combo_stop_huur.get()
    if keuze == "":
        return
    h_id = keuze.split(" - ")[0]
    gelukt, bericht = db.stop_verhuur(h_id, "retour")
    messagebox.showinfo("Info", bericht)
    combo_stop_huur.set("")
    ververs_alles()

btn_annuleer = tk.Button(frame_huur_stop, text="Annuleer Verhuur", command=klik_annuleer_huur)
btn_annuleer.grid(row=0, column=2, padx=5)

btn_retour = tk.Button(frame_huur_stop, text="Fiets Retour (Vrijgeven)", command=klik_retour_huur)
btn_retour.grid(row=0, column=3, padx=5)

# Tabel verhuur

kolommen_verhuur = ("huur_id", "klant", "fiets", "start", "eind", "borg", "totaal", "status")
tabel_verhuur = ttk.Treeview(tab_verhuur, columns=kolommen_verhuur, show="headings", height=14)

tabel_verhuur.heading("huur_id", text="Huur ID")
tabel_verhuur.heading("klant", text="Klant")
tabel_verhuur.heading("fiets", text="Fiets")
tabel_verhuur.heading("start", text="Startdatum")
tabel_verhuur.heading("eind", text="Einddatum")
tabel_verhuur.heading("borg", text="Borg")
tabel_verhuur.heading("totaal", text="Totaal")
tabel_verhuur.heading("status", text="Status")

tabel_verhuur.column("huur_id", width=60)
tabel_verhuur.column("klant", width=150)
tabel_verhuur.column("fiets", width=80)
tabel_verhuur.column("start", width=95)
tabel_verhuur.column("eind", width=95)
tabel_verhuur.column("borg", width=75)
tabel_verhuur.column("totaal", width=85)
tabel_verhuur.column("status", width=180)

tabel_verhuur.pack(fill="both", expand=True, padx=10, pady=5)

def toon_verhuur():
    for rij in tabel_verhuur.get_children():
        tabel_verhuur.delete(rij)

    verhuren = db.haal_verhuur_op()
    for v in verhuren:
        klant = db.zoek_klant(v.klant_id)
        klant_naam = f"{klant.naam} (ID:{v.klant_id})" if klant else f"ID:{v.klant_id}"

        status_tekst = v.status.upper()
        if v.is_verlopen() == True:
            status_tekst = status_tekst + " (VERLOPEN!)"

        tabel_verhuur.insert("", tk.END, values=(
            v.huur_id, klant_naam, v.serial_code, v.startdatum, v.einddatum, f"€{v.borg}", f"€{v.totaalprijs}", status_tekst
        ))

#Voorraad bestand

frame_voorraad_nieuw = tk.LabelFrame(tab_voorraad, text="Nieuwe fiets toevoegen aan voorraad", padx=10, pady=10)
frame_voorraad_nieuw.pack(fill="x", padx=10, pady=5)

tk.Label(frame_voorraad_nieuw, text="Serial Code:").grid(row=0, column=0, sticky="w")
entry_v_serial = tk.Entry(frame_voorraad_nieuw, width=12)
entry_v_serial.grid(row=0, column=1, padx=5)

tk.Label(frame_voorraad_nieuw, text="Soort fiets:").grid(row=0, column=2, sticky="w")
entry_v_soort = tk.Entry(frame_voorraad_nieuw, width=18)
entry_v_soort.grid(row=0, column=3, padx=5)

tk.Label(frame_voorraad_nieuw, text="Huurprijs/dag (€):").grid(row=1, column=0, sticky="w", pady=5)
entry_v_huur = tk.Entry(frame_voorraad_nieuw, width=12)
entry_v_huur.grid(row=1, column=1, padx=5)

tk.Label(frame_voorraad_nieuw, text="Koopprijs (€):").grid(row=1, column=2, sticky="w")
entry_v_koop = tk.Entry(frame_voorraad_nieuw, width=12)
entry_v_koop.grid(row=1, column=3, padx=5)

tk.Label(frame_voorraad_nieuw, text="Borg (€):").grid(row=1, column=4, sticky="w")
entry_v_borg = tk.Entry(frame_voorraad_nieuw, width=12)
entry_v_borg.grid(row=1, column=5, padx=5)

def klik_fiets_toevoegen():
    serial = entry_v_serial.get()
    soort = entry_v_soort.get()
    huur = entry_v_huur.get()
    koop = entry_v_koop.get()
    borg = entry_v_borg.get()

    if serial == "" or soort == "" or huur == "" or koop == "" or borg == "":
        messagebox.showwarning("Fout", "Vul alle velden in.")
        return

    gelukt, bericht = db.voeg_fiets_toe(serial, soort, huur, koop, borg)
    messagebox.showinfo("Voorraad", bericht)

    entry_v_serial.delete(0, tk.END)
    entry_v_soort.delete(0, tk.END)
    entry_v_huur.delete(0, tk.END)
    entry_v_koop.delete(0, tk.END)
    entry_v_borg.delete(0, tk.END)
    ververs_alles()

btn_fiets_toevoegen = tk.Button(frame_voorraad_nieuw, text="Fiets Toevoegen", command=klik_fiets_toevoegen)
btn_fiets_toevoegen.grid(row=2, column=1, pady=5)

#Tabel voorraad

kolommen_voorraad = ("serial", "soort", "huurprijs", "koopprijs", "borg", "status")
tabel_voorraad = ttk.Treeview(tab_voorraad, columns=kolommen_voorraad, show="headings", height=16)

tabel_voorraad.heading("serial", text="Serial Code")
tabel_voorraad.heading("soort", text="Soort Fiets")
tabel_voorraad.heading("huurprijs", text="Huur / dag")
tabel_voorraad.heading("koopprijs", text="Koopprijs")
tabel_voorraad.heading("borg", text="Borg")
tabel_voorraad.heading("status", text="Status")

tabel_voorraad.column("serial", width=110)
tabel_voorraad.column("soort", width=180)
tabel_voorraad.column("huurprijs", width=100)
tabel_voorraad.column("koopprijs", width=100)
tabel_voorraad.column("borg", width=90)
tabel_voorraad.column("status", width=140)

tabel_voorraad.pack(fill="both", expand=True, padx=10, pady=5)

def toon_voorraad():
    for rij in tabel_voorraad.get_children():
        tabel_voorraad.delete(rij)

    fietsen = db.haal_voorraad_op()
    for f in fietsen:
        tabel_voorraad.insert("", tk.END, values=(
            f.serial_code, f.soort, f"€{f.huurprijs}", f"€{f.koopprijs}", f"€{f.borg}", f.status.upper()
        ))

#Verkoop

frame_verkoop = tk.LabelFrame(tab_verkoop, text="Fiets verkopen aan klant", padx=10, pady=10)
frame_verkoop.pack(fill="x", padx=10, pady=5)

tk.Label(frame_verkoop, text="Klant ID:").grid(row=0, column=0, sticky="w")
combo_koop_klant = ttk.Combobox(frame_verkoop, width=22)
combo_koop_klant.grid(row=0, column=1, padx=5)

tk.Label(frame_verkoop, text="Fiets Serial Code:").grid(row=0, column=2, sticky="w")
combo_koop_serial = ttk.Combobox(frame_verkoop, width=24)
combo_koop_serial.grid(row=0, column=3, padx=5)

def klik_verkoop_fiets():
    k_keuze = combo_koop_klant.get()
    s_keuze = combo_koop_serial.get()

    if k_keuze == "" or s_keuze == "":
        messagebox.showwarning("Fout", "Vul Klant ID en Serial Code in.")
        return

    k_id = k_keuze.split(" - ")[0]
    serial = s_keuze.split(" - ")[0]

    gelukt, bericht = db.verkoop_fiets(k_id, serial)
    messagebox.showinfo("Verkoop", bericht)
    combo_koop_serial.set("")
    ververs_alles()

btn_verkoop = tk.Button(frame_verkoop, text="Verkoop Fiets", command=klik_verkoop_fiets)
btn_verkoop.grid(row=0, column=4, padx=10)

tk.Label(tab_verkoop, text="Beschikbare fietsen voor verkoop (komt direct uit voorraad):").pack(anchor="w", padx=10)

#Tabel verkoop

kolommen_verkoop = ("serial", "soort", "normale_prijs", "vaste_klant_prijs")
tabel_verkoop = ttk.Treeview(tab_verkoop, columns=kolommen_verkoop, show="headings", height=16)

tabel_verkoop.heading("serial", text="Serial Code")
tabel_verkoop.heading("soort", text="Soort Fiets")
tabel_verkoop.heading("normale_prijs", text="Normale Koopprijs")
tabel_verkoop.heading("vaste_klant_prijs", text="Prijs Vaste Klant (10% korting)")

tabel_verkoop.column("serial", width=120)
tabel_verkoop.column("soort", width=200)
tabel_verkoop.column("normale_prijs", width=160)
tabel_verkoop.column("vaste_klant_prijs", width=220)

tabel_verkoop.pack(fill="both", expand=True, padx=10, pady=5)

def toon_verkoop_voorraad():
    for rij in tabel_verkoop.get_children():
        tabel_verkoop.delete(rij)

    fietsen = db.haal_voorraad_op()
    for f in fietsen:
        if f.status == "beschikbaar":
            korting_prijs = round(f.koopprijs * 0.90, 2)
            tabel_verkoop.insert("", tk.END, values=(
                f.serial_code, f.soort, f"€{f.koopprijs}", f"€{korting_prijs}"
            ))

#Start app

ververs_alles()
root.mainloop()
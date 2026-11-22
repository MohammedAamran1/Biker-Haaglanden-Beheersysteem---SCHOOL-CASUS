#Importeren van JSON, Opperating System en Huidige tijd en datum

import json
import os
from datetime import datetime, timedelta

#De 3 JSON bestanden

VOORRAAD_FILE = "JSON/Voorraad.json"
KLANTEN_FILE = "JSON/Klanten.json"
VERHUUR_FILE = "JSON/Verhuur.json"

#classes voor Fiets, klant en verhuur

class Fiets:
    def __init__(self, serial_code, soort, huurprijs, koopprijs, borg, status="beschikbaar"):
        self.serial_code = serial_code
        self.soort = soort
        self.huurprijs = float(huurprijs)
        self.koopprijs = float(koopprijs)
        self.borg = float(borg)
        self.status = status

    def naar_dict(self):
        return {
            "serial_code": self.serial_code,
            "soort": self.soort,
            "huurprijs": self.huurprijs,
            "koopprijs": self.koopprijs,
            "borg": self.borg,
            "status": self.status
        }

class Klant:
    def __init__(self, klant_id, naam, telefoon, vaste_klant=False, geblokkeerd=False, notities=""):
        self.klant_id = int(klant_id)
        self.naam = naam
        self.telefoon = telefoon
        self.vaste_klant = bool(vaste_klant)
        self.geblokkeerd = bool(geblokkeerd)
        self.notities = notities

    def naar_dict(self):
        return {
            "klant_id": self.klant_id,
            "naam": self.naam,
            "telefoon": self.telefoon,
            "vaste_klant": self.vaste_klant,
            "geblokkeerd": self.geblokkeerd,
            "notities": self.notities
        }

class Verhuur:
    def __init__(self, huur_id, klant_id, serial_code, startdatum, einddatum, borg, totaalprijs, status="actief"):
        self.huur_id = int(huur_id)
        self.klant_id = int(klant_id)
        self.serial_code = serial_code
        self.startdatum = startdatum
        self.einddatum = einddatum
        self.borg = float(borg)
        self.totaalprijs = float(totaalprijs)
        self.status = status

    def is_verlopen(self):
        if self.status != "actief":
            return False
        vandaag = datetime.now().date()
        eind = datetime.strptime(self.einddatum, "%Y-%m-%d").date()
        if vandaag > eind:
            return True
        else:
            return False

    def naar_dict(self):
        return {
            "huur_id": self.huur_id,
            "klant_id": self.klant_id,
            "serial_code": self.serial_code,
            "startdatum": self.startdatum,
            "einddatum": self.einddatum,
            "borg": self.borg,
            "totaalprijs": self.totaalprijs,
            "status": self.status
        }

#Het wijzigen,lezen en aanmaken van JSON files voor voorraad, huur en klant bestanden.

def laad_json(bestandsnaam):
    if not os.path.exists(bestandsnaam):
        return []
    bestand = open(bestandsnaam, "r", encoding="utf-8")
    data = json.load(bestand)
    bestand.close()
    return data

def sla_json_op(bestandsnaam, lijst_met_dicts):
    bestand = open(bestandsnaam, "w", encoding="utf-8")
    json.dump(lijst_met_dicts, bestand, indent=4)
    bestand.close()

#Definitions voor Voorraad

def haal_voorraad_op():
    ruwe_data = laad_json(VOORRAAD_FILE)
    fietsen_lijst = []
    for item in ruwe_data:
        fiets = Fiets(
            item["serial_code"],
            item["soort"],
            item["huurprijs"],
            item["koopprijs"],
            item["borg"],
            item["status"]
        )
        fietsen_lijst.append(fiets)
    return fietsen_lijst

def sla_voorraad_op(fietsen_lijst):
    lijst_om_op_te_slaan = []
    for fiets in fietsen_lijst:
        lijst_om_op_te_slaan.append(fiets.naar_dict())
    sla_json_op(VOORRAAD_FILE, lijst_om_op_te_slaan)

def voeg_fiets_toe(serial_code, soort, huurprijs, koopprijs, borg):
    fietsen = haal_voorraad_op()
    for fiets in fietsen:
        if fiets.serial_code.lower() == serial_code.lower():
            return False, "Deze serial code bestaat al."
            
    nieuwe_fiets = Fiets(serial_code.upper(), soort, huurprijs, koopprijs, borg, "beschikbaar")
    fietsen.append(nieuwe_fiets)
    sla_voorraad_op(fietsen)
    return True, "Fiets toegevoegd aan voorraad!"

def zoek_fiets(serial_code):
    fietsen = haal_voorraad_op()
    for fiets in fietsen:
        if fiets.serial_code.lower() == serial_code.lower():
            return fiets
    return None

#Definitions voor klanten

def haal_klanten_op():
    ruwe_data = laad_json(KLANTEN_FILE)
    klanten_lijst = []
    for item in ruwe_data:
        klant = Klant(
            item["klant_id"],
            item["naam"],
            item["telefoon"],
            item["vaste_klant"],
            item["geblokkeerd"],
            item["notities"]
        )
        klanten_lijst.append(klant)
    return klanten_lijst


def sla_klanten_op(klanten_lijst):
    lijst_om_op_te_slaan = []
    for klant in klanten_lijst:
        lijst_om_op_te_slaan.append(klant.naar_dict())
    sla_json_op(KLANTEN_FILE, lijst_om_op_te_slaan)


def voeg_klant_toe(naam, telefoon, vaste_klant, notities):
    klanten = haal_klanten_op()
    
    # Hoogste ID zoeken met een gewone for-loop
    hoogste_id = 0
    for klant in klanten:
        if klant.klant_id > hoogste_id:
            hoogste_id = klant.klant_id
    nieuw_id = hoogste_id + 1

    nieuwe_klant = Klant(nieuw_id, naam, telefoon, vaste_klant, False, notities)
    klanten.append(nieuwe_klant)
    sla_klanten_op(klanten)
    return True, "Klant is aangemaakt!"


def zoek_klant(klant_id):
    klanten = haal_klanten_op()
    for klant in klanten:
        if klant.klant_id == int(klant_id):
            return klant
    return None


def wijzig_blokkade_klant(klant_id, blokkeer_status, reden=""):
    klanten = haal_klanten_op()
    for klant in klanten:
        if klant.klant_id == int(klant_id):
            klant.geblokkeerd = blokkeer_status
            if reden != "":
                klant.notities = klant.notities + " | " + reden
            sla_klanten_op(klanten)
            return True, "Blokkade status is aangepast."
    return False, "Klant niet gevonden."


def update_klant_gegevens(klant_id, nieuwe_notitie, vaste_klant):
    klanten = haal_klanten_op()
    for klant in klanten:
        if klant.klant_id == int(klant_id):
            klant.notities = nieuwe_notitie
            klant.vaste_klant = vaste_klant
            sla_klanten_op(klanten)
            return True, "Klantgegevens zijn opgeslagen."
    return False, "Klant niet gevonden."

#Definitions voor Verhuur

def haal_verhuur_op():
    ruwe_data = laad_json(VERHUUR_FILE)
    verhuur_lijst = []
    for item in ruwe_data:
        verhuur = Verhuur(
            item["huur_id"],
            item["klant_id"],
            item["serial_code"],
            item["startdatum"],
            item["einddatum"],
            item["borg"],
            item["totaalprijs"],
            item["status"]
        )
        verhuur_lijst.append(verhuur)
    return verhuur_lijst


def sla_verhuur_op(verhuur_lijst):
    lijst_om_op_te_slaan = []
    for verhuur in verhuur_lijst:
        lijst_om_op_te_slaan.append(verhuur.naar_dict())
    sla_json_op(VERHUUR_FILE, lijst_om_op_te_slaan)


def bereken_huurprijs(serial_code, klant_id, aantal_dagen):
    fiets = zoek_fiets(serial_code)
    klant = zoek_klant(klant_id)
    
    if fiets is None or klant is None:
        return None

    basis_huur = fiets.huurprijs * int(aantal_dagen)
    
    if klant.vaste_klant == True:
        korting = basis_huur * 0.10
    else:
        korting = 0.0

    huur_na_korting = basis_huur - korting
    totaal_prijs = huur_na_korting + fiets.borg

    return {
        "basis_huur": round(basis_huur, 2),
        "korting": round(korting, 2),
        "borg": round(fiets.borg, 2),
        "totaal": round(totaal_prijs, 2)
    }


def maak_verhuur_aan(klant_id, serial_code, aantal_dagen):
    klant = zoek_klant(klant_id)
    if klant is None:
        return False, "Klant bestaat niet."
    if klant.geblokkeerd == True:
        return False, "Deze klant is geblokkeerd en mag niet huren!"

    fietsen = haal_voorraad_op()
    gekozen_fiets = None
    for fiets in fietsen:
        if fiets.serial_code.lower() == serial_code.lower():
            gekozen_fiets = fiets

    if gekozen_fiets is None:
        return False, "Fiets niet gevonden."
    if gekozen_fiets.status != "beschikbaar":
        return False, "Deze fiets is niet beschikbaar."

    # Datums instellen
    start_datum = datetime.now().date()
    eind_datum = start_datum + timedelta(days=int(aantal_dagen))

    # Prijs berekenen
    prijs_info = bereken_huurprijs(gekozen_fiets.serial_code, klant.klant_id, aantal_dagen)

    # Nieuw verhuur ID maken
    verhuren = haal_verhuur_op()
    hoogste_id = 0
    for v in verhuren:
        if v.huur_id > hoogste_id:
            hoogste_id = v.huur_id
    nieuw_id = hoogste_id + 1

    nieuwe_verhuur = Verhuur(
        nieuw_id,
        klant.klant_id,
        gekozen_fiets.serial_code,
        str(start_datum),
        str(eind_datum),
        prijs_info["borg"],
        prijs_info["totaal"],
        "actief"
    )
    verhuren.append(nieuwe_verhuur)
    sla_verhuur_op(verhuren)

    #Fiets op 'verhuurd' zetten in de voorraad
    gekozen_fiets.status = "verhuurd"
    sla_voorraad_op(fietsen)

    return True, f"Verhuur #{nieuw_id} is aangemaakt! Totaal: €{prijs_info['totaal']}"

#Nieuwe status is bijvoorbeeld "geannuleerd" of "retour"

def stop_verhuur(huur_id, nieuwe_status):
    verhuren = haal_verhuur_op()
    fietsen = haal_voorraad_op()

    for v in verhuren:
        if v.huur_id == int(huur_id):
            if v.status != "actief":
                return False, "Deze verhuur is al gestopt."
            
            v.status = nieuwe_status
            sla_verhuur_op(verhuren)

            # Fiets weer op beschikbaar zetten
            for f in fietsen:
                if f.serial_code == v.serial_code:
                    f.status = "beschikbaar"
            sla_voorraad_op(fietsen)
            
            return True, f"Verhuur #{huur_id} is nu {nieuwe_status}."

    return False, "Verhuur niet gevonden."

#Fiets verkopen

def verkoop_fiets(klant_id, serial_code):
    klant = zoek_klant(klant_id)
    if klant is None:
        return False, "Klant niet gevonden."
    if klant.geblokkeerd == True:
        return False, "Deze klant is geblokkeerd."

    fietsen = haal_voorraad_op()
    for fiets in fietsen:
        if fiets.serial_code.lower() == serial_code.lower():
            if fiets.status != "beschikbaar":
                return False, "Deze fiets is niet beschikbaar voor verkoop."
            
            if klant.vaste_klant == True:
                prijs = fiets.koopprijs * 0.90
            else:
                prijs = fiets.koopprijs

            fiets.status = "verkocht"
            sla_voorraad_op(fietsen)
            return True, f"Fiets verkocht aan {klant.naam} voor €{round(prijs, 2)}!"

    return False, "Fiets niet gevonden."
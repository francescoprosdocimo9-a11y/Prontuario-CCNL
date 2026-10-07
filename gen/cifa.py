import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import build, write

CC = "turismo-cifa"
LIV = ["Quadro", "7°", "6°", "5°", "4°", "3°", "2°S", "2°", "1°"]
# Settore Turismo (identica ai Pubblici esercizi). Livello 1°: il testo riporta solo 3 valori.
MT = {
 "2025-06-01": [2290, 2045, 1870, 1765, 1665, 1560, 1500, 1480, None],
 "2026-06-01": [2345, 2110, 1920, 1805, 1695, 1585, 1515, 1495, 1395],
 "2027-06-01": [2390, 2150, 1955, 1835, 1725, 1610, 1545, 1520, 1415],
 "2027-12-01": [2450, 2205, 2000, 1880, 1765, 1645, 1575, 1550, 1445],
}
LS = ["Quadro", "7°", "6°", "5°", "4°", "3°", "2°", "1°"]
MS = {"1/3/2025": [2930, 2455, 2190, 1945, 1750, 1630, 1515, 1375], "1/11/2025": [2990, 2510, 2240, 1990, 1790, 1660, 1545, 1405],
      "1/11/2026": [3045, 2560, 2285, 2025, 1820, 1690, 1570, 1425], "1/2/2027": [3115, 2625, 2340, 2070, 1860, 1730, 1605, 1450]}
def eur(x): return "—" if x is None else f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
SC = {l: round(v * 0.02, 2) for l, v in zip(LIV, MT["2026-06-01"])}

ITEMS = [
 dict(id="vigenza", s="CCNIL CIFA – Confsal / Confsal Federlavoratori per i dipendenti delle PMI di Commercio, Servizi, Turismo e Pubblici esercizi (codice CNEL H03A): vale dal 1/6/2025 al 31/5/2028. Parte generale comune più sezioni settoriali; ai clienti si applica la sezione Turismo / Pubblici esercizi.",
  p=["Testo coordinato al 20/10/2025.", "Sezioni settoriali: Commercio, Servizi, Turismo, Pubblici esercizi (tabelle Turismo e Pubblici esercizi identiche)."],
  art="Art. 1, Parte settoriale", att="Beducci Travel Bus è indicato come «Autorimesse/Turismo CIFA»: verificare la sezione applicata (Turismo o Servizi).", tag=["vigenza","scadenza","cifa","confsal","h03a"]),
 dict(id="codici", s="Codice CNEL H03A. Ente bilaterale EPAR, fondo sanitario Sanarcom, contributo di assistenza contrattuale Co.As.Co.", art="Art. 80, Parte settoriale comune", tag=["h03a","epar","sanarcom","coasco","codice"]),
 dict(id="contrattazione-aziendale", s="Contrattazione integrativa aziendale o territoriale e contrattazione di prossimità nei limiti di legge; retribuzione premiale definita al secondo livello.", art="Artt. 3-5, 33", tag=["secondo livello","prossimità","premio"]),
 dict(id="prova", s="Prova in giorni di effettiva prestazione: 1° livello 45, dal 2° al 5° 60, 6° 90, 7° e Quadri 180. Dimezzata per chi ha già svolto le stesse mansioni per 3 anni o ha completato l'apprendistato. Contratti a termine: 1 giorno ogni 15 di calendario (fino a 6 mesi da 2 a 15 giorni; fino a 12 mesi massimo 30).",
  tab=[["Livello","Giorni di effettiva prestazione"],["1°","45"],["2°-5°","60"],["6°","90"],["7° e Quadri","180"]], art="Artt. 16-17", tag=["prova","giorni effettivi"]),
 dict(id="inquadramento", s="Classificazione su livelli dal 1° (più basso) al 7° più i Quadri; nel Turismo esiste anche il livello 2°S. La nuova numerazione inverte quella precedente (ex 7° = nuovo 1°, ex 1° = nuovo 7°).",
  att="Attenzione alla numerazione invertita rispetto al vecchio testo e agli altri CCNL del turismo.", art="Artt. 26-28, Parte settoriale", tag=["livelli","classificazione","ex livelli"]),
 dict(id="quadri", s="Indennità di funzione dei Quadri già compresa nel minimo: 70 € mensili nel Turismo e Pubblici esercizi, 180 € per 14 mensilità nei Servizi. Prova 180 giorni; preavviso 60/90/120 giorni.", art="Art. 25, Parte settoriale", tag=["quadri","indennità di funzione"]),
 dict(id="apprendistato", s="Apprendistato professionalizzante dai 17 anni per le qualifiche dal 2° al 7° livello: massimo 3 anni (2 per il 7°, 5 per i profili artigiani). Inquadramento due livelli sotto il finale nel primo anno, un livello sotto dal secondo anno; per il 2° livello finale si resta nel 1° per tutta la durata. Ammesso l'apprendistato stagionale.",
  art="Artt. 18-21", tag=["apprendistato","apprendisti","stagionale"]),
 dict(id="tempo-determinato", s="Contratto a termine secondo la legge, consegnato entro 5 giorni lavorativi. Recesso anticipato del datore solo per giusta causa o impossibilità sopravvenuta (con 15 giorni di preavviso); altrimenti risarcimento delle retribuzioni fino alla scadenza.",
  p=["Nelle aziende di stagione del turismo: retribuzione maggiorata del 20% per ingaggi fino a un mese, 15% fino a 2 mesi, 8% oltre i 2 mesi."], art="Art. 17, Parte settoriale", tag=["tempo determinato","stagionali","recesso"]),
 dict(id="stagionali", s="Ingaggi stagionali nel Turismo con maggiorazione della retribuzione: +20% fino a un mese, +15% fino a 2 mesi, +8% oltre i 2 mesi fino a fine stagione. Intensificazioni dell'attività (festività, manifestazioni, promozioni) giustificano il termine.",
  tab=[["Durata ingaggio","Maggiorazione"],["Fino a 1 mese","20%"],["Fino a 2 mesi","15%"],["Oltre 2 mesi","8%"]], art="Parte settoriale Turismo", tag=["stagionali","maggiorazione stagionale"]),
 dict(id="part-time", s="Clausole elastiche entro il 25% dell'orario, preavviso di 2 giorni lavorativi, maggiorazione 1,5% (collocazione) o 31,5% (aumento). Supplementare fino al 25% delle ore settimanali con maggiorazione del 30%.",
  art="Art. 24", tag=["part-time","clausole elastiche","supplementare","30%"]),
 dict(id="lavoro-intermittente", s="Lavoro intermittente nei casi di legge e del CCNIL, con indennità di disponibilità.", art="Art. 22", tag=["intermittente","a chiamata"]),
 dict(id="somministrazione", s="Somministrazione di lavoro secondo la legge.", art="Art. 23", tag=["somministrazione"]),
 dict(id="orario", s="Orario normale di 40 ore settimanali (44 o 45 per alcune figure del turismo, con divisori 190 e 195). Massimo 50/54 ore settimanali e media di 48 ore su 4 mesi.",
  art="Artt. 37-38, Parte settoriale", tag=["orario","40 ore","48 ore"]),
 dict(id="straordinario", s="Fino a 250 ore annue, obbligatorio entro 100. Maggiorazioni nel Turismo e Pubblici esercizi: straordinario diurno 30%, notturno 60%; lavoro notturno 25%; festivo e domenicale 20%. Non cumulabili: la maggiore assorbe la minore.",
  tab=[["Tipo","Maggiorazione"],["Straordinario diurno","30%"],["Straordinario notturno","60%"],["Lavoro notturno","25%"],["Festivo e domenica","20%"]],
  art="Art. 39, Parte settoriale Turismo", tag=["straordinario","250 ore","maggiorazioni"]),
 dict(id="notturno-domenicale", s="Lavoro notturno (periodo di 7 ore che comprende 24-5) +25%; lavoro festivo e domenicale +20%. Indennità domenicale del 10% del minimo per ogni ora ordinaria di domenica a chi riposa in altro giorno.",
  art="Artt. 43-44, Parte settoriale Turismo", tag=["notturno","domenica","festivo","indennità domenicale"]),
 dict(id="festivita", s="Festività nazionali e Patrono retribuite; se coincidono con la domenica spetta una quota giornaliera in più. Spettano anche in malattia, infortunio e maternità.", art="Art. 43", tag=["festività"]),
 dict(id="ferie", s="26 giorni lavorativi l'anno (4 settimane più 2 giorni), maturati in proporzione al servizio: un dodicesimo per mese o frazione superiore a 14 giorni.", art="Art. 47", tag=["ferie","26 giorni"]),
 dict(id="permessi-rol", s="Permessi annui retribuiti (PAR): 32 ore per ex festività più ROL per almeno 40 ore. In più 12 ore l'anno per visite mediche, richieste con 2 giorni di anticipo.",
  art="Artt. 41, 93", tag=["par","rol","ex festività","visite mediche"]),
 dict(id="permessi-lutto", s="3 giorni lavorativi di permesso retribuito l'anno per decesso o grave infermità del coniuge, del convivente o di un parente entro il 2° grado.", art="Art. 92", tag=["lutto","grave infermità"]),
 dict(id="congedo-matrimoniale", s="15 giorni consecutivi di calendario, richiesti con almeno 10 giorni di anticipo.", art="Art. 90", tag=["matrimonio","congedo matrimoniale"]),
 dict(id="minimi", s="Minimi tabellari mensili del Turismo / Pubblici esercizi per 14 mensilità, con tranche dal 1/6/2026, 1/6/2027 e 1/12/2027. Dal 1/6/2026: 4° livello 1.695 €, 3° 1.585 €, 2° 1.495 €, 1° 1.395 €.",
  p=["Il minimo dei Quadri comprende l'indennità di funzione di 70 €.", "Livello 1°: il testo non riporta il valore 2025."],
  tab=[["Livello","1/6/2025","1/6/2026","1/6/2027","1/12/2027"]] + [[l] + [eur(MT[d][i]) for d in sorted(MT)] for i, l in enumerate(LIV)],
  art="Parte settoriale Turismo e Pubblici esercizi", att="Tabella del testo impaginata male: abbinamento colonne ricostruito, da verificare.", tag=["minimi","paga base","tabelle"]),
 dict(id="minimi-servizi", voce="Minimi settore Servizi", cap="r", s="Sezione Servizi (nel caso si applichi a Beducci Travel Bus): minimi dal 1/3/2025, 1/11/2025, 1/11/2026 e 1/2/2027; divisore orario 168, giornaliero 26; Quadri con indennità di funzione di 180 € compresa; 5 scatti triennali del 2%.",
  tab=[["Livello"] + list(MS)] + [[l] + [eur(MS[d][i]) for d in MS] for i, l in enumerate(LS)],
  art="Parte settoriale Servizi", tag=["minimi","servizi"]),
 dict(id="divisori", s="Divisore orario 172 (40 ore), 190 (44 ore) o 195 (45 ore); giornaliero 26.", art="Parte settoriale Turismo", tag=["divisore","172","26"]),
 dict(id="mensilita-aggiuntive", s="13ª a dicembre e 14ª con la retribuzione di giugno, ciascuna pari a una mensilità di fatto; in dodicesimi con frazione superiore a 15 giorni come mese intero. La 13ª si può pagare in 12 rate mensili.",
  art="Art. 31.3, Parte settoriale comune", tag=["tredicesima","quattordicesima"]),
 dict(id="scatti", s="5 scatti triennali, ciascuno pari al 2% della retribuzione mensile.", art="Parte settoriale Turismo", att="Nel calcolatore l'importo è il 2% del minimo dal 1/6/2026.", tag=["scatti","triennali","2%"]),
 dict(id="indennita-varie", s="Maneggio di denaro 6% del minimo; indennità domenicale 10% del minimo orario; emolumento al preposto alla sicurezza pari al 5% della paga base; percentuale di servizio fissata dagli integrativi territoriali.",
  art="Parte settoriale", tag=["maneggio denaro","domenicale","preposto"]),
 dict(id="trasferta", s="Indennità di trasferta nel Turismo: 15% della retribuzione giornaliera per giornata intera, 10% per assenze tra 6 e 24 ore, 20% all'estero, oltre alle spese.", art="Art. 51, Parte settoriale Turismo", tag=["trasferta","indennità"]),
 dict(id="ratei", s="Ferie per dodicesimi (frazione oltre 14 giorni = mese); 13ª e 14ª per dodicesimi con frazione oltre 15 giorni come mese intero.", art="Artt. 31, 47", tag=["ratei","dodicesimi"]),
 dict(id="malattia-trattamento", s="Integrazione dell'INPS: carenza (giorni 1-3) al 100% per il primo evento dell'anno e al 50% per il 2° e il 3°; dal 4° al 20° giorno fino al 75%; dal 21° giorno fino al 100% della retribuzione.",
  tab=[["Giorni","Trattamento complessivo"],["1-3 (1° evento)","100%"],["1-3 (2° e 3° evento)","50%"],["4-20","75%"],["Dal 21°","100%"]], art="Art. 55", tag=["malattia","carenza","integrazione"]),
 dict(id="malattia-comporto", s="Conservazione del posto per 12 mesi nell'arco dell'ultimo triennio. Poi aspettativa non retribuita di 6 mesi, rinnovabile una volta. Esclusi dal comporto i giorni di terapie salvavita.", art="Art. 55", tag=["comporto","12 mesi","triennio","aspettativa"]),
 dict(id="infortunio", s="Infortunio sul lavoro: conservazione del posto fino a guarigione, con indennità INAIL e integrazione secondo l'art. 54.", art="Art. 54", tag=["infortunio","inail"]),
 dict(id="aspettative", s="Aspettativa non retribuita fino a 6 mesi per chi ha almeno 2 anni di anzianità, su richiesta scritta con 15 giorni di preavviso.", art="Art. 99", tag=["aspettativa","non retribuita"]),
 dict(id="disciplinare", s="Rimprovero verbale, rimprovero scritto, multa fino a 3 ore di retribuzione base, sospensione fino a 10 giorni, licenziamento. Impugnazione entro 20 giorni presso il collegio di conciliazione.", art="Artt. 60-61", tag=["disciplinare","sanzioni","multa"]),
 dict(id="preavviso", s="Licenziamento, in giorni di calendario (fino a 5 anni / 5-10 anni / oltre 10): 1° livello 15/20/20; 2° e 3° 20/30/45; 4°-6° 30/45/60; 7° e Quadri 60/90/120. Dimissioni: 30 giorni fino a 5 anni, 60 oltre.",
  tab=[["Livello","Fino a 5 anni","5-10 anni","Oltre 10 anni"],["1°","15","20","20"],["2° e 3°","20","30","45"],["4°-6°","30","45","60"],["7° e Quadri","60","90","120"],["Dimissioni (tutti)","30","60","60"]],
  art="Artt. 64, 66", tag=["preavviso","licenziamento","dimissioni"]),
 dict(id="tfr", s="TFR secondo l'art. 2120 c.c.", art="Art. 72", tag=["tfr"]),
 dict(id="ente-bilaterale", s="EPAR: 0,60% della paga base conglobata per 12 mensilità (0,50% azienda, 0,10% lavoratore). Co.As.Co.: 1% della paga base conglobata per 12 mensilità. Se l'azienda non aderisce a EPAR deve pagare un EDR dell'1% della paga base per 14 mensilità.",
  tab=[["Voce","Azienda","Lavoratore","Se non versato"],["EPAR (×12)","0,50%","0,10%","EDR 1% × 14"],["Co.As.Co. (×12)","1%","—","—"],["Sanarcom (×12)","10 €","2 €","EDR 30 € × 14"]],
  art="Parte settoriale comune", att="In anagrafica i clienti CIFA risultano senza ente bilaterale e sanità: verificare se va pagato l'EDR sostitutivo.", tag=["epar","coasco","edr","contributi"]),
 dict(id="sanita", s="Fondo Sanarcom: 12 € al mese per 12 mensilità (10 € azienda, 2 € lavoratore). Senza adesione: EDR di 30 € mensili per 14 mensilità, non assorbibile.", art="Parte settoriale comune", tag=["sanarcom","sanità","edr"]),
 dict(id="previdenza-complementare", voce="Previdenza complementare", cap="e", s="Contributo del datore pari alla metà di quello del lavoratore (2%→1%, 3%→1,5%, 4%→2%), massimo 2%. Quota d'iscrizione una tantum di 10 € a carico del lavoratore.", art="Parte settoriale comune", tag=["previdenza complementare","fondo pensione"]),
 dict(id="lavoro-agile", s="Lavoro agile e telelavoro con accordo individuale.", art="Artt. 52-53", tag=["lavoro agile","telelavoro"]),
 dict(id="riepilogo-costi", s="Costi contrattuali: 14 mensilità; EPAR 0,50% e Co.As.Co. 1% della paga base × 12; Sanarcom 10 € × 12; in alternativa EDR (30 € × 14 e 1% × 14).", art="Parte settoriale comune", tag=["costi"]),
]

REGOLE = {
 "nome": "Turismo e pubblici esercizi CIFA",
 "livelli": LIV, "livelloDefault": "4°",
 "gruppi": [{"nome": "1° livello", "livelli": ["1°"]}, {"nome": "2° e 3°", "livelli": ["2°", "2°S", "3°"]}, {"nome": "4°-6°", "livelli": ["4°", "5°", "6°"]}, {"nome": "7° e Quadri", "livelli": ["7°", "Quadro"]}],
 "preavviso": {"fasce": [{"finoAnni": 5, "label": "fino a 5 anni"}, {"finoAnni": 10, "label": "da 5 a 10 anni"}, {"finoAnni": None, "label": "oltre 10 anni"}],
  "lic": [[{"g": 15}, {"g": 20}, {"g": 30}, {"g": 60}], [{"g": 20}, {"g": 30}, {"g": 45}, {"g": 90}], [{"g": 20}, {"g": 45}, {"g": 60}, {"g": 120}]],
  "dim": [[{"g": 30}] * 4, [{"g": 60}] * 4, [{"g": 60}] * 4],
  "lavorativi": False, "decorrenza": "giorno-successivo", "nota": "Giorni di calendario.", "art": "Artt. 64, 66"},
 "prova": {"livelli": {**{l: {"g": 60, "effettivo": True, "txt": "60 giorni di effettiva prestazione"} for l in ["2°", "2°S", "3°", "4°", "5°"]},
   "1°": {"g": 45, "effettivo": True, "txt": "45 giorni di effettiva prestazione"}, "6°": {"g": 90, "effettivo": True, "txt": "90 giorni di effettiva prestazione"},
   "7°": {"g": 180, "effettivo": True, "txt": "180 giorni di effettiva prestazione"}, "Quadro": {"g": 180, "effettivo": True, "txt": "180 giorni di effettiva prestazione"}},
  "nota": "Dimezzata con 3 anni nelle stesse mansioni o apprendistato completato.", "art": "Art. 16"},
 "scatti": {"anni": 3, "max": 5, "imp": SC, "decorrenza": "mese-successivo", "nota": "5 scatti triennali del 2% della retribuzione mensile (importo calcolato sul minimo dal 1/6/2026).", "art": "Parte settoriale Turismo"},
 "minimi": [{"dal": d, "v": {l: x for l, x in zip(LIV, v) if x is not None}} for d, v in MT.items()],
 "minimiNota": "Minimo tabellare Turismo / Pubblici esercizi; Quadri comprensivi dell'indennità di funzione di 70 €. Livello 1°: valore 2025 assente nel testo.",
 "mensilita": 14, "divOra": 172, "divGiorno": 26,
 "fraz": {"giorni": 15, "op": ">"},
 "aggiuntive": [{"nome": "13ª", "meseInizio": 1}, {"nome": "14ª", "meseInizio": 7}],
 "ferie": {"giorni": 26, "txt": "26 giorni lavorativi (4 settimane più 2 giorni)"},
 "permessi": [{"label": "32 ore ex festività", "ore": 32}, {"label": "ROL almeno 40 ore", "ore": 40}],
 "ratei": {"nota": "Frazioni oltre 15 giorni = mese intero (ferie: oltre 14 giorni).", "art": "Artt. 31, 47"},
 "comporto": {"tipo": "mesi", "mesi": 36, "fasce": [{"finoAnni": None, "giorni": 365}], "separaInfortunio": True,
  "nota": "12 mesi nell'ultimo triennio; poi aspettativa non retribuita di 6 mesi rinnovabile una volta.", "art": "Art. 55"},
 "malattia": {"casi": [
   {"nome": "Primo evento nell'anno", "inps": True, "fasce": [{"dal": 1, "al": 3, "tot": 100}, {"dal": 4, "al": 20, "tot": 75}, {"dal": 21, "al": 365, "tot": 100}]},
   {"nome": "2° e 3° evento nell'anno", "inps": True, "fasce": [{"dal": 1, "al": 3, "tot": 50}, {"dal": 4, "al": 20, "tot": 75}, {"dal": 21, "al": 365, "tot": 100}]}],
  "nota": "Integrazione dell'indennità INPS fino alle percentuali indicate.", "art": "Art. 55"},
 "straord": {"voci": [
   {"l": "Straordinario diurno", "m": 30, "full": True}, {"l": "Straordinario notturno", "m": 60, "full": True},
   {"l": "Lavoro notturno", "m": 25, "full": False}, {"l": "Lavoro festivo e domenicale", "m": 20, "full": False},
   {"l": "Indennità domenicale (riposo in altro giorno)", "m": 10, "full": False}, {"l": "Supplementare part-time", "m": 30, "full": True}],
  "base": "retribuzione normale mensile ÷ 172", "nota": "Fino a 250 ore annue; maggiorazioni non cumulabili.", "art": "Art. 39, Parte settoriale Turismo"}
}

META = {
 "sigla": "Turismo CIFA", "ordine": 41,
 "nome": "CCNIL PMI Commercio, Servizi, Turismo e Pubblici esercizi (CIFA; Confsal, Confsal Federlavoratori) – sezione Turismo",
 "vigenza": "1/6/2025 - 31/5/2028", "testo": "Testo coordinato al 20/10/2025 (codice CNEL H03A)", "fonte": "Testo CIFA in Drive (CCNL 2)",
 "dubbi": [
  "Beducci Travel Bus è registrato come «Autorimesse/Turismo CIFA»: verificare se applica la sezione Turismo o Servizi (scheda «Minimi settore Servizi»).",
  "Tabella minimi Turismo impaginata male: il valore 2025 del 1° livello manca, abbinamento colonne da verificare.",
  "Clienti senza EPAR e Sanarcom in anagrafica: se non aderiscono vanno pagati gli EDR sostitutivi (1% × 14 e 30 € × 14).",
  "Scatti in percentuale (2%): il calcolatore usa un importo fisso calcolato sul minimo 2026."
 ],
 "regoleJson": REGOLE
}

if __name__ == "__main__":
    write(CC, build(CC, ITEMS), META, sys.argv[1])

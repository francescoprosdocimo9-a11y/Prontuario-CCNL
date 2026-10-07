import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import build, write

CC = "abbigliamento-pmi"
L = ["1", "2", "2 bis", "3", "3 bis", "4", "5", "6", "7", "8"]
OPL = ["Op. " + x for x in L[:6]]
IMPL = ["Imp. " + x for x in L[1:]]
LIV = OPL + IMPL
M = {  # tessile-abbigliamento-moda
 "2019-07-01": [1246.97, 1556.54, 1595.78, 1642.79, 1681.29, 1719.83, 1816.58, 1938.53, 2068.42, 2189.30],
 "2022-03-01": [1261.79, 1575.06, 1614.74, 1662.34, 1701.29, 1740.28, 1838.21, 1961.49, 2093.01, 2215.37],
 "2022-07-01": [1276.61, 1593.58, 1633.70, 1681.89, 1721.29, 1760.73, 1859.84, 1984.45, 2117.60, 2241.44],
 "2022-12-01": [1306.24, 1630.62, 1671.62, 1720.99, 1761.29, 1801.63, 1903.10, 2030.37, 2166.78, 2293.58],
}
SCL = {"1": 6.71, "2": 7.23, "2 bis": 7.23, "3": 7.75, "3 bis": 7.75, "4": 8.26, "5": 9.81, "6": 10.33, "7": 11.88, "8": 12.91}
def eur(x): return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
def row(v):
    d = dict(zip(L, v)); return {**{"Op. " + k: d[k] for k in L[:6]}, **{"Imp. " + k: d[k] for k in L[1:]}}

ITEMS = [
 dict(id="vigenza", s="CCNL per le piccole e medie imprese (fino a 249 dipendenti) del tessile-abbigliamento-moda, calzature, pelli e cuoio, occhiali, giocattoli e penne, firmato da Confartigianato Moda, CNA Federmoda, Casartigiani, CLAAI e FILCTEM-CGIL, FEMCA-CISL, UILTEC-UIL. Decorre dal 1/1/2019 e scadeva il 31/12/2022; resta in vigore fino al rinnovo.",
  p=["Ultimo testo unico disponibile: 23/3/2022 (Ipotesi 17/2/2022).","Comprende anche chimica, plastica, gomma, ceramica e vetro fino a 49 dipendenti e decorazione piastrelle."],
  art="Art. 7", att="Scaduto il 31/12/2022: verificare se è intervenuto un rinnovo dopo il 2022 e gli aumenti successivi.", tag=["vigenza","tessile","abbigliamento","moda","pmi","confartigianato","cna"]),
 dict(id="codici", s="Previdenza complementare Fon.Te. (ex Artifond); bilateralità e sanità secondo gli accordi interconfederali dell'artigianato e delle PMI. Il codice CNEL non è nel testo.", art="Comunicato 17/11/2011", tag=["fon.te","artifond","codice"]),
 dict(id="contrattazione-aziendale", s="Contrattazione su CCNL nazionale, livello regionale (a metà vigenza) e aziendale per premi legati a risultati.", art="Artt. 9-9-ter", tag=["regionale","aziendale"]),
 dict(id="prova", s="Prova in giorni di effettiva prestazione: 7° e 8° livello 6 mesi; 5° e 6° 3 mesi; 4° 2 mesi; 3° 1 mese e mezzo; 2° 1 mese; 1° 3 settimane. Nel part-time può essere prolungata in proporzione.",
  tab=[["Livello","Prova"],["7° e 8°","6 mesi"],["5° e 6°","3 mesi"],["4°","2 mesi"],["3°","1 mese e 1/2"],["2°","1 mese"],["1°","3 settimane"]],
  art="Art. 27", tag=["prova"]),
 dict(id="inquadramento", s="Inquadramento unico su livelli 1, 2, 2 bis, 3, 3 bis, 4, 5, 6, 7 e 8 (quadri), con declaratorie per operai, intermedi e impiegati; tabelle distinte per tessile-abbigliamento, calzature, pelli e cuoio, occhiali e giocattoli.",
  art="Art. 45; Parte retributiva", tag=["livelli","inquadramento"]),
 dict(id="mansioni", s="Cambiamento, cumulo e pluralità di mansioni e passaggi da operaio a intermedio o impiegato secondo gli artt. 44 e 46.", art="Artt. 44, 46", tag=["mansioni"]),
 dict(id="apprendistato", s="Apprendistato professionalizzante e addestramento secondo l'art. 28.", art="Art. 28", tag=["apprendistato"]),
 dict(id="tempo-determinato", s="Contratto a termine secondo l'art. 26 e il D.Lgs. 81/2015.", art="Art. 26", tag=["tempo determinato"]),
 dict(id="part-time", s="Part-time e job-sharing secondo gli artt. 36 e 36-bis.", art="Artt. 36, 36-bis", tag=["part-time","job sharing"]),
 dict(id="orario", s="40 ore settimanali e 8 giornaliere, di norma su 5 giorni; con 6 giornate per maggior utilizzo degli impianti l'orario scende a 36 ore per turno. Flessibilità con media su 12 mesi.",
  art="Artt. 31-32, 34", tag=["orario","40 ore","flessibilità"]),
 dict(id="permessi-rol", s="Riduzioni annue d'orario: 56 ore per i giornalieri, 52 per gli addetti a squadre (64 ore in alcuni comparti), oltre alle ex festività.",
  art="Art. 31", att="Verificare la misura applicabile al comparto dell'azienda.", tag=["riduzione orario","rol","56 ore"]),
 dict(id="straordinario", s="Straordinario volontario fino a 180 ore individuali (monte aziendale 130 ore per dipendente); le ore tra 130 e 180 si recuperano a richiesta. Straordinario diurno 35% (prime 5 ore settimanali) e 45% (successive), notturno 56%, festivo diurno 61%, festivo notturno 66%. Lavoro notturno 44% (turni 6x6 38%), domenicale e festivo diurno 38%, notturno festivo 54%; non cumulabili.",
  art="Artt. 33, 33-bis, 35", tag=["straordinario","notturno","festivo","180 ore"]),
 dict(id="notturno-domenicale", s="Notturno (22-6) 44%, turni 6x6 a rotazione 38%, domenicale e festivo diurno 38%, domenicale e festivo notturno 54% sulla retribuzione di fatto.", art="Art. 35", tag=["notturno","domenicale","festivo"]),
 dict(id="ferie", s="4 settimane l'anno con retribuzione di fatto, di cui 3 consecutive tra giugno e settembre; per intermedi e impiegati 1 giorno in più da 12 a 20 anni e 5 settimane oltre 20 anni.",
  art="Art. 12 operai; art. 3 intermedi; art. 4 impiegati", tag=["ferie","4 settimane"]),
 dict(id="permessi-lutto", s="Permessi, assenze e aspettative secondo l'art. 48 e la legge 53/2000.", art="Art. 48", tag=["permessi","lutto"]),
 dict(id="congedo-matrimoniale", s="Congedo matrimoniale retribuito secondo l'art. 51.", art="Art. 51", tag=["matrimonio"]),
 dict(id="studio", s="Diritto allo studio e facilitazioni per i corsi secondo gli artt. 56-58.", art="Artt. 56-58", tag=["studio"]),
 dict(id="minimi", s="Minimi mensili del settore tessile-abbigliamento-moda dal 1/12/2022: 1° 1.306,24 €, 2° 1.630,62, 2 bis 1.671,62, 3° 1.720,99, 3 bis 1.761,29, 4° 1.801,63, 5° 1.903,10, 6° 2.030,37, 7° 2.166,78, 8° 2.293,58. Tabelle diverse per calzature, pelli e cuoio, occhiali e giocattoli.",
  tab=[["Livello","1/7/2019","1/3/2022","1/7/2022","1/12/2022"]] + [[l] + [eur(M[d][i]) for d in sorted(M)] for i, l in enumerate(L)],
  art="Parte retributiva", att="Ultima tranche nel testo: 1/12/2022. Verificare eventuali aumenti successivi.", tag=["minimi","tabelle","tessile"]),
 dict(id="divisori", s="Retribuzione oraria secondo l'art. 38 (mensile ÷ 173).", art="Art. 38", tag=["divisore","173"]),
 dict(id="mensilita-aggiuntive", s="13ª mensilità per operai, intermedi e impiegati secondo le rispettive parti speciali.", art="Art. 13 operai; art. 4 intermedi; art. 5 impiegati", tag=["tredicesima"]),
 dict(id="scatti", s="4 aumenti biennali dal mese successivo al biennio, fissati in lire (8° 25.000 = 12,91 €; 7° 11,88 €; 6° 10,33 €; 5° 9,81 €; 4° 8,26 €; 3° 7,75 €; 2° 7,23 €; 1° 6,71 €).",
  art="Art. 39", att="Importi in euro ricavati dalla conversione delle lire (1.936,27).", tag=["scatti","biennali"]),
 dict(id="trasferta", s="Trasferte e trasferimenti secondo gli artt. 41-42.", art="Artt. 41-42", tag=["trasferta"]),
 dict(id="malattia-trattamento", s="Operai: integrazione dell'INPS fino al 50% della retribuzione di fatto nei giorni 1-3 e al 100% netto dal 4° al 180° giorno; oltre il 6° mese, cessata l'INPS, 50% fino al termine del comporto. Intermedi: 100% netto per 4 mesi e poi metà retribuzione.",
  art="Art. 14 operai; art. 5 intermedi; art. 7 impiegati", tag=["malattia","integrazione","carenza 50%"]),
 dict(id="malattia-comporto", s="Tessile-abbigliamento: conservazione del posto per 15 mesi, anche con più malattie nell'arco di 30 mesi (909 giorni). Calzature: 12 mesi in 28. Poi aspettativa fino a 8 mesi per ricoveri e terapie salvavita.",
  art="Art. 53", tag=["comporto","15 mesi","30 mesi"]),
 dict(id="malattia-obblighi", s="Certificato entro 2 giorni; reperibilità 10-12 e 17-19 tutti i giorni.", art="Art. 53", tag=["certificato","reperibilità"]),
 dict(id="infortunio", s="Infortunio sul lavoro e malattie professionali secondo l'art. 52.", art="Art. 52", tag=["infortunio"]),
 dict(id="maternita", s="Gravidanza e puerperio secondo le parti speciali e la legge.", art="Art. 15 operai; art. 6 intermedi; art. 8 impiegati", tag=["maternità"]),
 dict(id="disciplinare", s="Provvedimenti disciplinari e procedura secondo gli artt. 64-65; licenziamenti all'art. 66.", art="Artt. 64-66", tag=["disciplinare"]),
 dict(id="danni", s="Trattenute per risarcimento danni secondo l'art. 47.", art="Art. 47", tag=["danni"]),
 dict(id="divise", s="Abiti da lavoro secondo l'art. 54.", art="Art. 54", tag=["abiti da lavoro"]),
 dict(id="preavviso", s="Operai e apprendisti: 2 settimane. Impiegati e quadri (dalla metà o dalla fine del mese): 8° e 7° 2/3/4 mesi; 6° e 5° 1,5/2/3 mesi; 4°-2° 1/1,5/2 mesi (fino a 5, 5-10, oltre 10 anni).",
  tab=[["Anzianità","Operai","Imp. 8°-7°","Imp. 6°-5°","Imp. 4°-2°"],["Fino a 5 anni","2 settimane","2 mesi","1 mese e 1/2","1 mese"],["5-10 anni","2 settimane","3 mesi","2 mesi","1 mese e 1/2"],["Oltre 10 anni","2 settimane","4 mesi","3 mesi","2 mesi"]],
  art="Art. 16 operai; art. 12 impiegati", tag=["preavviso"]),
 dict(id="tfr", s="TFR secondo la legge 297/1982.", art="Art. 17 operai; art. 13 impiegati", tag=["tfr"]),
 dict(id="previdenza", s="Previdenza complementare Fon.Te. (dal 2011, ex Artifond).", art="Comunicato 17/11/2011", tag=["fon.te"]),
 dict(id="diritti-sindacali", s="RSU, delegato d'impresa, assemblee e permessi sindacali secondo gli artt. 16-22.", art="Artt. 16-22", tag=["rsu","assemblea"]),
 dict(id="contributi-sindacali", s="Versamento dei contributi sindacali su delega secondo l'art. 23.", art="Art. 23", tag=["contributi sindacali"]),
 dict(id="sicurezza", s="Ambiente di lavoro e doveri di aziende e lavoratori secondo l'art. 59.", art="Art. 59", tag=["sicurezza"]),
 dict(id="lavoro-agile", s="Telelavoro secondo la disciplina contrattuale dedicata.", art="Art. ___ Telelavoro", tag=["telelavoro"]),
]

def pv(o, a, b, c): return [{"g": 14}, a, b, c]
REGOLE = {
 "nome": "Abbigliamento PMI (tessile-moda)",
 "livelli": LIV, "livelloDefault": "Op. 3",
 "gruppi": [{"nome": "Operai", "livelli": OPL}, {"nome": "Impiegati 8° e 7°", "livelli": ["Imp. 7", "Imp. 8"]}, {"nome": "Impiegati 6° e 5°", "livelli": ["Imp. 5", "Imp. 6"]},
            {"nome": "Impiegati 4°-2°", "livelli": ["Imp. 2", "Imp. 2 bis", "Imp. 3", "Imp. 3 bis", "Imp. 4"]}],
 "preavviso": {"fasce": [{"finoAnni": 5, "label": "fino a 5 anni"}, {"finoAnni": 10, "label": "da 5 a 10 anni"}, {"finoAnni": None, "label": "oltre 10 anni"}],
  "lic": [pv(0, {"m": 2}, {"m": 1, "g": 15}, {"m": 1}), pv(0, {"m": 3}, {"m": 2}, {"m": 1, "g": 15}), pv(0, {"m": 4}, {"m": 3}, {"m": 2})],
  "dim": [pv(0, {"m": 2}, {"m": 1, "g": 15}, {"m": 1}), pv(0, {"m": 3}, {"m": 2}, {"m": 1, "g": 15}), pv(0, {"m": 4}, {"m": 3}, {"m": 2})],
  "lavorativi": False, "decorrenza": "1-16", "decorrenzaGruppi": ["giorno-successivo", "1-16", "1-16", "1-16"],
  "nota": "Operai: 2 settimane. Impiegati: dalla metà o dalla fine del mese.", "art": "Art. 16 operai; art. 12 impiegati"},
 "prova": {"livelli": {**{l: {"g": 21, "effettivo": True, "txt": "3 settimane di effettiva prestazione"} for l in ["Op. 1"]},
   **{l: {"m": 1, "txt": "1 mese di effettiva prestazione"} for l in ["Op. 2", "Op. 2 bis", "Imp. 2", "Imp. 2 bis"]},
   **{l: {"m": 1, "g": 15, "txt": "1 mese e mezzo di effettiva prestazione"} for l in ["Op. 3", "Op. 3 bis", "Imp. 3", "Imp. 3 bis"]},
   **{l: {"m": 2, "txt": "2 mesi di effettiva prestazione"} for l in ["Op. 4", "Imp. 4"]},
   **{l: {"m": 3, "txt": "3 mesi di effettiva prestazione"} for l in ["Imp. 5", "Imp. 6"]}, **{l: {"m": 6, "txt": "6 mesi di effettiva prestazione"} for l in ["Imp. 7", "Imp. 8"]}},
  "nota": "Il CCNL parla di effettiva prestazione: la data di fine è indicativa.", "art": "Art. 27"},
 "scatti": {"anni": 2, "max": 4, "imp": {**{"Op. " + k: SCL[k] for k in L[:6]}, **{"Imp. " + k: SCL[k] for k in L[1:]}}, "decorrenza": "mese-successivo", "nota": "Importi convertiti dalle lire.", "art": "Art. 39"},
 "minimi": [{"dal": d, "v": row(v)} for d, v in M.items()],
 "minimiNota": "Minimi del settore tessile-abbigliamento-moda (calzature, pelli, occhiali e giocattoli hanno tabelle proprie).",
 "mensilita": 13, "divOra": 173, "divGiorno": 26,
 "fraz": {"giorni": 15, "op": ">="},
 "aggiuntive": [{"nome": "13ª", "meseInizio": 1}],
 "ferie": {"giorni": 24, "txt": "4 settimane (intermedi e impiegati: più giorni oltre 12 e 20 anni)"},
 "permessi": [{"label": "56 ore riduzione orario (giornalieri)", "ore": 56}, {"label": "52 ore (addetti a squadre)", "ore": 52}],
 "ratei": {"nota": "Dodicesimi.", "art": "Artt. 12-13 operai"},
 "comporto": {"tipo": "mesi", "mesi": 30, "fasce": [{"finoAnni": None, "giorni": 456}], "separaInfortunio": False,
  "nota": "15 mesi nell'arco di 30 mesi (909 giorni) per il tessile-abbigliamento; calzature 12 mesi in 28.", "art": "Art. 53"},
 "malattia": {"casi": [
   {"nome": "Operai", "inps": True, "fasce": [{"dal": 1, "al": 3, "tot": 50}, {"dal": 4, "al": 180, "tot": 100}, {"dal": 181, "al": 456, "tot": 50}]},
   {"nome": "Intermedi", "inps": True, "fasce": [{"dal": 1, "al": 120, "tot": 100}, {"dal": 121, "al": 456, "tot": 50}]}],
  "nota": "Operai: 100% della retribuzione netta dal 4° giorno (il calcolatore usa il lordo).", "art": "Art. 14 operai; art. 5 intermedi"},
 "straord": {"voci": [{"l": "Straordinario diurno (prime 5 ore settimanali)", "m": 35, "full": True}, {"l": "Straordinario diurno (ore successive)", "m": 45, "full": True}, {"l": "Straordinario notturno", "m": 56, "full": True}, {"l": "Straordinario festivo diurno", "m": 61, "full": True}, {"l": "Straordinario festivo notturno", "m": 66, "full": True}, {"l": "Lavoro notturno", "m": 44, "full": True}, {"l": "Notturno turni 6x6", "m": 38, "full": True},
   {"l": "Domenicale e festivo diurno", "m": 38, "full": True}, {"l": "Domenicale e festivo notturno", "m": 54, "full": True}],
  "base": "retribuzione di fatto ÷ 173", "nota": "Limite 180 ore individuali; maggiorazioni non cumulabili, la maggiore assorbe la minore.", "art": "Artt. 33, 35"}
}

META = {
 "sigla": "Abbigliamento PMI", "ordine": 40,
 "nome": "CCNL piccola e media impresa del tessile-abbigliamento-moda, calzature, pelli e cuoio, occhiali, giocattoli (Confartigianato Moda, CNA Federmoda, Casartigiani, CLAAI; FILCTEM-CGIL, FEMCA-CISL, UILTEC-UIL)",
 "vigenza": "1/1/2019 - 31/12/2022", "testo": "Testo unico vigente al 23/3/2022", "fonte": "TeleConsul, stampa in Drive (CCNL 2)",
 "dubbi": [
  "CCNL scaduto il 31/12/2022: il testo in Drive non contiene rinnovi successivi.",
  "Il cliente Italian Factory è registrato come «Abbigliamento industria»: il testo caricato è quello per PMI di Confartigianato e CNA, da verificare con l'azienda.",
  "Tabella del calcolatore: settore tessile-abbigliamento-moda.",
  "Scatti di anzianità espressi in lire nel testo.",
  "Codice CNEL non riportato nel testo."
 ],
 "regoleJson": REGOLE
}

if __name__ == "__main__":
    write(CC, build(CC, ITEMS), META, sys.argv[1])

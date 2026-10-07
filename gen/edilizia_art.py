import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import build, write

CC = "edilizia-artigianato"
OP = ["Op. comune (1°)", "Op. qualificato (2°)", "Op. specializzato (3°)", "Op. 4° livello"]
IMP = ["Imp. 1° livello", "Imp. 2° livello", "Imp. 3° livello", "Imp. 4° livello", "Imp. 5° livello", "Imp. 6° livello", "Imp. 7° livello"]
LIV = OP + IMP
# minimi mensili per livello 1°..7°
M = {"2025-05-01": [1062.30, 1239.90, 1381.22, 1485.23, 1593.54, 1912.08, 2147.21],
     "2026-01-01": [1097.30, 1280.15, 1426.72, 1533.88, 1646.04, 1975.08, 2218.96],
     "2027-01-01": [1132.30, 1320.40, 1472.22, 1582.53, 1698.54, 2038.08, 2290.71],
     "2028-01-01": [1165.30, 1358.35, 1515.12, 1628.40, 1748.04, 2097.48, 2358.36]}
SC_IMP = {"Imp. 2° livello": 9.86, "Imp. 3° livello": 10.78, "Imp. 4° livello": 11.54, "Imp. 5° livello": 12.55, "Imp. 6° livello": 15.42, "Imp. 7° livello": 16.73}
def eur(x): return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
def row(v): return {**dict(zip(OP, v[:4])), **dict(zip(IMP, v))}

ITEMS = [
 dict(id="vigenza", s="CCNL per i dipendenti delle imprese artigiane e delle PMI industriali dell'edilizia (ANAEPA-Confartigianato, CNA Costruzioni, FIAE-Casartigiani, CLAAI; FENEAL-UIL, FILCA-CISL, FILLEA-CGIL) del 20/5/2025: vale dal 1/5/2025 al 30/9/2028. Senza disdetta 6 mesi prima si rinnova.",
  p=["Testo definitivo sottoscritto il 10/2/2026, con verbali su DUE, bilateralità, Prevedi e Fondo FAQS.",
     "Gli integrativi territoriali rinnovati nel 2024-2025 hanno efficacia non prima del 1/2/2026."],
  art="Art. 104", tag=["vigenza","edilizia","artigianato","anaepa","cna","fillea"]),
 dict(id="codici", s="Enti collegati: Cassa Edile artigiana / Edilcassa (accantonamenti ferie e gratifica), CNCE, Formedil, Prevedi (previdenza), Sanedil (sanità), Fondo prepensionamenti, FIO, FAQS.",
  art="Artt. 21, 43, 92, 96, 98, 102-103", tag=["cassa edile","edilcassa","prevedi","sanedil","cnce"]),
 dict(id="contrattazione-aziendale", voce="Contrattazione territoriale e EVR", s="Accordi locali (regionali/provinciali) fissano orari, indennità territoriale di settore, EVR, trasferte, ferie e welfare; l'Elemento Variabile della Retribuzione dipende dagli indicatori territoriali.",
  art="Artt. 15, 42, 50", tag=["integrativo","territoriale","evr"]),
 dict(id="prova", s="Operai: 35 giorni di lavoro (4° livello), 30 (specializzati e autisti di autobetoniere), 25 (qualificati), 15 (altri). Impiegati: 6 mesi (7° livello), 5 mesi (6°), 3 mesi (5° e assistenti tecnici di 4°), 2 mesi (4°, 3°, 2°, 1°).",
  p=["Operai esenti se già occupati nella stessa impresa e mansione con rapporto cessato da non oltre 3 anni (impiegati: 1 anno).",
     "La malattia sospende la prova se non supera la sua durata; infortunio sul lavoro fino a guarigione (impiegati)."],
  tab=[["Lavoratore","Prova"],["Operaio 4° livello","35 giorni di lavoro"],["Operaio specializzato","30 giorni di lavoro"],["Operaio qualificato","25 giorni di lavoro"],["Altri operai","15 giorni di lavoro"],["Impiegato 7°","6 mesi"],["Impiegato 6°","5 mesi"],["Impiegato 5° e assistente tecnico 4°","3 mesi"],["Impiegato 4°, 3°, 2°, 1°","2 mesi"]],
  art="Artt. 3, 46", tag=["prova","operai","impiegati"]),
 dict(id="inquadramento", s="Classificazione unica su 7 livelli con parametri da 100 (operaio comune, 1°) a 205 (7° livello); quadri regolati dall'art. 78.",
  art="Artt. 77-78", tag=["livelli","classificazione","parametri"]),
 dict(id="mansioni", s="Mutamento di mansioni e mansioni promiscue con trattamento della mansione superiore se prevalente; passaggio da operaio a impiegato secondo l'art. 89.",
  art="Artt. 4-5, 59, 89", tag=["mansioni","promiscue"]),
 dict(id="apprendistato", s="Apprendistato professionalizzante regolato dall'Allegato D (durate, retribuzione e formazione specifiche dell'edilizia artigiana).",
  art="Allegato D", tag=["apprendistato"]),
 dict(id="tempo-determinato", s="Contratto a termine secondo il D.Lgs. 81/2015 e l'art. 93 del CCNL; distacco temporaneo e somministrazione agli artt. 94-95.",
  art="Artt. 93-95", tag=["tempo determinato","somministrazione","distacco"]),
 dict(id="part-time", s="Part-time regolato dall'art. 97 con limiti percentuali per gli operai e obbligo di contribuzione Cassa Edile sulle ore contrattuali.",
  art="Art. 97", tag=["part-time"]),
 dict(id="orario", s="40 ore settimanali di media annua, massimo 10 ore al giorno; distribuzione fissata dagli integrativi. Discontinui e custodi con orari specifici; flessibilità e lavoro a turni all'art. 9.",
  art="Artt. 6, 8-9, 47", tag=["orario","40 ore","media annua"]),
 dict(id="permessi-rol", s="Operai: riposi annui di 88 ore (1 ora ogni 20 di lavoro ordinario), pagati con la percentuale del 4,95% corrisposta direttamente dall'impresa a ogni periodo di paga.",
  art="Art. 7", tag=["riposi annui","88 ore","4,95%"]),
 dict(id="straordinario", s="Straordinario fino a 250 ore annue con preavviso di 48 ore. Maggiorazioni: straordinario 35%, festivo 45%, straordinario festivo 55%, notturno non in turni 28%, turni diurni 12%, turni notturni 14%, guardiano 8%, notturno continuativo 16%, straordinario notturno 40%, festivo notturno 50%, festivo notturno straordinario 70%, domenica con riposo compensativo 8%.",
  tab=[["Prestazione","Maggiorazione"],["Straordinario","35%"],["Festivo","45%"],["Straordinario festivo","55%"],["Notturno non in turni","28%"],["Turni diurni avvicendati","12%"],["Turni notturni avvicendati","14%"],["Straordinario notturno","40%"],["Festivo notturno","50%"],["Festivo notturno straordinario","70%"],["Domenica con riposo compensativo","8%"]],
  art="Artt. 22, 57", tag=["straordinario","maggiorazioni","250 ore"]),
 dict(id="notturno-domenicale", s="Notturno (22-6) non in turni 28%, in turni 14%, guardiano 8%; domenica con riposo compensativo 8%; festivo 45%.",
  art="Art. 22", tag=["notturno","domenica","festivo"]),
 dict(id="festivita", s="Festività nazionali e infrasettimanali secondo gli artt. 20 e 61; per gli operai pagate con le regole della Cassa Edile.",
  art="Artt. 20, 61", tag=["festività"]),
 dict(id="ferie", s="4 settimane di calendario (160 ore per gli operai di produzione). Per gli operai ferie e gratifica natalizia sono pagate tramite accantonamento alla Cassa Edile (18,5%). Malattia con ricovero oltre 3 giorni o prognosi oltre 10 giorni sospende le ferie.",
  art="Artt. 18, 21, 62", tag=["ferie","4 settimane","cassa edile"]),
 dict(id="permessi-lutto", s="Assenze e permessi, compresi quelli per lutto e grave infermità, secondo l'art. 87 e la legge 53/2000.",
  art="Art. 87", tag=["permessi","lutto"]),
 dict(id="congedo-matrimoniale", s="Congedo matrimoniale retribuito per operai e impiegati secondo gli artt. 29 e 68.", art="Artt. 29, 68", tag=["matrimonio"]),
 dict(id="studio", s="Diritto allo studio secondo l'art. 86.", art="Art. 86", tag=["studio"]),
 dict(id="minimi", s="Minimi mensili per livello (parametro 100 = operaio comune): 1° 1.097,30 € dal 1/1/2026, 2° 1.280,15, 3° 1.426,72, 4° 1.533,88, 5° 1.646,04, 6° 1.975,08, 7° 2.218,96. Per gli operai la paga oraria = minimo mensile ÷ 173; si aggiungono contingenza, ITS ed EVR territoriali.",
  tab=[["Livello","1/5/2025","1/1/2026","1/1/2027","1/1/2028"]] + [[f"{i+1}°"] + [eur(M[d][i]) for d in sorted(M)] for i in range(7)],
  art="Art. 101; Allegato A", att="Ex contingenza, ITS ed EVR non sono nella tabella: il calcolatore usa solo il minimo.", tag=["minimi","paga base","stipendi"]),
 dict(id="divisori", s="Operai: quota oraria = mensile ÷ 173 (÷ 208 per i discontinui). Impiegati: mensile.", art="Artt. 14, 25", tag=["divisore","173","208"]),
 dict(id="mensilita-aggiuntive", s="Operai: gratifica natalizia di 173 ore pagata tramite Cassa Edile. Impiegati: 13ª mensilità e premio annuo (art. 64) più premio di fedeltà.",
  art="Artt. 19, 21, 63-65", tag=["tredicesima","gratifica","premio annuo"]),
 dict(id="scatti", s="Impiegati: 5 scatti biennali (7° 16,73 €, 6° 15,42, 5° 12,55, 4° 11,54, 3° 10,78, 2° 9,86). Operai: niente scatti aziendali, c'è l'anzianità professionale edile (APE) pagata dalla Cassa Edile.",
  art="Artt. 31, 56", tag=["scatti","ape","biennali"]),
 dict(id="indennita-varie", s="Indennità per lavori speciali disagiati, alta montagna, cassoni, uso del mezzo proprio, cassa e maneggio denaro; mense aziendali.",
  art="Artt. 23, 52-55", tag=["indennità","lavori disagiati"]),
 dict(id="trasferta", s="Trasferta regolata dall'art. 24 (novato dall'Allegato C-2025) per gli operai e dall'art. 58 per gli impiegati.", art="Artt. 24, 58", tag=["trasferta"]),
 dict(id="malattia-trattamento", s="Operai: l'impresa paga quote orarie sul minimo, ITS e contingenza: carenza al 54,95% se la malattia supera 6 giorni (104,95% se supera 12); dal 4° al 20° giorno integrazione di 37,95 punti all'INPS, dal 21° al 180° di 15,65 punti; dal 181° al 365° (non indennizzato INPS) 54,95%. Impiegati: 100% per 6 mesi, poi 75% o 50% secondo l'anzianità.",
  p=["Malattie fino a 6 giorni: carenza non pagata; spetta comunque il 4,95% dei riposi annui.",
     "Durante la malattia l'impresa accantona in Cassa Edile la percentuale per ferie e gratifica."],
  tab=[["Operai","Coefficiente azienda"],["Giorni 1-3 (malattia oltre 6 gg)","0,5495"],["Giorni 1-3 (malattia oltre 12 gg)","1,0495"],["Giorni 4-20","0,3795 + INPS"],["Giorni 21-180","0,1565 + INPS"],["Giorni 181-365","0,5495"]],
  art="Artt. 27, 66", tag=["malattia","carenza","coefficienti","impiegati"]),
 dict(id="malattia-comporto", s="Operai: 9 mesi consecutivi (12 oltre 3 anni e mezzo di anzianità); con più malattie 9 mesi nei 20 mesi consecutivi (12 nei 24). Impiegati: 6 mesi fino a 2 anni, fino a 12 mesi oltre; con più malattie 9 mesi in 12, 12 in 18, 15 in 24.",
  art="Artt. 27, 66", tag=["comporto","operai","impiegati"]),
 dict(id="malattia-obblighi", s="Operai: comunicare l'assenza in giornata e il certificato entro 2 giorni. Impiegati: entro 24 ore e certificato entro 3 giorni.", art="Artt. 27, 66", tag=["certificato","comunicazione"]),
 dict(id="infortunio", s="Infortunio sul lavoro e malattia professionale con integrazione aziendale all'INAIL secondo gli artt. 28 e 67.", art="Artt. 28, 67", tag=["infortunio","inail"]),
 dict(id="aspettative", s="Aspettativa non retribuita per gravi motivi secondo gli artt. 30, 69 e 85.", art="Artt. 30, 69, 85", tag=["aspettativa"]),
 dict(id="disciplinare", s="Provvedimenti disciplinari comuni a operai e impiegati secondo l'art. 88.", art="Art. 88", tag=["disciplinare"]),
 dict(id="preavviso", s="Operai: 7 giorni lavorativi fino a 3 anni di anzianità ininterrotta, 10 oltre. Impiegati (dalla metà o dalla fine del mese; dimissioni a metà): 1ª super e 1ª categoria 2/3/4 mesi; 2ª categoria e assistenti tecnici 1,5/2/3 mesi; 3ª, 4ª e 5ª 1/1,5/2 mesi (fino a 5, 5-10, oltre 10 anni).",
  art="Artt. 33, 72", tag=["preavviso","operai","impiegati"]),
 dict(id="tfr", s="TFR secondo la legge; per gli operai la gratifica e le ferie accantonate in Cassa Edile seguono le regole dell'art. 38.", art="Artt. 38, 70", tag=["tfr"]),
 dict(id="sanita", s="Fondo sanitario Sanedil a carico dell'impresa secondo l'art. 98.", art="Art. 98", tag=["sanedil","sanità"]),
 dict(id="previdenza", s="Previdenza complementare Prevedi con contributo contrattuale secondo l'art. 92 e l'accordo 4/7/2025.", art="Art. 92", tag=["prevedi","previdenza"]),
 dict(id="ente-bilaterale", s="Iscrizione alla Cassa Edile artigiana / Edilcassa e versamento degli accantonamenti (18,5% per ferie e gratifica, 14,20% al netto) e dei contributi per CNCE, Formedil, Sanedil, Fondo prepensionamenti, FIO e FAQS.", art="Artt. 21, 43, 96; Allegato B", tag=["cassa edile","accantonamenti","18,5%"]),
 dict(id="contributi-sindacali", s="Quote sindacali trattenute su delega secondo gli artt. 41 e 76.", art="Artt. 41, 76", tag=["contributi sindacali"]),
 dict(id="sicurezza", s="Sicurezza del lavoro, RLS e RLST (accordo allegato all'art. 84), formazione obbligatoria Formedil per i nuovi ingressi.", art="Artt. 39-40, 83-84", tag=["sicurezza","rlst","formedil"]),
 dict(id="appalti", s="Disciplina dell'impiego di manodopera negli appalti e congruità secondo l'art. 17.", art="Art. 17", tag=["appalti","congruità"]),
 dict(id="riepilogo-costi", s="Costi contrattuali: accantonamento Cassa Edile 18,5% per gli operai, 4,95% per i riposi annui, contributi Cassa Edile ed enti, Prevedi, Sanedil, EVR territoriale.", art="Artt. 7, 21, 92, 98", tag=["costi","cassa edile"]),
]

REGOLE = {
 "nome": "Edilizia artigianato",
 "livelli": LIV, "livelloDefault": "Op. qualificato (2°)",
 "gruppi": [{"nome": "Operai", "livelli": OP}, {"nome": "Impiegati 6° e 7° (1ª e 1ª super)", "livelli": IMP[5:]},
            {"nome": "Impiegati 4° e 5° (2ª e assistenti)", "livelli": IMP[3:5]}, {"nome": "Impiegati 1°, 2°, 3°", "livelli": IMP[:3]}],
 "preavviso": {"fasce": [{"finoAnni": 3, "label": "fino a 3 anni"}, {"finoAnni": 5, "label": "oltre 3 e fino a 5 anni"}, {"finoAnni": 10, "label": "oltre 5 e fino a 10 anni"}, {"finoAnni": None, "label": "oltre 10 anni"}],
  "lic": [[{"g": 7, "lav": True}, {"m": 2}, {"m": 1, "g": 15}, {"m": 1}], [{"g": 10, "lav": True}, {"m": 2}, {"m": 1, "g": 15}, {"m": 1}],
          [{"g": 10, "lav": True}, {"m": 3}, {"m": 2}, {"m": 1, "g": 15}], [{"g": 10, "lav": True}, {"m": 4}, {"m": 3}, {"m": 2}]],
  "dim": [[{"g": 7, "lav": True}, {"m": 1}, {"g": 23, "txt": "22 giorni e mezzo (metà)"}, {"g": 15}], [{"g": 10, "lav": True}, {"m": 1}, {"g": 23, "txt": "22 giorni e mezzo (metà)"}, {"g": 15}],
          [{"g": 10, "lav": True}, {"m": 1, "g": 15}, {"m": 1}, {"g": 23, "txt": "22 giorni e mezzo (metà)"}], [{"g": 10, "lav": True}, {"m": 2}, {"m": 1, "g": 15}, {"m": 1}]],
  "lavorativi": False, "decorrenza": "1-16", "decorrenzaGruppi": ["giorno-successivo", "1-16", "1-16", "1-16"],
  "nota": "Operai: giorni lavorativi da qualsiasi giorno. Impiegati: dalla metà o dalla fine del mese; nelle dimissioni i termini sono dimezzati.", "art": "Artt. 33, 72"},
 "prova": {"livelli": {"Op. comune (1°)": {"g": 15, "effettivo": True, "txt": "15 giorni di lavoro"}, "Op. qualificato (2°)": {"g": 25, "effettivo": True, "txt": "25 giorni di lavoro"},
   "Op. specializzato (3°)": {"g": 30, "effettivo": True, "txt": "30 giorni di lavoro"}, "Op. 4° livello": {"g": 35, "effettivo": True, "txt": "35 giorni di lavoro"},
   **{l: {"m": 2, "txt": "2 mesi"} for l in IMP[:4]}, "Imp. 5° livello": {"m": 3, "txt": "3 mesi"}, "Imp. 6° livello": {"m": 5, "txt": "5 mesi"}, "Imp. 7° livello": {"m": 6, "txt": "6 mesi"}},
  "nota": "Assistenti tecnici di 4° livello: 3 mesi.", "art": "Artt. 3, 46"},
 "scatti": {"anni": 2, "max": 5, "imp": {**{l: 0 for l in OP}, "Imp. 1° livello": 0, **SC_IMP}, "decorrenza": "mese-successivo",
  "nota": "Solo impiegati; per gli operai c'è l'anzianità professionale edile pagata dalla Cassa Edile.", "art": "Art. 56"},
 "minimi": [{"dal": d, "v": row(v)} for d, v in M.items()],
 "minimiNota": "Minimi mensili di paga base e stipendio (operai: ÷ 173 per la paga oraria). Esclusi contingenza, ITS ed EVR territoriali.",
 "mensilita": 13, "divOra": 173, "divGiorno": 26,
 "fraz": {"giorni": 15, "op": ">"},
 "aggiuntive": [{"nome": "13ª (operai tramite Cassa Edile)", "meseInizio": 1}],
 "ferie": {"ore": 160, "txt": "4 settimane di calendario (160 ore); operai tramite Cassa Edile"},
 "permessi": [{"label": "88 ore riposi annui (operai)", "ore": 88}],
 "ratei": {"nota": "Operai: ferie e gratifica pagate tramite accantonamento alla Cassa Edile (18,5%). Impiegati in dodicesimi.", "art": "Artt. 18-21, 62-63"},
 "comporto": {"tipo": "mesi", "mesi": 20, "fasce": [{"finoAnni": 3.5, "giorni": 274, "mesi": 20}, {"finoAnni": None, "giorni": 365, "mesi": 24}], "separaInfortunio": True,
  "nota": "Regole degli OPERAI: 9 mesi nell'arco di 20 mesi fino a 3 anni e mezzo, 12 mesi in 24 oltre. Impiegati: 9 in 12, 12 in 18, 15 in 24 secondo l'anzianità.", "art": "Artt. 27, 66"},
 "malattia": {"casi": [
   {"nome": "Operai - malattia oltre 12 giorni", "inps": True, "fasce": [{"dal": 1, "al": 3, "tot": 100}, {"dal": 4, "al": 20, "tot": 87.95}, {"dal": 21, "al": 180, "tot": 82.31}, {"dal": 181, "al": 365, "tot": 54.95}]},
   {"nome": "Operai - malattia da 7 a 12 giorni", "inps": True, "fasce": [{"dal": 1, "al": 3, "tot": 54.95}, {"dal": 4, "al": 12, "tot": 87.95}]},
   {"nome": "Impiegati - fino a 2 anni", "inps": True, "fasce": [{"dal": 1, "al": 180, "tot": 100}]},
   {"nome": "Impiegati - oltre 6 anni", "inps": True, "fasce": [{"dal": 1, "al": 180, "tot": 100}, {"dal": 181, "al": 270, "tot": 75}, {"dal": 271, "al": 365, "tot": 50}]}],
  "nota": "Operai: quote orarie con coefficienti su minimo, ITS e contingenza (calcolatore approssimato). Impiegati da 2 a 6 anni: 100% per 6 mesi e 50% per i restanti.", "art": "Artt. 27, 66"},
 "straord": {"voci": [
   {"l": "Straordinario", "m": 35, "full": True}, {"l": "Festivo", "m": 45, "full": True}, {"l": "Straordinario festivo", "m": 55, "full": True},
   {"l": "Notturno non in turni", "m": 28, "full": False}, {"l": "Turni diurni avvicendati", "m": 12, "full": False}, {"l": "Turni notturni avvicendati", "m": 14, "full": False},
   {"l": "Notturno guardiano", "m": 8, "full": False}, {"l": "Notturno continuativo", "m": 16, "full": False}, {"l": "Straordinario notturno", "m": 40, "full": True},
   {"l": "Festivo notturno", "m": 50, "full": True}, {"l": "Festivo notturno straordinario", "m": 70, "full": True}, {"l": "Domenica con riposo compensativo", "m": 8, "full": False}],
  "base": "operai: minimo, contingenza, ITS ÷ 173", "nota": "Limite 250 ore annue, preavviso 48 ore.", "art": "Artt. 22, 57"}
}

META = {
 "sigla": "Edilizia artigianato", "ordine": 39,
 "nome": "CCNL per i dipendenti delle imprese artigiane e delle PMI industriali dell'edilizia e affini (ANAEPA-Confartigianato, CNA Costruzioni, FIAE-Casartigiani, CLAAI; FENEAL-UIL, FILCA-CISL, FILLEA-CGIL)",
 "vigenza": "1/5/2025 - 30/9/2028", "testo": "Testo unico vigente al 10/2/2026", "fonte": "TeleConsul, stampa in Drive (CCNL 2)",
 "dubbi": [
  "Contingenza, ITS ed EVR territoriali non in tabella: il calcolatore usa solo il minimo.",
  "Malattia operai: il calcolatore approssima i coefficienti orari in percentuali.",
  "Preavviso impiegati: «dalla metà o dalla fine del mese» reso come 1° o 16° del mese.",
  "DMP risulta senza dipendenti in anagrafica.",
  "Codice CNEL non riportato nel testo."
 ],
 "regoleJson": REGOLE
}

if __name__ == "__main__":
    write(CC, build(CC, ITEMS), META, sys.argv[1])

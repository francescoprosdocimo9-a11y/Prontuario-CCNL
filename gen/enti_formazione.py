import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import build, write

CC = "formazione-fidef"
LIV = ["I", "II", "III", "IV", "V", "VI s/A", "VI s/B", "VI s/C", "VII", "VIII"]
PB = {"2025-09-01": [1350, 1400, 1430, 1530, 1750, 1820, 1930, 1950, 2000, 2350],
      "2027-09-01": [1420, 1470, 1490, 1590, 1810, 1870, 2000, 2050, 2150, 2450]}
SC = [23, 25, 28, 30, 40, 45, 45, 50, 55, 65]
def eur(x): return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

ITEMS = [
 dict(id="vigenza", s="CCNL per il personale degli enti gestori di corsi di istruzione, formazione e cultura varia aderenti a Fidef (CNEL T279), con Ciu UnionQuadri, Confal Federazione Scuola, Fla e Confal: vale dal 1/9/2025 al 31/8/2028. Testo unico del 24/8/2026 (2ª edizione firmata il 30/8/2026); sostituisce il CCNL del 27/10/2022.",
  p=["Ultrattività fino al rinnovo.", "Piattaforma 6 mesi prima della scadenza; 7 mesi di tregua.", "L'applicazione comporta l'adesione dell'ente a Fidef."],
  art="Art. 24", att="CCNL riservato agli enti aderenti a Fidef: verificare l'adesione.", tag=["vigenza","scadenza","fidef","t279","formazione"]),
 dict(id="codici", s="Codice CNEL T279. Ente bilaterale Ebiefo; Co.As.Co. codice INPS W470.", art="Artt. 76-78", tag=["t279","ebiefo","w470","codice"]),
 dict(id="contrattazione-aziendale", s="Contrattazione aziendale o territoriale con piattaforme 2 mesi prima della scadenza; intese modificative per nuove iniziative o crisi aziendali, trasmesse alle parti nazionali.", art="Artt. 2, 24", tag=["secondo livello","intese modificative"]),
 dict(id="prova", s="Prova scritta: I e II livello 30 giorni, III 60, IV e V 90, VI (s/A, s/B, s/C) 120, VII 150, VIII 190. Recesso con 3 giorni di preavviso; malattia e infortunio la sospendono. Contratti a termine: 1 giorno ogni 15 di calendario, massimo 30; stagionali 5 giorni lavorativi.",
  tab=[["Livello","Prova"],["I e II","30 giorni"],["III","60 giorni"],["IV e V","90 giorni"],["VI s/A, s/B, s/C","120 giorni"],["VII","150 giorni"],["VIII","190 giorni"]], art="Artt. 11-12, 31", tag=["prova"]),
 dict(id="inquadramento", s="Due aree: tecnico-operativa e ausiliare (livelli I-VI s/A) e quadri e dirigenti (VI s/B, VI s/C, VII, VIII). Esempi: I operatore tecnico-ausiliario e di segreteria; IV docente tecnico di laboratorio, responsabile amministrativo; V formatore/docente e tutor; VI s/B docente con coordinamento; VII direttore; VIII dirigente di più sedi.",
  art="Artt. 26-28", tag=["livelli","classificazione","docenti"]),
 dict(id="mansioni", s="Mutamenti di qualifica secondo l'art. 27; il docente con coordinamento didattico (riduzione della docenza fino al 50%) mantiene il V livello ma riceve la retribuzione del VI s/B per il periodo.", art="Art. 27, Allegato 1", tag=["mansioni superiori","coordinamento"]),
 dict(id="apprendistato", s="Apprendistato professionalizzante (18-29 anni) da 12 a 36 mesi: II-IV 24 mesi, V e VI 30, VII 36. Retribuzione in percentuale del livello finale, per semestri: II-IV 75/80/85/90%; V-VI 75/80/85/90/90%; VII 70/75/80/90/90/90%. Part-time minimo 20 ore; formazione fino a 120 ore nel triennio.",
  tab=[["Livello finale","Durata","Prova","Semestri I-VI"],["II-IV","24 mesi","30 giorni","75-80-85-90%"],["V-VI","30 mesi","40 giorni","75-80-85-90-90%"],["VII","36 mesi","60 giorni","70-75-80-90-90-90%"]],
  art="Art. 10", tag=["apprendistato","percentuali"]),
 dict(id="tempo-determinato", s="Contratti a termine secondo il D.Lgs. 81/2015, senza limite percentuale rispetto agli indeterminati. Primo contratto acausale fino a 12 mesi. Nessuna prova in caso di rinnovo. I corsi di insegnamento professionale sono attività stagionale, senza i limiti dei contratti a termine.",
  art="Artt. 11-12", tag=["tempo determinato","stagionali","nessun limite"]),
 dict(id="stagionali", s="Sono stagionali i corsi di insegnamento professionale (D.P.R. 1525/1963) e le attività non programmabili richieste da privati, aziende o istituzioni. Prova massima 5 giorni lavorativi; diritto di precedenza.", art="Art. 12", tag=["stagionali","corsi"]),
 dict(id="part-time", s="Part-time orizzontale, verticale, ciclico (almeno 8 mesi per anno formativo) o misto. Clausole flessibili ed elastiche con preavviso di almeno 2 giorni. Supplementare pagato come ordinario fino all'orario pieno, o con riposi compensativi.",
  art="Artt. 32-33, 50", tag=["part-time","clausole elastiche","supplementare"]),
 dict(id="lavoro-intermittente", s="Lavoro intermittente secondo la legge.", art="Art. 13", tag=["intermittente"]),
 dict(id="somministrazione", s="Somministrazione a tempo determinato secondo la legge.", art="Art. 15", tag=["somministrazione"]),
 dict(id="collaborazioni", voce="Collaborazioni e monte ore", cap="t", s="Il CCNL regola anche co.co.co., autonomi e il contratto a monte ore (M.O.G.). Compenso orario minimo di riferimento: V livello 14,00 € (14,50 dal 1/9/2027), VI 15,60 € (16,00).", art="Artt. 16-18, Allegato 1 tab. 4", tag=["cococo","autonomi","monte ore"]),
 dict(id="orario", s="Non docenti 40 ore settimanali (fino a 48 con lo straordinario); docenti/formatori 32 ore tra insegnamento e attività connesse (monte annuo convenzionale 1.664 ore). Orario multiperiodale fino a 48 ore per 22 settimane, con recupero e banca delle ore.",
  art="Artt. 46-47, Allegato 1", tag=["orario","40 ore","32 ore docenti","banca ore"]),
 dict(id="straordinario", s="Straordinario solo su accordo, fino a 250 ore annue. Maggiorazioni sulla retribuzione oraria di fatto: 20% feriale, 30% festivo o domenicale, 35% notturno (22-7, esclusi i turni regolari). Non cumulabili.",
  tab=[["Tipo","Maggiorazione"],["Straordinario feriale","20%"],["Festivo o domenicale","30%"],["Notturno (22-7)","35%"]], art="Art. 50", tag=["straordinario","250 ore","maggiorazioni"]),
 dict(id="festivita", s="12 festività compreso il Patrono (se lavorato: permesso, ferie aggiuntive o 1/26). Per le festività soppresse 4 giorni di permesso retribuito l'anno; festività di domenica pagate una giornata o trasformate in riposo o banca ore.", art="Artt. 51-52", tag=["festività","festività soppresse","patrono"]),
 dict(id="ferie", s="26 giorni lavorativi l'anno, frazionabili. La sospensione dei corsi o l'inattività della scuola si computa come ferie. In dodicesimi nell'anno di assunzione o cessazione (frazione oltre 15 giorni = mese).", art="Art. 51", att="La sospensione dei corsi conta come ferie: verificare come viene gestita nel cedolino.", tag=["ferie","26 giorni"]),
 dict(id="permessi-rol", s="Nessun ROL: spettano 4 giorni di permesso per le festività soppresse, più 30 minuti per ogni settimana oltre l'orario nel regime multiperiodale.", art="Artt. 47, 52", tag=["permessi","festività soppresse","rol"]),
 dict(id="congedo-matrimoniale", s="15 giorni consecutivi di calendario non frazionabili, richiesti con almeno 30 giorni di anticipo; se si sovrappone alle ferie, queste vanno spostate.", art="Artt. 54 C, 57", tag=["matrimonio","congedo matrimoniale"]),
 dict(id="minimi", s="Retribuzione tabellare mensile (contingenza conglobata) per 13 mensilità, con aumento dal 1/9/2027. Dal 1/9/2025: I 1.350 €, III 1.430 €, IV 1.530 €, V 1.750 €.",
  tab=[["Livello","1/9/2025","1/9/2027"]] + [[l, eur(PB["2025-09-01"][i]), eur(PB["2027-09-01"][i])] for i, l in enumerate(LIV)], art="Artt. 36, 39-40, Allegato 1", tag=["minimi","paga base","tabelle"]),
 dict(id="divisori", s="Giornaliera ÷ 26. Oraria ÷ 173 (40 ore) per tutti, ÷ 139 per i docenti e formatori a 32 ore (IV docente tecnico, V, VI).", art="Allegato 1", tag=["divisore","173","139","26"]),
 dict(id="mensilita-aggiuntive", s="Solo 13ª, pagata entro il 24 dicembre, pari a una mensilità di fatto; in dodicesimi con frazione oltre 15 giorni come mese. Con variazioni di orario si usa la media ponderata delle ore.", art="Art. 38", tag=["tredicesima","13 mensilità"]),
 dict(id="scatti", s="4 incrementi quadriennali presso lo stesso ente, dal mese successivo alla maturazione: I 23 €, II 25, III 28, IV 30, V 40, VI s/A e s/B 45, VI s/C 50, VII 55, VIII 65. Riassorbiti nel passaggio di livello.",
  tab=[["Livello","Importo"]] + [[l, eur(v)] for l, v in zip(LIV, SC)], art="Art. 36, Allegato 1 tab. 3", tag=["scatti","quadriennali"]),
 dict(id="pagamento", s="Retribuzione entro il 7 del mese successivo; il prospetto paga indica il codice CNEL del CCNL.", art="Artt. 36-37", tag=["pagamento","busta paga"]),
 dict(id="indennita-varie", s="Indennità di cassa 3% della paga base; lavoro fuori sede mezz'ora per ogni spostamento; commissioni d'esame 30 € al giorno (gettone minimo 60 € per membri esterni non retribuiti). Attività non didattiche convertite in ore di docenza (esaminatore 1,5, riunioni 0,5…).", art="Art. 41, Allegato 1", tag=["indennità di cassa","fuori sede","commissioni"]),
 dict(id="trasferta", s="Rimborso spese di viaggio, vitto e alloggio documentate e indennità dell'Allegato 1; ridotta del 10% per trasferte oltre il mese o abituali.", art="Art. 42", tag=["trasferta","rimborso"]),
 dict(id="allineamento", voce="Allineamento da altro CCNL", cap="r", s="Chi proviene da un altro CCNL viene reinquadrato secondo le mansioni senza ridurre la retribuzione annua lorda: la differenza diventa superminimo ad personam assorbibile da scatti, passaggi di livello o rinnovi.", art="Art. 45", tag=["allineamento","superminimo","cambio ccnl"]),
 dict(id="ratei", s="13ª e ferie in dodicesimi, frazione oltre 15 giorni = mese intero.", art="Artt. 38, 51", tag=["ratei","dodicesimi"]),
 dict(id="malattia-trattamento", s="Integrazione al 100% della retribuzione netta del mese precedente, dal 1° giorno, per massimo 180 giorni nell'anno solare. Giorni di terapie salvavita esclusi dal comporto e pagati per intero.", art="Art. 54 E", att="Integrazione al 100% del netto: nel calcolatore approssimata al 100% lordo.", tag=["malattia","100%","carenza"]),
 dict(id="malattia-comporto", s="Comporto di 180 giorni per assenza continuativa (anche a cavallo di due anni) e 365 giorni per più assenze nell'arco di 3 anni. Dopo, aspettativa non retribuita fino a 6 mesi (art. 54) o 120 giorni (art. 56), su richiesta con certificato; patologie particolari 270 giorni + 8 mesi.", art="Artt. 54, 56", att="Artt. 54 e 56 indicano durate dell'aspettativa diverse (6 mesi o 120 giorni).", tag=["comporto","180 giorni","365 giorni","aspettativa"]),
 dict(id="infortunio", s="Infortunio sul lavoro: il datore paga il 100% il giorno dell'evento e il 60% nei 3 giorni successivi; poi indennità INAIL (60% fino al 90° giorno, 75% dopo) con l'integrazione al 100% dell'art. 54.", art="Art. 55", tag=["infortunio","inail"]),
 dict(id="maternita", s="Maternità e paternità secondo il D.Lgs. 151/2001; flessibilità del congedo (1 mese prima e 4 dopo il parto).", art="Artt. 54 D, 58", tag=["maternità","paternità"]),
 dict(id="aspettative", s="Aspettativa non retribuita per gravi motivi di salute propri o dei familiari: 15 giorni per anno di anzianità fino a 6 mesi, prorogabile del 50%. Mancato rientro entro 3 giorni = dimissioni. Aspettative per formazione fino a 2 anni.", art="Artt. 56, 60-61", tag=["aspettativa","non retribuita"]),
 dict(id="disciplinare", s="Rimprovero verbale, rimprovero scritto, multa fino a 4 ore di retribuzione base (destinata a fini assistenziali), sospensione fino a 10 giorni, licenziamento. Codice disciplinare nell'Allegato 2.", art="Art. 68, Allegato 2", tag=["disciplinare","sanzioni","multa"]),
 dict(id="preavviso", s="Preavviso uguale per licenziamento e dimissioni, dal giorno dopo la ricezione (fino a 3 anni / 3-10 anni / oltre 10): VI-VIII 2/3/4 mesi; IV-V 1 mese e 15 giorni / 2 mesi / 2 mesi e 15 giorni; II-III 10/20 giorni/1 mese; I 7/15/30 giorni.",
  tab=[["Livello","Fino a 3 anni","3-10 anni","Oltre 10 anni"],["VI, VII e VIII","2 mesi","3 mesi","4 mesi"],["IV e V","1 mese e 15 giorni","2 mesi","2 mesi e 15 giorni"],["II e III","10 giorni","20 giorni","1 mese"],["I","7 giorni","15 giorni","30 giorni"]],
  art="Art. 71", tag=["preavviso","licenziamento","dimissioni"]),
 dict(id="tfr", s="TFR secondo la L. 297/1982, escludendo rimborsi di missione, ferie non godute monetizzate e assegni familiari; anticipazioni secondo l'Allegato.", art="Art. 72", tag=["tfr","anticipazione"]),
 dict(id="ente-bilaterale", s="Ebiefo: 0,60% dell'imponibile previdenziale (0,36% azienda, 0,24% lavoratore). Se non versato: EDR pari alla quota azienda, con dicitura «mancata adesione all'Ente Bilaterale del contratto» (non dovuto finché l'ente non è operativo). Co.As.Co. 0,10% della paga di fatto a carico azienda (codice W470): chi non lo versa non può applicare il CCNL.",
  tab=[["Voce","Azienda","Lavoratore"],["Ebiefo","0,36%","0,24%"],["Co.As.Co. (W470)","0,10%","—"]], art="Artt. 76-78", tag=["ebiefo","coasco","w470","edr"]),
 dict(id="sanita", s="Fondo di assistenza sanitaria integrativa da individuare durante la vigenza, per indeterminati, apprendisti e determinati oltre 6 mesi; contributi soggetti solo al contributo di solidarietà del 10%.", art="Art. 76", tag=["sanità integrativa","fondo"]),
 dict(id="diritti-sindacali", s="Permessi sindacali retribuiti (30 ore annue per i dirigenti dei comitati), assemblee, affissioni, trattenuta sindacale su delega.", art="Artt. 3-7", tag=["permessi sindacali","assemblea"]),
 dict(id="lavoro-agile", s="Telelavoro, lavoro agile e didattica a distanza con accordo individuale.", art="Art. 19", tag=["lavoro agile","didattica a distanza"]),
 dict(id="riepilogo-costi", s="13 mensilità; Ebiefo 0,36% e Co.As.Co. 0,10% a carico azienda; 4 scatti quadriennali; nessuna 14ª.", art="Artt. 36-38, 77-78", tag=["costi"]),
]

REGOLE = {
 "nome": "Enti di formazione Fidef",
 "livelli": LIV, "livelloDefault": "V",
 "gruppi": [{"nome": "I", "livelli": ["I"]}, {"nome": "II e III", "livelli": ["II", "III"]}, {"nome": "IV e V", "livelli": ["IV", "V"]}, {"nome": "VI, VII e VIII", "livelli": LIV[5:]}],
 "preavviso": {"fasce": [{"finoAnni": 3, "label": "fino a 3 anni"}, {"finoAnni": 10, "label": "da 3 a 10 anni"}, {"finoAnni": None, "label": "oltre 10 anni"}],
  "lic": [[{"g": 7}, {"g": 10}, {"m": 1, "g": 15}, {"m": 2}], [{"g": 15}, {"g": 20}, {"m": 2}, {"m": 3}], [{"g": 30}, {"m": 1}, {"m": 2, "g": 15}, {"m": 4}]],
  "dim": [[{"g": 7}, {"g": 10}, {"m": 1, "g": 15}, {"m": 2}], [{"g": 15}, {"g": 20}, {"m": 2}, {"m": 3}], [{"g": 30}, {"m": 1}, {"m": 2, "g": 15}, {"m": 4}]],
  "lavorativi": False, "decorrenza": "giorno-successivo", "nota": "Decorre dal giorno successivo alla ricezione; uguale per licenziamento e dimissioni.", "art": "Art. 71"},
 "prova": {"livelli": {"I": {"g": 30, "txt": "30 giorni"}, "II": {"g": 30, "txt": "30 giorni"}, "III": {"g": 60, "txt": "60 giorni"}, "IV": {"g": 90, "txt": "90 giorni"}, "V": {"g": 90, "txt": "90 giorni"},
   "VI s/A": {"g": 120, "txt": "120 giorni"}, "VI s/B": {"g": 120, "txt": "120 giorni"}, "VI s/C": {"g": 120, "txt": "120 giorni"}, "VII": {"g": 150, "txt": "150 giorni"}, "VIII": {"g": 190, "txt": "190 giorni"}},
  "nota": "Sospesa da malattia e infortunio; tempo determinato massimo 30 giorni.", "art": "Art. 31"},
 "scatti": {"anni": 4, "max": 4, "imp": dict(zip(LIV, SC)), "decorrenza": "mese-successivo", "nota": "4 incrementi quadriennali presso lo stesso ente.", "art": "Allegato 1 tab. 3"},
 "minimi": [{"dal": d, "v": dict(zip(LIV, v))} for d, v in PB.items()],
 "minimiNota": "Retribuzione tabellare con contingenza conglobata.",
 "mensilita": 13, "divOra": 173, "divGiorno": 26,
 "fraz": {"giorni": 15, "op": ">"},
 "aggiuntive": [{"nome": "13ª", "meseInizio": 1}],
 "ferie": {"giorni": 26, "txt": "26 giorni lavorativi"},
 "permessi": [{"label": "4 giorni per festività soppresse (32 ore)", "ore": 32}],
 "ratei": {"nota": "Frazioni oltre 15 giorni = mese intero.", "art": "Artt. 38, 51"},
 "comporto": {"tipo": "mesi", "mesi": 36, "fasce": [{"finoAnni": None, "giorni": 365}], "separaInfortunio": False,
  "nota": "365 giorni nell'arco di 3 anni per assenze anche non continuative; 180 giorni per un'unica assenza continuativa.", "art": "Art. 54"},
 "malattia": {"casi": [{"nome": "Malattia", "inps": True, "fasce": [{"dal": 1, "al": 180, "tot": 100}]}],
  "nota": "Integrazione al 100% della retribuzione netta del mese precedente dal 1° giorno, per 180 giorni nell'anno solare.", "art": "Art. 54"},
 "straord": {"voci": [{"l": "Straordinario feriale", "m": 20, "full": True}, {"l": "Straordinario festivo o domenicale", "m": 30, "full": True}, {"l": "Lavoro notturno (22-7)", "m": 35, "full": True}],
  "base": "retribuzione di fatto ÷ 173 (docenti ÷ 139)", "nota": "Fino a 250 ore annue; maggiorazioni non cumulabili.", "art": "Art. 50"}
}

META = {
 "sigla": "Enti formazione Fidef", "ordine": 42,
 "nome": "CCNL personale degli enti gestori di corsi di istruzione, formazione e cultura varia (Fidef; Ciu UnionQuadri, Confal, Fla)",
 "vigenza": "1/9/2025 - 31/8/2028", "testo": "Testo unico del 24/8/2026, 2ª edizione firmata il 30/8/2026 (CNEL T279)", "fonte": "Testo Fidef in Drive (CCNL 2)",
 "dubbi": [
  "Aspettativa dopo il comporto: l'art. 54 indica 6 mesi, l'art. 56 120 giorni.",
  "Comporto doppio: 180 giorni continuativi e 365 nel triennio; il calcolatore usa il secondo.",
  "Divisore orario 139 per i docenti a 32 ore: il calcolatore usa 173.",
  "Ebiefo: EDR sostitutivo non dovuto finché l'ente non è operativo; verificare lo stato."
 ],
 "regoleJson": REGOLE
}

if __name__ == "__main__":
    write(CC, build(CC, ITEMS), META, sys.argv[1])

"""Regole del calcolatore infortunio per ogni CCNL.

Giorni contati dal giorno successivo all'infortunio (1 = primo giorno dopo l'evento).
Il giorno dell'infortunio è pagato per intero dal datore (art. 73 DPR 1124/1965).
fasce: tot = percentuale complessiva garantita (INAIL + datore) della retribuzione giornaliera;
       al = None = fino alla guarigione. Dove nessuna fascia copre un giorno vale la legge:
       60% a carico del datore nei 3 giorni di carenza, poi la sola indennità INAIL.
coeff: integrazione degli operai edili = k x paga oraria x (orario settimanale / 7) al giorno.
comporto.tipo: escluso (non conta nel comporto di malattia), separato (limite proprio), unico (sommato alla malattia).
"""
import json, sys, os

F = lambda dal, al, tot: {"dal": dal, "al": al, "tot": tot}
CAR60 = F(1, 3, 60)
ESCLUSO = lambda txt="Posto conservato fino alla guarigione clinica; l'infortunio non conta nel comporto di malattia.": {"tipo": "escluso", "txt": txt}
UNICO180 = {"tipo": "unico", "txt": "Comporto unico con la malattia: 180 giorni nell'anno solare, sommando gli eventi."}

INF = {
 "commercio": {"casi": [{"nome": "Lavoratori", "fasce": [CAR60, F(4, 19, 90), F(20, None, 100)]},
                        {"nome": "Apprendisti", "fasce": [CAR60, F(4, 19, 80), F(20, None, 90)]}],
   "base": "netto", "comporto": {"tipo": "separato", "txt": "Comporto di 180 giorni distinto da quello per malattia; poi aspettativa non retribuita per la durata dell'inabilità (art. 198)."},
   "nota": "Il testo conta come 1° giorno quello dell'evento: 90% dal 5° al 20° giorno, 100% dal 21°. Se l'INAIL non paga, il datore non integra.", "art": "Artt. 192-193, 198"},
 "metalmeccanica": {"casi": [{"nome": "Anzianità fino a 3 anni", "fasce": [F(1, 183, 100)]}, {"nome": "Anzianità da 3 a 6 anni", "fasce": [F(1, 274, 100)]}, {"nome": "Anzianità oltre 6 anni", "fasce": [F(1, 365, 100)]}],
   "base": "netto", "comporto": ESCLUSO(), "nota": "Integrazione fino al normale trattamento netto per la durata del comporto breve; oltre resta la sola indennità INAIL.", "art": "Sez. IV, Tit. VI, art. 1"},
 "abbigliamento-pmi": {"casi": [{"nome": "Infortunio sul lavoro o malattia professionale", "fasce": [F(1, None, 100)]}], "base": "netto", "comporto": ESCLUSO(),
   "nota": "Integrazione dal primo giorno di assenza fino alla guarigione clinica, al 100% della retribuzione netta normale di fatto, se l'INAIL riconosce l'evento.", "art": "Art. 52"},
 "acconciatura": {"casi": [{"nome": "Infortunio sul lavoro", "fasce": [F(1, None, 100)]}], "base": "netto",
   "comporto": {"tipo": "separato", "txt": "Posto conservato fino alla guarigione clinica; comporto separato da quello della malattia."},
   "nota": "Integrazione fino al 100% della retribuzione normale di fatto netta, anche durante la prova.", "art": "Art. 31"},
 "agenzie-viaggio": {"casi": [{"nome": "Infortunio sul lavoro", "fasce": [CAR60]}], "base": "lordo", "comporto": UNICO180,
   "nota": "Il CCNL non prevede integrazione dell'indennità INAIL. Ai lavoratori a tempo indeterminato il datore anticipa l'indennità e ne chiede il rimborso.", "art": "Artt. 165-169"},
 "autorimesse": {"casi": [{"nome": "Infortunio sul lavoro", "fasce": [F(1, None, 100)]}], "base": "lordo", "comporto": ESCLUSO(),
   "nota": "Integrazione al 100% della retribuzione globale dal primo giorno alla guarigione, carenza compresa.", "art": "Art. 60"},
 "ced": {"casi": [{"nome": "Infortunio sul lavoro", "fasce": [CAR60, F(4, None, 75)]}], "base": "netto",
   "comporto": {"tipo": "unico", "txt": "Comporto unico con la malattia: 180 giorni nell'anno solare, più 120 giorni di aspettativa."},
   "nota": "L'art. 147 scrive «75% (cento per cento)»: cifra e lettere non coincidono, verifica. Se l'INAIL non paga, il datore non integra.", "art": "Artt. 144-150"},
 "edilizia-artigianato": {"casi": [{"nome": "Operai", "coeff": [{"dal": 1, "al": 90, "k": 0.2538}, {"dal": 91, "al": None, "k": 0.0574}]},
                                   {"nome": "Impiegati (come la malattia)", "fasce": [F(1, 180, 100)]}],
   "base": "lordo", "comporto": ESCLUSO("Operai: posto conservato per tutta l'inabilità temporanea. Impiegati: fino al certificato di guarigione."),
   "nota": "Operai: l'impresa paga ogni giorno indennizzato (domeniche comprese) la paga oraria (minimo, indennità territoriale, contingenza) × coefficiente × orario settimanale ÷ 7. Il giorno dell'infortunio i riposi annui (4,95%) sono pagati per intero, nei 3 giorni successivi al 60%. Impiegati: trattamento della malattia (art. 66) e 50% oltre i limiti.", "art": "Artt. 28, 67"},
 "edilizia-industria": {"casi": [{"nome": "Operai", "coeff": [{"dal": 1, "al": 90, "k": 0.2538}, {"dal": 91, "al": None, "k": 0.0574}]},
                                 {"nome": "Impiegati (come la malattia)", "fasce": [F(1, 183, 100), F(184, None, 50)]}],
   "base": "lordo", "comporto": ESCLUSO("Operai: posto conservato fino alla fine dell'inabilità. Impiegati: fino a guarigione o stabilizzazione clinica."),
   "nota": "Operai: l'impresa paga ogni giorno indennizzato (domeniche comprese) la paga oraria × coefficiente × orario settimanale ÷ 7; in più accantonamento Cassa Edile. Impiegati: trattamento della malattia (durata del 100% secondo l'anzianità) e 50% oltre i limiti.", "art": "Artt. 27, 67; Allegati D, E"},
 "formazione-fidef": {"casi": [{"nome": "Infortunio sul lavoro", "fasce": [CAR60, F(4, 180, 100)]}], "base": "netto",
   "comporto": {"tipo": "unico", "txt": "Comporto di 180 giorni per assenza continuativa e 365 nel triennio (art. 54)."},
   "nota": "Integrazione al 100% della retribuzione netta (art. 54) per massimo 180 giorni nell'anno solare.", "art": "Artt. 54-55"},
 "impianti-sportivi": {"casi": [{"nome": "Lavoratori", "fasce": [CAR60, F(4, 19, 90), F(20, None, 100)]},
                                {"nome": "Apprendisti", "fasce": [CAR60, F(4, 19, 80), F(20, None, 90)]}],
   "base": "netto", "comporto": {"tipo": "separato", "txt": "Posto conservato per 180 giorni, più aspettativa non retribuita fino a 120 giorni."},
   "nota": "Refuso nel testo: il 4° giorno non è disciplinato; il calcolatore applica il 90% dal 4° giorno. Se l'INAIL non paga, il datore non integra.", "art": "Artt. 104-108"},
 "legno-artigianato": {"casi": [{"nome": "Infortunio sul lavoro", "fasce": [F(1, None, 100)]}], "base": "netto", "comporto": ESCLUSO(),
   "nota": "Integrazione fino al 100% della retribuzione netta dal primo giorno alla guarigione clinica, per operai e impiegati.", "art": "Art. 49; Art. 55 p. 13"},
 "logistica-trasporto-merci": {"casi": [{"nome": "Sezione I, anzianità fino a 5 anni (come la malattia)", "fasce": [F(1, 90, 100), F(91, 240, 50)]},
                                        {"nome": "Sezione I, anzianità oltre 5 anni (come la malattia)", "fasce": [F(1, 150, 100), F(151, 360, 50)]},
                                        {"nome": "Sezione II e soci di cooperativa (art. 77)", "fasce": [F(1, 1, 100), F(2, 4, 90), F(5, None, 100)]}],
   "base": "netto", "comporto": ESCLUSO("Posto conservato per tutta l'inabilità riconosciuta dall'INAIL; l'infortunio non conta nel comporto."),
   "nota": "Sezione I: trattamento complessivo come la malattia. Sezione II e cooperative: integrazione (carenza compresa) al 100%, 90% dal 2° al 4° giorno e 100% dal 5°.", "art": "Artt. 63 B), 77"},
 "metalmeccanica-anpit": {"casi": [{"nome": "Infortunio sul lavoro o malattia professionale", "fasce": [CAR60, F(4, 90, 75)]},
                                   {"nome": "Infortunio in itinere", "fasce": [CAR60]}],
   "base": "lordo", "comporto": {"tipo": "escluso", "txt": "Conservazione del posto secondo l'art. 198; in itinere come la malattia non professionale."},
   "nota": "Dal 4° al 90° giorno il datore aggiunge il 15% della retribuzione giornaliera normale all'indennità INAIL (60%); dal 91° solo INAIL (75%). Nessuna integrazione per l'infortunio in itinere.", "art": "Art. 198"},
 "metalmeccanica-confapi": {"casi": [{"nome": "Anzianità fino a 3 anni", "fasce": [F(1, 183, 100)]}, {"nome": "Anzianità da 3 a 6 anni", "fasce": [F(1, 274, 100)]}, {"nome": "Anzianità oltre 6 anni", "fasce": [F(1, 365, 100)]}],
   "base": "netto", "comporto": ESCLUSO(),
   "nota": "Integrazione fino al normale trattamento netto per un periodo pari a quello previsto per la malattia (art. 55, punto 3); oltre, sola indennità INAIL. Durate da verificare sul testo.", "art": "Art. 54"},
 "operai-agricoli": {"casi": [{"nome": "Florovivaisti (a carico del datore)", "fasce": [CAR60, F(4, 180, 100)]},
                              {"nome": "Operai agricoli (Cassa extra legem)", "fasce": [CAR60]}],
   "base": "lordo", "comporto": ESCLUSO("Posto conservato fino a guarigione, massimo 15 mesi."),
   "nota": "Agricoli: l'integrazione all'80% e poi al 100% la paga la Cassa extra legem provinciale, non il datore. Florovivaisti: integrazione al 100% dal 4° giorno per 180 giorni.", "art": "Artt. 61-63"},
 "oreficeria-industria": {"casi": [{"nome": "Anzianità fino a 5 anni", "fasce": [F(1, 61, 100), F(62, 183, 75)]}, {"nome": "Anzianità da 5 a 10 anni", "fasce": [F(1, 91, 100), F(92, 244, 75)]}, {"nome": "Anzianità oltre 10 anni", "fasce": [F(1, 122, 100), F(123, 305, 75)]}],
   "base": "netto", "comporto": ESCLUSO(),
   "nota": "Integrazione fino al trattamento netto che sarebbe spettato per la malattia di pari durata (100% e poi 75%); oltre, sola indennità INAIL.", "art": "Art. 34 Disciplina comune"},
 "portieri": {"casi": [{"nome": "Infortunio sul lavoro", "fasce": [CAR60]}], "base": "lordo", "comporto": {"tipo": "nessuno", "txt": "Il CCNL non prevede un comporto specifico per l'infortunio."},
   "nota": "Nessuna integrazione dell'indennità INAIL. Dagli infortuni dell'1/1/2026 il datore anticipa l'indennità per conto dell'INAIL. Festività durante l'infortunio: una giornata al netto di quanto paga l'INAIL.", "art": "Artt. 35, 79, 104, 112"},
 "pubblici-esercizi": {"casi": [{"nome": "Pubblici esercizi e ristorazione", "fasce": [CAR60, F(4, None, 100)]}, {"nome": "Stabilimenti balneari e alberghi diurni", "fasce": [F(1, None, 100)]}],
   "base": "lordo", "comporto": UNICO180,
   "nota": "Il testo prevede sia il 60% nei 3 giorni di carenza sia l'integrazione al 100% «sin dal giorno dell'infortunio»: verifica se la carenza va integrata al 100%. L'integrazione spetta solo se l'INAIL paga.", "art": "Artt. 191-194, 251, 267"},
 "pulizia": {"casi": [{"nome": "Operai", "fasce": [F(1, None, 100)]}, {"nome": "Impiegati (come la malattia)", "fasce": [F(1, 150, 100), F(151, 360, 50)]}],
   "base": "lordo", "comporto": {"tipo": "nessuno", "txt": "Il CCNL non fissa un comporto specifico per l'infortunio sul lavoro."},
   "nota": "Operai: 100% della retribuzione globale dal giorno successivo all'infortunio alla guarigione. Impiegati: trattamento della malattia (100% per 5 mesi, 50% per altri 7).", "art": "Artt. 41, 51"},
 "studi-professionali": {"casi": [{"nome": "Infortunio sul lavoro", "fasce": [CAR60, F(4, None, 75)]}], "base": "lordo",
   "comporto": {"tipo": "separato", "txt": "Comporto per infortunio di 180 giorni, distinto da quello per malattia."},
   "nota": "Dal giorno successivo alla carenza il datore integra l'INAIL fino al 75% della retribuzione media giornaliera. Vale anche per gli apprendisti.", "art": "Artt. 122-126"},
 "terziario-cnai": {"casi": [{"nome": "Infortunio sul lavoro o malattia professionale", "fasce": [F(1, 3, 70), F(4, 90, 80), F(91, None, 90)]}], "base": "lordo", "comporto": ESCLUSO(),
   "nota": "100% il giorno dell'evento, 70% nei 3 giorni successivi, 80% dal 4° al 90° e 90% dal 91° alla guarigione. In itinere: come la malattia.", "art": "Art. 63"},
 "turismo-catene": {"casi": [{"nome": "Infortunio sul lavoro", "fasce": [CAR60]}], "base": "lordo", "comporto": UNICO180,
   "nota": "Nessuna integrazione oltre la carenza. Ai lavoratori a tempo indeterminato il datore anticipa l'indennità INAIL e ne chiede il rimborso.", "art": "Artt. 124-127"},
 "turismo-cifa": {"casi": [{"nome": "Infortunio sul lavoro (anche in itinere)", "fasce": [F(1, None, 100)]}], "base": "netto", "comporto": ESCLUSO(),
   "nota": "Integrazione aziendale fino al normale trattamento economico complessivo netto; vale anche per l'infortunio in itinere, non per il rischio elettivo.", "art": "Art. 54"},
 "turismo-confesercenti": {"casi": [{"nome": "Pubblici esercizi", "fasce": [CAR60, F(4, None, 100)]}, {"nome": "Alberghi, campeggi e altri comparti", "fasce": [CAR60]}],
   "base": "lordo", "comporto": UNICO180,
   "nota": "Nei pubblici esercizi il datore integra l'INAIL fino al 100%; negli altri comparti paga solo giorno dell'infortunio e carenza.", "art": "Artt. 170-172"},
}
for v in INF.values(): v.setdefault("giorno", 100)

HARD = ("commercio", "metalmeccanica")

if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]          # cartella con ccnl/<id>.json letti dal db, cartella di output
    os.makedirs(out, exist_ok=True)
    writes = []
    for cc, rule in sorted(INF.items()):
        if cc in HARD: continue
        d = json.load(open(f"{src}/{cc}.json")); d = d.get("data", d)
        R = json.loads(d["regoleJson"]); R["infortunio"] = rule
        p = f"{out}/inf-{cc}.json"
        json.dump({"regoleJson": json.dumps(R, ensure_ascii=False)}, open(p, "w"), ensure_ascii=False)
        writes.append({"op": "update", "collection": "ccnl", "doc_id": cc, "file_path": p, "if_version": 1})
    json.dump(writes, open(f"{out}/batch-infortunio.json", "w"), indent=0)
    print(len(writes), "aggiornamenti")
    print("const INF_HARD = " + json.dumps({k: INF[k] for k in HARD}, ensure_ascii=False, separators=(",", ":")) + ";", file=open(f"{out}/inf-hard.js", "w"))

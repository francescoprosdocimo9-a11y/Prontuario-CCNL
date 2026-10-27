"""Pubblici esercizi Confesercenti: CCNL derivato dal Turismo Confesercenti con le tabelle TeleConsul
«Pubblici esercizi (Confesercenti) (agg. ipotesi)», stampa del 27/10/2026.
Uso: python3 -I gen/pe_confesercenti.py <cartella con ccnl/ e schede/ del Turismo Confesercenti> data"""
import json, os, sys, copy

SRC, OUT = sys.argv[1], sys.argv[2]
ID, OLD = "pe-confesercenti", "turismo-confesercenti"
FONTE = "TeleConsul, Pubblici esercizi (Confesercenti) agg. ipotesi, stampa del 27/10/2026"
ORIG = "Copiata dal Turismo Confesercenti e aggiornata con le tabelle TeleConsul dei pubblici esercizi: da verificare"
NOW = "2026-10-27T12:00:00+01:00"

def load(p):
    d = json.load(open(p, encoding="utf-8"))
    return d.get("data", d)

LIV = ["A", "B", "1", "2", "3", "4", "5", "6S", "6", "7"]
# vigente dal 1/6/2026 al 31/5/2027: minimo, contingenza, totale (Quadri con indennità di funzione a parte)
TAB = {"A": (1920.26, 542.70, 75), "B": (1734.02, 537.59, 70), "1": (1570.97, 536.71, 0), "2": (1384.76, 531.59, 0),
       "3": (1272.47, 528.26, 0), "4": (1167.75, 524.94, 0), "5": (1057.72, 522.37, 0), "6S": (994.19, 520.64, 0),
       "6": (971.06, 520.51, 0), "7": (871.75, 518.45, 0)}
APP = [  # (figura, livello, [(da, a, totale)])
    ("Artigiano", "2", [(1, 12, "1.533,08"), (13, 24, "1.628,90"), (25, 36, "1.724,71"), (37, 48, "1.820,53")]),
    ("Artigiano", "3", [(1, 12, "1.440,59"), (13, 24, "1.530,62"), (25, 36, "1.620,65"), (37, 48, "1.710,70")]),
    ("Artigiano", "4", [(1, 12, "1.354,15"), (13, 24, "1.438,79"), (25, 36, "1.523,42"), (37, 42, "1.608,05")]),
    ("Professionalizzante", "2", [(1, 12, "1.533,08"), (13, 24, "1.628,90"), (25, 36, "1.724,71")]),
    ("Professionalizzante", "3", [(1, 12, "1.440,59"), (13, 24, "1.530,62"), (25, 36, "1.620,65")]),
    ("Professionalizzante", "4", [(1, 12, "1.354,15"), (13, 24, "1.438,79"), (25, 36, "1.523,42")]),
    ("Professionalizzante", "5", [(1, 12, "1.264,08"), (13, 24, "1.343,07"), (25, 36, "1.422,08")]),
    ("Professionalizzante", "6S", [(1, 12, "1.211,86"), (13, 24, "1.287,60"), (25, 36, "1.363,35")]),
    ("Professionalizzante", "6", [(1, 12, "1.193,26"), (13, 24, "1.267,83")]),
]
EXTRA = [("4", "16,74"), ("5", "15,93"), ("6S", "15,26"), ("6", "15,07"), ("7", "14,10")]
MANS = """6S|Addetto ai servizi mensa (almeno 15 anni di servizio)
6|Addetto ai servizi mensa con meno di un anno di anzianità
5|Addetto al caricamento dei distributori di cibo e bevande
6|Addetto al confezionamento di buffet stazione e pasticceria
5|Addetto al controllo accessi di sede o filiale
5|Addetto al prelievo o versamento denaro distributori cibi e bevande
5|Addetto alla movimentazione, allestimento e disallestimento (banqueting e catering)
5|Addetto alla sicurezza
5|Addetto alla sicurezza nei locali notturni, sale da ballo e simili
6|Addetto alla stiratura
4|Addetto all'attività di movimentazione, allestimento e disallestimento (banqueting e catering)
4|Addetto all'attività di produzione di pasti (banqueting e catering)
3|Addetto amministrazione e controllo
6|Addetto consegne con o senza mezzi di locomozione
6|Addetto di lavanderia
6|Addetto servizi mensa (meno di 15 mesi di anzianità nel settore)
6|Aiutante pista catering
5|Allestitore catering
2|Analista programmatore CED
1|Analista sistemista
2|Assistente di direzione
3|Assistente o vice o aiuto supervisore catering
1|Assistente senior di direzione
5|Autista di pista catering
5|Banconiere di gelateria, pasticceria
5|Banconiere di tavola calda, chiosco di stazione
5|Barista
4|Barman
3|Barman unico
6|Caffettiere non barista
4|Cameriere (banqueting e catering)
4|Cameriere ai vini, antipasti, trinciatore
5|Cameriere bar, tavola calda, self-service
4|Cameriere di ristorante
5|Cantiniere
4|Cantiniere e caffettiere
A|Capo area di catena di esercizi
2|Capo banconiere di pasticceria
2|Capo barista - responsabile banco bar
2|Capo CED
2|Capo contabile
2|Capo cuoco p.e. e ristorazione collettiva
B|Capo del personale
4|Capo gruppo mensa
2|Capo laboratorio
2|Capo laboratorio gelateria (ex capo gelatiere)
2|Capo laboratorio pasticceria
3|Capo mensa surgelati e/o precotti
3|Capo operaio
3|Capo reparto catering
A|Capo servizi amministrativi catering
1|Capo servizio catering
2|Capo ufficio catering
6|Caricatore catering
5|Carrellista di stazione o addetto vendita alle banchine
5|Cassiera mensa aziendale con funzioni di esazione
2|Cassiere centrale catering
5|Cassiere risto-bar, self-service, tavola calda, pasticceria, gelateria
5|Cellista surgelati o precotti
5|Centralinista
4|Centralinista con conoscenza di lingua estera
4|Chef de rang di ristorante
6|Commis di bar (ex aiuto barista)
6S|Commis di cucina, sala e piani, bar, diplomato
6|Commis di cucina, sala, bar, tavola calda, self service (ex aiuti in genere)
6|Commis di cucina, sala, tavola calda, self service
5|Conducente automezzi leggeri
5|Conducente automezzi leggeri (banqueting e catering)
4|Conducente automezzi pesanti
7|Conducente di motocicli
4|Conducente mezzi leggeri (banqueting e catering)
6|Confezionatrice di buffet stazione e pasticceria
3|Controllo amministrativo
5|Controllo merci
4|Cuoco capo partita
4|Cuoco di cucina non organizzata in partite
3|Cuoco unico
5|Dattilografo
5|Demi chef de rang dove il servizio di sala è organizzato in ranghi
2|Dietologo
3|Dietologo
A|Direttore
2|Direttore servizio mensa o capo impianto mensa
5|Dispensiere
B|Economo responsabile del settore acquisti
4|Gastronomo
4|Gelatiere
A|Gerente
6|Guardarobiera clienti (vestiarista)
5|Guardarobiera non consegnataria
5|Guardia giurata
6|Guardiano notturno
5|Impiegato d'ordine
4|Impiegato d'ordine con autonomia esecutiva
1|Ispettore amministrativo catena d'esercizi
2|Ispettore mensa
6|Lavandaia
7|Lavoratore catering
5|Magazziniere comune
2|Magazziniere consegnatario o economo
3|Maitre
4|Operaio specializzato alla riparazione di distributori di cibi e bevande
5|Operaio qualificato
4|Operaio specializzato
3|Operaio specializzato provetto
4|Operatore CED - consollista
5|Operatore della ristorazione commerciale in catena
5|Operatore macchine perforatrici e/o verificatrici
2|Operatore o procuratore doganale catering
5|Operatore pizza
7|Personale di fatica e/o pulizia addetto alla sala, cucina, office, magazzino
4|Pizzaiolo
4|Portiere (ex secondo portiere ed ex turnante)
6|Preparatore catering
2|Primo barman p.e.
2|Primo maitre o capo servizio sala
3|Primo pasticciere
3|Programmatore CED
4|Referente di magazzino
A|Responsabile acquisti
B|Responsabile acquisti
A|Responsabile amministrazione e controllo
B|Responsabile amministrazione e controllo
B|Responsabile area mense
A|Responsabile commerciale
B|Responsabile commerciale
B|Responsabile della manutenzione
A|Responsabile della manutenzione, responsabile tecnico
1|Responsabile delle procedure
2|Responsabile di amministrazione
B|Responsabile di funzione
A|Responsabile di funzione in strutture organizzative complesse
2|Responsabile di magazzino
2|Responsabile impianti tecnici
A|Responsabile marketing
B|Responsabile marketing
A|Responsabile personale e formazione
B|Responsabile personale e formazione
B|Responsabile punto vendita
3|Responsabile servizio ristorazione commerciale a catena
B|Responsabile tecnico
6|Secondo banconiere pasticceria
5|Secondo cuoco mensa aziendale
4|Secondo pasticciere
4|Segretario
5|Sfoglina
3|Sommelier
3|Sotto capo cuoco
4|Stenodattilografa con funzioni di segreteria
6|Stiratrice
1|Superintendente catering
2|Supervisore catering
5|Telescriventista
5|Terzo pasticciere
B|Vice direttore"""

def it(x, d=2):
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")

ccnl = load(os.path.join(SRC, "ccnl", OLD + ".json"))
R = json.loads(ccnl["regoleJson"])
R["nome"] = "Pubblici esercizi Confesercenti"
R["minimiNota"] = ("Pubblici esercizi, ristorazione e catering: paga base nazionale + contingenza (esclusa l'indennità di funzione dei Quadri: "
                   "75 € A, 70 € B). Tabella TeleConsul vigente dal 1/6/2026 al 31/5/2027; le tranche successive vengono dal testo del rinnovo 22/7/2024.")
R["scatti"]["nota"] = ("6 scatti in cifra fissa: quadriennali per gli assunti dal 1/1/2018, triennali per gli assunti fino al 31/12/2017. "
                       "Alla maturazione di ogni scatto i precedenti si ricalcolano sul valore attuale. Nel calcolo del costo indica il numero di scatti maturati.")
R["permessi"] = [{"label": "104 ore (assunti fino al 2017, o dal 5° anno)", "ore": 104},
                 {"label": "68 ore (assunti dal 2018, 3° e 4° anno)", "ore": 68},
                 {"label": "32 ore (assunti dal 2018, primi 2 anni)", "ore": 32}]
for t in R["minimi"]:
    if t["dal"] == "2026-06-01":
        for l in LIV:
            t["v"][l] = round(TAB[l][0] + TAB[l][1], 2)
doc = {**ccnl, "sigla": "Pubblici esercizi Confesercenti", "ordine": (ccnl.get("ordine") or 32) + 1,
       "nome": "CCNL Turismo Confesercenti, sezione Pubblici esercizi, ristorazione collettiva e commerciale (FIEPET-Confesercenti; FILCAMS-CGIL, FISASCAT-CISL, UILTuCS)",
       "testo": "Tabelle TeleConsul «Pubblici esercizi (Confesercenti) (agg. ipotesi)» e testo unico Turismo Confesercenti (Ipotesi 18/7/2018 e 22/7/2024)",
       "fonte": FONTE,
       "dubbi": json.dumps(["Il testo normativo è quello del Turismo Confesercenti (parte generale e Titolo XII pubblici esercizi): le schede non legate alle tabelle sono copiate da lì.",
                            "Scatti: quadriennali per gli assunti dal 2018, triennali prima; il calcolo del costo usa il numero di scatti indicato.",
                            "Tabella minimi TeleConsul vigente fino al 31/5/2027; da giugno 2027 il calcolo usa le tranche del rinnovo 2024 (da verificare)."], ensure_ascii=False),
       "regoleJson": json.dumps(R, ensure_ascii=False)}
os.makedirs(OUT, exist_ok=True)
json.dump(doc, open(os.path.join(OUT, f"ccnl-{ID}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

over = {
 "minimi": dict(voce="Minimi tabellari (paga base, contingenza)",
   sintesi="Paga base più contingenza dal 1/6/2026 al 31/5/2027: 4° livello 1.692,69 €, 5° 1.580,09 €, 6° 1.491,57 €, 7° 1.390,20 €. Quadri più indennità di funzione (75 € A, 70 € B).",
   punti=["Da giugno 2027 (1.722,69 € al 4°) e da dicembre 2027 (1.762,69 €) le tranche del rinnovo 22/7/2024.",
          "EDR di 16 € per 14 mensilità se l'azienda non versa al Fondo ASTER.",
          "Divisore orario 172 (40 ore), giornaliero 26."],
   tabella={"intest": ["Livello", "Minimo", "Contingenza", "Ind. funzione", "Totale"],
            "righe": [{"c": [l, it(TAB[l][0]), it(TAB[l][1]), it(TAB[l][2]) if TAB[l][2] else "—", it(sum(TAB[l]))]} for l in LIV]},
   attenzione=""),
 "apprendistato": dict(sintesi="Apprendistato professionalizzante per i livelli dal 2° al 6°: 36 mesi (24 per il 6° livello); figure artigiane 48 mesi (42 per il 4° livello). Retribuzione all'80% nei mesi 1-12, 85% nei mesi 13-24, 90% nei mesi 25-36 e 95% dal 37° del livello finale (paga base e contingenza).",
   tabella={"intest": ["Figura", "Livello finale", "Mesi", "Totale mensile"],
            "righe": [{"c": [f, l, f"{a}-{b}", v]} for f, l, P in APP for a, b, v in P]},
   attenzione="Importi della tabella TeleConsul in vigore dal 1/6/2026 per gli assunti dal 26/4/2012."),
 "scatti": dict(sintesi="6 scatti in cifra fissa per livello (4° livello 33,05 €): ogni 4 anni per gli assunti dal 1/1/2018, ogni 3 anni per gli assunti fino al 31/12/2017. Alla maturazione di ogni scatto i precedenti si ricalcolano sul valore del livello attuale."),
 "permessi-rol": dict(sintesi="104 ore annue di permessi retribuiti (ROL ed ex festività). Gli assunti dal 1/1/2018 maturano 32 ore nei primi 2 anni, 68 ore nel 3° e 4° anno e 104 ore dal 5°."),
 "ferie": dict(sintesi="26 giorni lavorativi di ferie all'anno (settimana di 6 giornate), pari a 173 ore con orario di 40 ore (190 con 44 ore, 195 con 45 ore)."),
 "divisori": dict(sintesi="Retribuzione giornaliera = mensile ÷ 26; oraria = mensile ÷ 172 con orario di 40 ore (190 per 44 ore, 192 per 45 ore)."),
 "previdenza": dict(sintesi="Fon.Te.: contributo 0,55% a carico dell'azienda e 0,55% del lavoratore sulla retribuzione utile al TFR, più il TFR (100% per i primi occupati dopo il 28/4/1993, 50% per chi era già occupato).",
   punti=["Quota d'iscrizione una tantum: 11,88 € azienda, 3,62 € lavoratore.", "Il lavoratore può aumentare il proprio contributo."]),
 "lavoro-extra": dict(sintesi="Lavoro extra e di surroga: compenso orario omnicomprensivo per un servizio minimo di 4 ore, per massimo 3 giorni (banchetti, eventi, fine settimana e festività).",
   punti=["Paga oraria dal 1/6/2026: 4° 16,74 €, 5° 15,93 €, 6S 15,26 €, 6° 15,07 €, 7° 14,10 €.", "Comunicazione quadrimestrale dei nominativi all'Ente bilaterale."],
   tabella={"intest": ["Livello", "Paga oraria da giugno 2026"], "righe": [{"c": [l, v]} for l, v in EXTRA]}, attenzione=""),
 "inquadramento": dict(sintesi="10 livelli: Quadri A e B, 1°, 2°, 3°, 4°, 5°, 6° super, 6° e 7°. La tabella riporta il mansionario dei pubblici esercizi, della ristorazione e del catering.",
   tabella={"intest": ["Livello", "Mansione"], "righe": [{"c": [("Quadro " + l) if l in "AB" else l, m]} for l, m in (x.split("|") for x in MANS.splitlines())]}),
 "vigenza": dict(attenzione="Tabelle del comparto pubblici esercizi: per alberghi, campeggi e agenzie usa il CCNL Turismo Confesercenti."),
}
n = 0
for f in sorted(os.listdir(os.path.join(SRC, "schede"))):
    if not f.startswith(OLD + "--"): continue
    s = load(os.path.join(SRC, "schede", f)); v = s["voce_id"]
    if v == "minimi-alberghi-minori": continue
    s = copy.deepcopy(s); s.pop("version", None)
    s.update(ccnl=ID, origine=ORIG, aggiornatoIl=NOW, aggiornatoDa="", verificata=False)
    if v in over: s.update(over[v])
    for k in ("sintesi", "attenzione"):
        if isinstance(s.get(k), str): s[k] = s[k].replace("CCNL Turismo Confesercenti", "CCNL Turismo Confesercenti (sezione pubblici esercizi)")
    json.dump(s, open(os.path.join(OUT, f"{ID}--{v}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1); n += 1
print("schede", n)

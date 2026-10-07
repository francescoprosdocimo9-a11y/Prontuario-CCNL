import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import build
OUT = sys.argv[1]
NP = "Il CCNL non contiene una disciplina specifica"
SETS = {
 "pubblici-esercizi": [
  dict(id="legge-104", s=NP + " dei permessi della legge 104/1992, che si applicano secondo la legge (3 giorni al mese o 2 ore al giorno, congedo straordinario fino a 2 anni). Il CCNL richiama la legge 104 nel part-time: chi assiste un convivente con handicap grave o ha un figlio con handicap può denunciare il patto sulle clausole elastiche.",
   p=["Dopo la denuncia il datore non può più variare la collocazione dell'orario concordata.",
      "Stessa facoltà per patologie oncologiche o gravi patologie cronico-degenerative proprie o di coniuge, figli e genitori, e per figli conviventi fino a 13 anni."],
   art="Art. 83, c. 4-6; legge 104/1992", att="Voce non disciplinata dal CCNL oltre al richiamo nel part-time.", tag=["legge 104","handicap","part-time","clausole elastiche"])],
 "portieri": [
  dict(id="sospensioni", s="Il lavoratore sottoposto a procedimento penale per reato non colposo può essere sospeso dal servizio e dalla retribuzione fino alla sentenza definitiva, conservando gli elementi in natura (es. alloggio) se non è licenziato. La sospensione disciplinare arriva fino a 5 giorni.",
   p=["La sospensione cessa con la fine del procedimento penale."],
   art="Artt. 145-146", tag=["sospensione","procedimento penale","alloggio"]),
  dict(id="trasferta", s=NP + " della trasferta: la prestazione si svolge nello stabile. Eventuali missioni vanno regolate per accordo individuale con rimborso delle spese documentate.",
   p=["Il trasferimento di proprietà dello stabile non risolve il rapporto (art. 143)."],
   art="—; art. 143", att="Voce non disciplinata dal CCNL.", tag=["trasferta","rimborso spese"])],
 "acconciatura": [
  dict(id="contributi-sindacali", s=NP + " sulla trattenuta delle quote sindacali: si opera su delega scritta del lavoratore secondo gli accordi interconfederali dell'artigianato. Restano obbligatori i versamenti alla bilateralità artigiana (EBNA-FSBA, Sanarti, Fondartigianato).",
   art="Parte comune (bilateralità)", att="Voce non disciplinata dal CCNL.", tag=["contributi sindacali","delega","ebna","fsba"]),
  dict(id="divise", s=NP + " su divise e indumenti di lavoro: se l'impresa impone una divisa, il costo è a suo carico; restano gli obblighi di fornire i DPI previsti dal D.Lgs. 81/2008.",
   art="—; D.Lgs. 81/2008", att="Voce non disciplinata dal CCNL.", tag=["divise","indumenti","dpi"]),
  dict(id="quadri", s="Il CCNL artigiano dell'acconciatura ed estetica non prevede la categoria dei quadri: la classificazione parte dal 1° livello (lavoratori altamente qualificati che operano in autonomia e possono guidare altri addetti).",
   art="Classificazione del personale", tag=["quadri","classificazione","1° livello"])],
 "ced": [
  dict(id="appalti", s=NP + " sugli appalti: appalti ed esternalizzazioni sono oggetto dell'informazione ed esame congiunto annuale a livello nazionale tra ASSOCED, LAIT e UGL Terziario. Per la responsabilità solidale e i cambi d'appalto si applica la legge (art. 29 D.Lgs. 276/2003).",
   art="Art. 228", att="Voce non disciplinata dal CCNL oltre alle procedure di informazione.", tag=["appalti","esternalizzazione","informazione"]),
  dict(id="divise", s=NP + " su divise e indumenti di lavoro: si applicano gli eventuali accordi aziendali e gli obblighi sui DPI del D.Lgs. 81/2008.",
   art="—; D.Lgs. 81/2008", att="Voce non disciplinata dal CCNL.", tag=["divise","indumenti","dpi"])],
 "studi-professionali": [
  dict(id="appalti", s=NP + " sugli appalti; per responsabilità solidale e cambi d'appalto si applica la legge (art. 29 D.Lgs. 276/2003).",
   art="—; art. 29 D.Lgs. 276/2003", att="Voce non disciplinata dal CCNL.", tag=["appalti","responsabilità solidale"]),
  dict(id="divise", s=NP + " su divise e indumenti di lavoro: se lo studio impone una divisa il costo è a suo carico; restano gli obblighi sui DPI del D.Lgs. 81/2008.",
   art="—; D.Lgs. 81/2008", att="Voce non disciplinata dal CCNL.", tag=["divise","indumenti","dpi"])],
 "agenzie-viaggio": [
  dict(id="appalti", s=NP + " sugli appalti; per responsabilità solidale e cambi d'appalto si applica la legge (art. 29 D.Lgs. 276/2003).",
   art="—; art. 29 D.Lgs. 276/2003", att="Voce non disciplinata dal CCNL.", tag=["appalti","responsabilità solidale"])],
}
os.makedirs(OUT, exist_ok=True)
w = []
for cc, items in SETS.items():
    for vid, d in build(cc, items).items():
        fp = f"{OUT}/{cc}--{vid}.json"; json.dump(d, open(fp, 'w'), ensure_ascii=False)
        w.append({"op": "set", "collection": "schede", "doc_id": f"{cc}--{vid}", "file_path": fp})
print(json.dumps(w, separators=(',', ':')))

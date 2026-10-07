# Prontuario CCNL – dati e generatori

Materiale di lavoro dell'artefatto «Prontuario CCNL» (database condiviso con le collezioni `ccnl`, `schede`, `clienti`).

- `gen/` – script Python che generano schede e regole dei calcolatori per ciascun CCNL a partire dai testi unici TeleConsul (stampa del 06/10/2026) e dai testi della cartella Drive «CCNL 2» (CNAI, Confapi, Edilizia artigianato, Abbigliamento PMI, CIFA, Enti formazione Fidef).
  `common.py` contiene la logica comune, `canon.json` l'elenco delle voci canoniche; gli altri file contengono i dati di un CCNL.
  Uso: `python3 -I gen/<ccnl>.py data` e poi `python3 -I gen/mkbatch.py <id-ccnl> [id clienti]` per preparare le scritture batch.
- `data/` – documenti JSON generati (`ccnl-<id>.json` e `<id>--<voce>.json`) già caricati nel database.
- `page/prontuario.html` – sorgente della pagina pubblicata (versione con preavviso per gruppo/voce, comporto con arco per anzianità scheda «Scadenziario» che legge la vigenza di ogni CCNL e ordina i contratti per data di scadenza, calcolatori di infortunio, TFR e indennità sostitutiva del preavviso).
- `gen/infortunio.py` – regole del calcolatore infortunio per ogni CCNL (campo `infortunio` di `regoleJson`; Commercio e Metalmeccanica sono incorporati nella pagina). Uso: `python3 -I gen/infortunio.py <cartella con ccnl/<id>.json> <uscita>` per preparare gli aggiornamenti.

Tutte le schede generate sono marcate «Da verificare»: vanno controllate sul testo del CCNL prima dell'uso.
- `gen/contratti_termine.py` – importa lo scadenziario Excel dei contratti a termine nella collezione `contratti` (un documento per contratto: cliente, sede, dipendente, tipo, assunzione, scadenze e proroghe, note, stato). I dati dei dipendenti non sono salvati nel repository.

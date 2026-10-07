# Prontuario CCNL – dati e generatori

Materiale di lavoro dell'artefatto «Prontuario CCNL» (database condiviso con le collezioni `ccnl`, `schede`, `clienti`).

- `gen/` – script Python che generano schede e regole dei calcolatori per ciascun CCNL a partire dai testi unici TeleConsul (stampa del 06/10/2026).
  `common.py` contiene la logica comune, `canon.json` l'elenco delle voci canoniche; gli altri file contengono i dati di un CCNL.
  Uso: `python3 -I gen/<ccnl>.py data` e poi `python3 -I gen/mkbatch.py <id-ccnl> [id clienti]` per preparare le scritture batch.
- `data/` – documenti JSON generati (`ccnl-<id>.json` e `<id>--<voce>.json`) già caricati nel database.
- `page/prontuario.html` – sorgente della pagina pubblicata (versione con preavviso per gruppo/voce e comporto con arco per anzianità).

Tutte le schede generate sono marcate «Da verificare»: vanno controllate sul testo del CCNL prima dell'uso.

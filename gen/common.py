import json, os, sys
BASE = os.path.dirname(os.path.abspath(__file__))
CANON = json.load(open(os.path.join(BASE, 'canon.json')))
CH = {"c":"Il contratto","a":"3. L'assunzione","t":"4. Le tipologie contrattuali","o":"5. Orario di lavoro, riposi, ferie e permessi",
      "r":"6. La retribuzione","m":"10. Malattia, infortunio, maternità e congedi","d":"12. Il potere disciplinare",
      "x":"13. La cessazione del rapporto","s":"Rapporti sindacali, sicurezza e tutele","p":"Appalti e vicende d'azienda","e":"Enti bilaterali e welfare"}
EXTRA_ORD = {"c":80,"a":180,"t":282,"o":380,"r":480,"m":580,"d":680,"x":780,"s":880,"p":980,"e":1080}
NOW = "2026-10-07T12:00:00+02:00"
ORIG = "Estratta automaticamente dal testo unico: da verificare"

def build(ccnl, items):
    docs = {}
    for it in items:
        vid = it['id']
        c = CANON.get(vid)
        if c:
            cap, ordine, voce = c['capitolo'], c['ordine'], c['voce']
        else:
            cap = CH[it['cap']]; ordine = EXTRA_ORD[it['cap']]; voce = None
        if 'cap' in it and c is None: pass
        d = {"ccnl": ccnl, "voce_id": vid, "capitolo": cap, "voce": it.get('voce') or voce,
             "sintesi": it['s'], "punti": it.get('p', []), "articoli": it.get('art', ''),
             "attenzione": it.get('att', ''), "tag": it.get('tag', []), "verificata": False,
             "ordine": ordine, "origine": ORIG, "aggiornatoIl": NOW, "aggiornatoDa": ""}
        if it.get('tab'):
            h, *rows = it['tab']
            d['tabella'] = {"intest": h, "righe": [{"c": r} for r in rows]}
        assert d['voce'], vid
        assert vid not in docs, vid
        docs[vid] = d
    return docs

def write(ccnl, docs, meta, out):
    os.makedirs(out, exist_ok=True)
    for vid, d in docs.items():
        json.dump(d, open(f"{out}/{ccnl}--{vid}.json", 'w'), ensure_ascii=False)
    meta = dict(meta)
    meta['regoleJson'] = json.dumps(meta['regoleJson'], ensure_ascii=False)
    json.dump(meta, open(f"{out}/ccnl-{ccnl}.json", 'w'), ensure_ascii=False)
    ids = sorted(docs)
    batches = []
    for i in range(0, len(ids), 45):
        batches.append([{"op":"set","collection":"schede","doc_id":f"{ccnl}--{v}","file_path":f"{out}/{ccnl}--{v}.json"} for v in ids[i:i+45]])
    json.dump(batches, open(f"{out}/batches-{ccnl}.json", 'w'), ensure_ascii=False, indent=0)
    print(ccnl, len(docs), 'schede,', len(batches), 'batch')

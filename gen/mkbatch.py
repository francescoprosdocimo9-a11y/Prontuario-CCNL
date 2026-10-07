import json, sys
D = '/home/user/Prontuario-CCNL/data'; cc = sys.argv[1]; cl = sys.argv[2:]
b = json.load(open(f'{D}/batches-{cc}.json'))
w = [{"op":"set","collection":"ccnl","doc_id":cc,"file_path":f"{D}/ccnl-{cc}.json"}] + [x for bb in b for x in bb]
for c in cl: w.append({"op":"update","collection":"clienti","doc_id":c,"data":{"ccnl":cc,"abbinamento":"certo"},"if_version":1})
for i in range(0, len(w), 50): print(json.dumps(w[i:i+50], separators=(',',':'))); print()

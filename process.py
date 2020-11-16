import csv
import glob
import json

for f in glob.glob('Data/*.csv'):
    data = {}
    region = f.replace('Data/NSUL_OCT_2020_', '').replace('.csv', '')
    reader = csv.DictReader(open(f))
    for row in reader:
        uprn = row.pop('uprn')
        pc = row.pop('pcds')
        e = row.pop('gridgb1e')
        n = row.pop('gridgb1n')
        if not pc:
            continue
        for typ in row:
            data.setdefault(pc, {}).setdefault(typ, set()).add(row[typ])

    for pc in data:
        data[pc] = { k: list(v) for (k,v) in data[pc].items() if len(v) > 1 } 
    data = { k: v for (k,v) in data.items() if len(v) > 0 }

    wr = open('split%s.json' % region, 'w')
    json.dump(data, wr)
    wr.close()
    wr = open('split%s.csv' % region, 'w')
    writer = csv.writer(wr)
    writer.writerow(['postcode', 'key', 'value'])
    for pc in data:
        for typ in data[pc]:
            if len(data[pc][typ]) > 1:
                for v in data[pc][typ]:
                    writer.writerow([ pc, typ, v ])
    wr.close()


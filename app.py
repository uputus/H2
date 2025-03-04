import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

# Laadime CSV faili mällu
# Asendage failitee oma tegeliku faili asukohaga
df = pd.read_csv('LE.txt', sep="\t", encoding="ISO-8859-1")

# Kui fail on liiga suur, võib olla vajalik lugeda see osadeks
# df = pd.read_csv('LE.txt', sep="\t", encoding="utf-8", chunksize=10000)

@app.route('/spare-parts', methods=['GET'])
def get_spare_parts():
    # Filtreerimine parameetrite järgi
    name = request.args.get('name')
    sn = request.args.get('sn')
    sort = request.args.get('sort')
    page = int(request.args.get('page', 1))  # Lehekülg 1 on vaikimisi
    per_page = 30  # Üks lehekülg sisaldab 30 tulemust

    # Filtreerimine nime järgi
    if name:
        filtered_df = df[df['name'].str.contains(name, case=False, na=False)]
    elif sn:
        filtered_df = df[df['serial_number'] == sn]
    else:
        filtered_df = df

    # Sorteerimine
    if sort:
        if sort.startswith('-'):
            filtered_df = filtered_df.sort_values(by=sort[1:], ascending=False)
        else:
            filtered_df = filtered_df.sort_values(by=sort, ascending=True)

    # Leheküljendamine
    start = (page - 1) * per_page
    end = start + per_page
    result = filtered_df.iloc[start:end]

    # Tagastame JSON
    return jsonify(result.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True, port=3300)

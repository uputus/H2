import pandas as pd
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Laadime CSV faili mällu
try:
    df = pd.read_csv('LE.txt', sep="\t", encoding="ISO-8859-1", header=None)
    
    # Manually set column names based on the data structure
    df.columns = ['serial_number', 'name', 'attribute_1', 'attribute_2', 'attribute_3', 'attribute_4', 'attribute_5', 'attribute_6', 'price', 'brand', 'attribute_7']
    
    # Print column names to verify
    print(f"Columns in DataFrame: {df.columns.tolist()}")
    
except FileNotFoundError:
    print("File LE.txt not found.")
    abort(404, description="File not found.")
except Exception as e:
    print(f"Error loading file: {e}")
    abort(500, description="Error loading the file.")

# Kontrollime, kas vajalikud veerud eksisteerivad
required_columns = ['name', 'serial_number']  # Adjust this based on actual column names
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print(f"Missing columns: {', '.join(missing_columns)}")
    abort(400, description=f"Missing columns: {', '.join(missing_columns)}")

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

    # Tagastame JSON koos andmetega ja lehekülje teabega
    return jsonify({
        'data': result.to_dict(orient='records'),

    })



if __name__ == '__main__':
    app.run(debug=True, port=3300)

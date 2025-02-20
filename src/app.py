from flask import Flask, request, jsonify, render_template
import tn_funcs as t
from utils import validate

app = Flask(__name__)


# API route to calculate bill

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    try:

        units = int(data.get('units', 0))
        
        validate.isPositiveInt(units)
        
        result=t.calculate_bill(units)
        amount=result["amount"]
        df=result["df"]


        print(f"{amount} - amount")

        df_html = df.to_html(classes='table table-bordered', index=False)
        print(df_html)
        return jsonify({'df_html': df_html, 'amount': amount, 'units':units})

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# Home route (optional)s
@app.route('/')
def home():
   return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

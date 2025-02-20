from flask import Flask, request, jsonify, render_template
import tn_funcs as t
from utils import validate

app = Flask(__name__)


# API route to calculate bill

@app.route('/calculate_billAmount', methods=['POST'])
def calculate_billAmount():
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

@app.route('/page1', methods=['GET','POST'])
def page1():
    try:
        return render_template("page1.html")

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/page2', methods=['GET','POST'])
def page2():
    try:
        return render_template("page2.html")

    except ValueError as e:
        return jsonify({'error': str(e)}), 400


# API to determine units using price:

@app.route('/determine_unitsConsumed', methods=['POST'])
def determine_unitsConsumed_by_billAmount():
    data = request.json
    try:

        billAmount = int(data.get('billAmount', 0))
        
        validate.isPositiveInt(billAmount)
        
        result=t.determine_units_using_billAmount(billAmount)
        unitsConsumed=result
        
        print(f"return value is {unitsConsumed} units.")

        return jsonify({'unitsConsumed': unitsConsumed, 'billAmount': billAmount})

    except ValueError as e:
        return jsonify({'error': str(e)}), 400



# Home route (optional)s
@app.route('/')
def home():
   return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

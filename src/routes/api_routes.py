from flask import Flask, request, jsonify, render_template, Blueprint
import tn_funcs # found in same folder
from utils import validate # found in same folder

api_routes=Blueprint("api_routes",__name__)

# API route to calculate bill
@api_routes.route('/calculate_billAmount', methods=['POST'])
def calculate_billAmount():
    data = request.get_json(silent=True) #prevent crash for empty body
    
    if not data:
        return jsonify({'error': f'Invalid JSON or empty request body. \
                        request wanted to calculate_billAmount but didnt send units. \
                        given data={data}'}), 400
    
    try:

        units = data.get('units')
        if units is None:
            raise ValueError("Units is None in request")


        units=int(units)
        validate.isPositiveInt(units)
        
        #PROCESS
        result=tn_funcs.calculate_bill(units)
        amount,df=result["amount"],result["df"]


        #Prepare Output JSON
        df_html = df.to_html(classes='table table-bordered', index=False)

        return jsonify({'df_html': df_html, 'amount': amount, 'units':units})

    except (ValueError,TypeError,KeyError) as e:
        return jsonify({'error': str(e)}), 400

# API to determine units using price:
@api_routes.route('/determine_unitsConsumed', methods=['POST'])
def determine_unitsConsumed_by_billAmount():
    data = request.get_json(silent=True)
    
    if not data:
        return jsonify({'error':f'Invalid JSON or empty request body. \
                        whoever requested wanted to determine_unitsConsumed but didnt send billAmount. \
                        given data={data}'}),400
    try:
        
        # Get requirement arguments from request data object
        billAmount = data.get('billAmount')

        #Verify values of arguments
        if billAmount is None:
            raise ValueError("Missing 'billAmount' in request")

        billAmount=int(billAmount)
        validate.isPositiveInt(billAmount)
        
        #PROCESS
        unitsConsumed=tn_funcs.determine_units_using_billAmount(billAmount)
        
    
        return jsonify({'unitsConsumed': unitsConsumed, 'billAmount': billAmount})

    except (ValueError,TypeError,KeyError) as e:
        return jsonify({'error': str(e)}), 400

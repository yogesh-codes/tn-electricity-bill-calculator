from flask import Flask, request, jsonify, render_template, Blueprint


page_routes= Blueprint("page_routes",__name__)

@page_routes.route('/page1', methods=['GET'])
def page1():
    return render_template("page1.html")

    '''
    try:
        return render_template("page1.html")

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    '''

    '''
    if request.method=='POST':
        data= request.get_json(silent=True)
        if data is None:
            return jsonify({'error': 'No JSON data provided','extra':f'{data}'}), 400
        
        return jsonify({'message': 'POST request received', 'data': data})
    '''
    

@page_routes.route('/page2', methods=['GET'])
def page2():
    return render_template("page2.html")


# Home route (optional)s
@page_routes.route('/')
def home():
   return render_template('index.html')

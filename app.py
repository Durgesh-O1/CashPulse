from flask import Flask, jsonify, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    # 1. Grab the custom rates sent by your Screener UI!
    income_rate = float(request.args.get('income_rate', 5)) / 100
    expense_rate = float(request.args.get('expense_rate', 2)) / 100

    df = pd.read_csv('ledger.csv')
    df['Net_Cash'] = df['Income'] - df['Expenses']
    
    labels = df['Month'].tolist()
    historical_net = df['Net_Cash'].tolist()
    
    last_income = df['Income'].iloc[-1]
    last_expenses = df['Expenses'].iloc[-1]
    
    future_labels = ['April (Proj)', 'May (Proj)', 'June (Proj)']
    future_net = []
    
    for i in range(1, 4):
        # 2. Use the custom rates dynamically!
        proj_income = last_income * ((1 + income_rate) ** i)
        proj_expenses = last_expenses * ((1 + expense_rate) ** i)
        future_net.append(round(proj_income - proj_expenses, 2))
        
    padded_future = [None] * (len(historical_net) - 1) + [historical_net[-1]] + future_net
    all_labels = labels + future_labels

    return jsonify({
        'labels': all_labels,
        'historical': historical_net,
        'predicted': padded_future
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
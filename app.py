from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

AUTOMATED_COST_PER_INVOICE = 0.20
ERROR_RATE_AUTO = 0.001
TIME_SAVED_PER_INVOICE_MINS = 8
MIN_ROI_BOOST_FACTOR = 1.1
DB_FILE = 'scenarios.json'


def get_scenarios():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_scenarios(scenarios):
    with open(DB_FILE, 'w') as f:
        json.dump(scenarios, f, indent=2)


@app.route('/simulate', methods=['POST'])
def run_simulation():
    data = request.get_json()

    monthly_invoice_volume = float(data['monthly_invoice_volume'])
    hourly_wage = float(data['hourly_wage'])
    error_rate_manual = float(data['error_rate_manual']) / 100
    error_cost = float(data['error_cost'])
    time_horizon_months = int(data['time_horizon_months'])
    one_time_implementation_cost = float(data.get('one_time_implementation_cost', 0))

    time_saved_in_hours = TIME_SAVED_PER_INVOICE_MINS / 60.0
    labor_savings = monthly_invoice_volume * time_saved_in_hours * hourly_wage
    error_savings = (error_rate_manual - ERROR_RATE_AUTO) * monthly_invoice_volume * error_cost
    automation_cost = monthly_invoice_volume * AUTOMATED_COST_PER_INVOICE

    monthly_savings = (labor_savings + error_savings - automation_cost) * MIN_ROI_BOOST_FACTOR
    payback_months = one_time_implementation_cost / monthly_savings if monthly_savings > 0 else float('inf')

    cumulative_savings = monthly_savings * time_horizon_months
    net_savings = cumulative_savings - one_time_implementation_cost
    roi_percentage = (net_savings / one_time_implementation_cost) * 100 if one_time_implementation_cost > 0 else float('inf')

    return jsonify({
        'monthly_savings': round(monthly_savings, 2),
        'payback_months': round(payback_months, 1),
        'roi_percentage': round(roi_percentage, 2)
    })


@app.route('/scenarios', methods=['POST'])
def create_scenario():
    scenario_data = request.get_json()
    scenarios = get_scenarios()
    scenarios.append(scenario_data)
    save_scenarios(scenarios)
    return jsonify({'status': 'success', 'message': 'Scenario saved!'}), 201


@app.route('/scenarios', methods=['GET'])
def list_scenarios():
    scenarios = get_scenarios()
    return jsonify(scenarios)


if __name__ == '__main__':
    app.run(debug=True, port=5001)

const API_URL = 'http://localhost:5001';

document.getElementById('calculate_button').addEventListener('click', async () => {
  const data = {
    monthly_invoice_volume: document.getElementById('monthly_invoice_volume').value,
    hourly_wage: document.getElementById('hourly_wage').value,
    error_rate_manual: document.getElementById('error_rate_manual').value,
    error_cost: document.getElementById('error_cost').value,
    time_horizon_months: document.getElementById('time_horizon_months').value,
    one_time_implementation_cost: document.getElementById('one_time_implementation_cost').value,
  };

  try {
    const response = await fetch(`${API_URL}/simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    document.getElementById('monthly_savings_result').textContent = `$${result.monthly_savings}`;
    document.getElementById('payback_months_result').textContent = `${result.payback_months} months`;
    document.getElementById('roi_percentage_result').textContent = `${result.roi_percentage}%`;
  } catch (error) {
    alert('Error connecting to backend. Please make sure Flask is running.');
    console.error(error);
  }
});

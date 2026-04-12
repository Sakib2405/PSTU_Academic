document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('calcForm');
  const valueEl = document.getElementById('value');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const num1 = document.getElementById('num1').value;
    const operator = document.getElementById('operator').value;
    const num2 = document.getElementById('num2').value;

    valueEl.textContent = 'Calculating…';

    try {
      const res = await fetch('/api/calc', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ num1, operator, num2 })
      });

      const data = await res.json();
      valueEl.textContent = data.result;
    } catch (err) {
      valueEl.textContent = 'Error: ' + err.message;
    }
  });
});

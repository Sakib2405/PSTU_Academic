document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('calcForm');
  const valueEl = document.getElementById('value');
  const historyList = document.getElementById('historyList');
  const clearHistoryBtn = document.getElementById('clearHistory');
  const refreshHistoryBtn = document.getElementById('refreshHistory');
  const clearBtn = document.getElementById('clearButton');

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
      renderHistory(data.history || []);
    } catch (err) {
      valueEl.textContent = 'Error: ' + err.message;
    }
  });

  clearBtn.addEventListener('click', () => {
    document.getElementById('num1').value = '';
    document.getElementById('num2').value = '';
    valueEl.textContent = '—';
  });

  refreshHistoryBtn.addEventListener('click', fetchHistory);
  clearHistoryBtn.addEventListener('click', async () => {
    await fetch('/api/history/clear', { method: 'POST' });
    renderHistory([]);
  });

  async function fetchHistory(){
    try{
      const r = await fetch('/api/history');
      const j = await r.json();
      renderHistory(j.history || []);
    }catch(e){ console.warn(e) }
  }

  function renderHistory(list){
    historyList.innerHTML = '';
    if(!list || list.length === 0){
      historyList.innerHTML = '<div class="muted">No calculations yet.</div>';
      return;
    }
    for(const item of list){
      const div = document.createElement('div');
      div.className = 'history-item';
      div.textContent = item;
      historyList.appendChild(div);
    }
  }

  // load initial history
  fetchHistory();
});

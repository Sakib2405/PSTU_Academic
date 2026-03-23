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

    // Client-side validation
    const validOperators = ['+','-','*','/','%'];
    if(num1 === '' || num2 === ''){
      showError('Please enter both numbers');
      return;
    }
    if(!validOperators.includes(operator)){
      showError('Invalid operator selected');
      return;
    }
    if((operator === '/' || operator === '%') && Number(num2) === 0){
      showError('Cannot divide by zero');
      return;
    }

    valueEl.textContent = 'Calculating…';
    valueEl.parentElement.classList.remove('error');

    try {
      const res = await fetch('/api/calc', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ num1, operator, num2 })
      });

      const data = await res.json();
      if(data.ok){
        showResult(data.result);
      } else {
        showError(data.error || 'Server error');
      }
      renderHistory(data.history || []);
    } catch (err) {
      showError('Network error');
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

  function showResult(value){
    valueEl.textContent = value;
    // add success badge style + animation
    const parent = valueEl.parentElement;
    parent.classList.remove('error');
    parent.classList.add('pulse');
    setTimeout(()=> parent.classList.remove('pulse'), 950);
  }

  function showError(msg){
    valueEl.textContent = msg;
    const parent = valueEl.parentElement;
    parent.classList.add('error');
    parent.classList.remove('pulse');
  }

  // load initial history
  fetchHistory();
});

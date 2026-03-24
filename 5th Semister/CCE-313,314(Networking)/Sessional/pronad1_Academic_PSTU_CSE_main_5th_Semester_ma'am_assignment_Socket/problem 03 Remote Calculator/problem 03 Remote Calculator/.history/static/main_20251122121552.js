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
    // allow float zero check
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
      // choose icon based on success or error
      const isError = /ERROR:/i.test(item);
      const icon = isError ? errorSVG() : checkSVG();
      div.innerHTML = `${icon}<div style="display:inline-block;vertical-align:middle;margin-left:8px">${escapeHtml(item)}</div>`;
      historyList.appendChild(div);
    }
  }

  function escapeHtml(s){
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  function checkSVG(){
    return `<svg class="icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="9" stroke="#10B981" stroke-width="1.4"/><path d="M8.5 12.5l2 2 5-5" stroke="#10B981" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
  }

  function errorSVG(){
    return `<svg class="icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="9" stroke="#EF4444" stroke-width="1.4"/><path d="M12 8v5" stroke="#EF4444" stroke-width="1.6" stroke-linecap="round"/><path d="M12 16h.01" stroke="#EF4444" stroke-width="1.6" stroke-linecap="round"/></svg>`;
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

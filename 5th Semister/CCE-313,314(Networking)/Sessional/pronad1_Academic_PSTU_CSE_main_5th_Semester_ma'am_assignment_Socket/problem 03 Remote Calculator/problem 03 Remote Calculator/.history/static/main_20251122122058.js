document.addEventListener('DOMContentLoaded', () => {
  const displayEl = document.getElementById('calcDisplay');
  const valueEl = document.getElementById('value');
  const historyList = document.getElementById('historyList');
  const clearHistoryBtn = document.getElementById('clearHistory');
  const refreshHistoryBtn = document.getElementById('refreshHistory');
  const keypad = document.getElementById('keypad');

  // Calculator state
  let first = '';
  let second = '';
  let operator = null;
  let enteringSecond = false;

  function updateDisplay(){
    if(!enteringSecond){
      displayEl.textContent = first === '' ? '0' : first;
    } else {
      displayEl.textContent = (first === '' ? '0' : first) + ' ' + operator + ' ' + (second === '' ? '' : second);
    }
  }

  function resetAll(){ first = ''; second = ''; operator = null; enteringSecond = false; updateDisplay(); showResult('—'); }

  keypad.addEventListener('click', async (e) => {
    const btn = e.target.closest('button');
    if(!btn) return;
    const key = btn.getAttribute('data-key');
    const op = btn.getAttribute('data-op');

    if(key){
      // digit or dot
      if(!enteringSecond){
        if(key === '.' && first.includes('.')) return;
        first += key;
      } else {
        if(key === '.' && second.includes('.')) return;
        second += key;
      }
      updateDisplay();
      return;
    }

    if(op){
      if(op === 'C'){
        resetAll();
        return;
      }
      if(op === '←'){
        // backspace
        if(enteringSecond){ second = second.slice(0,-1); }
        else { first = first.slice(0,-1); }
        updateDisplay();
        return;
      }
      if(op === '='){
        // perform calculation if possible
        if(!operator || second === ''){ showError('Enter operator and second number'); return; }
        await callApiAndShow();
        return;
      }
      // operator selected (+ - * / %)
      if(first === ''){ showError('Enter first number'); return; }
      if(operator && second !== ''){
        // chain calculations: compute previous then set operator
        await callApiAndShow();
        // result moved to first by callApiAndShow
      }
      operator = op;
      enteringSecond = true;
      updateDisplay();
      return;
    }
  });

  async function callApiAndShow(){
    const num1 = first;
    const num2 = second;
    const op = operator;

    // client-side validation
    if(num1 === '' || num2 === '' || !op){ showError('Incomplete expression'); return; }
    if((op === '/' || op === '%') && Number(num2) === 0){ showError('Cannot divide by zero'); return; }

    showInfo('Calculating…');
    try{
      const res = await fetch('/api/calc', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ num1, operator: op, num2 })
      });
      const data = await res.json();
      if(data.ok){
        showResult(data.result);
        // put result back into first for chaining
        first = String(data.result);
        second = '';
        operator = null;
        enteringSecond = false;
      } else {
        showError(data.error || 'Server error');
      }
      renderHistory(data.history || []);
      updateDisplay();
    }catch(e){ showError('Network error'); }
  }

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

  function showInfo(msg){
    valueEl.textContent = msg;
    const parent = valueEl.parentElement;
    parent.classList.remove('error');
  }

  // load initial history
  fetchHistory();
  updateDisplay();
});

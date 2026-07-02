/* ── Renderizar items del resumen ── */
const itemsEl  = document.getElementById('resumen-items-js');
const items    = JSON.parse(itemsEl.dataset.items || '[]');
const resumen  = document.querySelector('.resumen-box');
let html = '';
items.forEach(it => {
  const p = Number(it.precio).toLocaleString('es-CL');
  html += `<div class="resumen-item"><span>${it.nombre}</span><span class="resumen-item-precio">$${p}</span></div>`;
});
itemsEl.innerHTML = html;

/* ── Selección de método de pago ── */
const metodos      = document.querySelectorAll('.metodo');
const panelTarjeta = document.getElementById('panel-tarjeta');
const panelEfectivo= document.getElementById('panel-efectivo');
let metodoActual   = 'webpay';

metodos.forEach(m => {
  m.addEventListener('click', () => {
    metodos.forEach(x => x.classList.remove('activo'));
    m.classList.add('activo');
    m.querySelector('input').checked = true;
    metodoActual = m.dataset.metodo;
    panelTarjeta.style.display  = metodoActual === 'efectivo' ? 'none' : 'block';
    panelEfectivo.style.display = metodoActual === 'efectivo' ? 'block' : 'none';
  });
});

/* ── Preview tarjeta en tiempo real ── */
function fmt4(v) { return v.replace(/\D/g,'').replace(/(.{4})/g,'$1 ').trim(); }

document.getElementById('card-numero').addEventListener('input', e => {
  e.target.value = fmt4(e.target.value).slice(0,19);
  document.getElementById('prev-numero').textContent = e.target.value || '•••• •••• •••• ••••';
});
document.getElementById('card-exp').addEventListener('input', e => {
  let v = e.target.value.replace(/\D/g,'');
  if (v.length >= 3) v = v.slice(0,2) + '/' + v.slice(2,4);
  e.target.value = v;
  document.getElementById('prev-exp').textContent = v || 'MM/AA';
});
document.getElementById('card-nombre').addEventListener('input', e => {
  document.getElementById('prev-nombre').textContent = e.target.value.toUpperCase() || 'NOMBRE APELLIDO';
});

/* ── Toast ── */
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2600);
}

/* ── Pagar ── */
document.getElementById('btn-pagar').addEventListener('click', async () => {
  const token = document.getElementById('btn-pagar').dataset.token;

  // Validación básica tarjeta
  if (metodoActual !== 'efectivo') {
    const num = document.getElementById('card-numero').value.replace(/\s/g,'');
    if (num.length < 16) { showToast('Ingresa un número de tarjeta válido'); return; }
    if (!document.getElementById('card-exp').value.includes('/')) { showToast('Ingresa la fecha de vencimiento'); return; }
    if (document.getElementById('card-cvv').value.length < 3) { showToast('Ingresa el CVV'); return; }
  }

  document.getElementById('overlay-loading').style.display = 'flex';

  // Simular demora de pasarela (1.5s)
  await new Promise(r => setTimeout(r, 1500));

  try {
    const res  = await fetch('/api/pago/confirmar', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, metodo: metodoActual })
    });
    const data = await res.json();
    if (data.ok) { window.location.href = data.redirect; }
    else { showToast('Error al procesar el pago'); document.getElementById('overlay-loading').style.display = 'none'; }
  } catch {
    showToast('Error de conexión'); document.getElementById('overlay-loading').style.display = 'none';
  }
});

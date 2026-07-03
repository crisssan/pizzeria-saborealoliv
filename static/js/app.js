/* ── NAV scroll ── */
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => nav.classList.toggle('scrolled', window.scrollY > 60));

/* ── FILTROS menu ── */
document.querySelectorAll('.filtro').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filtro').forEach(b => b.classList.remove('activo'));
    btn.classList.add('activo');
    const cat = btn.dataset.cat;
    document.querySelectorAll('.pizza-card').forEach(card => {
      card.classList.toggle('oculta', cat !== 'todas' && card.dataset.cat !== cat);
    });
  });
});

/* ── CARRITO ── */
let carrito = [];
function fmt(n) { return '$' + Number(n).toLocaleString('es-CL'); }

function renderCarrito() {
  const lista    = document.getElementById('carrito-items');
  const totalBox = document.getElementById('carrito-total');
  if (!lista) return;
  if (!carrito.length) {
    lista.innerHTML = '<p class="carrito-vacio">Agrega pizzas desde el menu arriba</p>';
    if (totalBox) totalBox.style.display = 'none';
    return;
  }
  lista.innerHTML = carrito.map((item, i) => `
    <div class="carrito-item">
      <span class="carrito-item-nombre">${item.nombre}</span>
      <span class="carrito-item-precio">${fmt(item.precio)}</span>
      <button class="btn-quitar" data-idx="${i}">x</button>
    </div>`).join('');
  const total = carrito.reduce((s, i) => s + i.precio, 0);
  if (document.getElementById('total-valor')) document.getElementById('total-valor').textContent = fmt(total);
  if (totalBox) totalBox.style.display = 'flex';
  document.querySelectorAll('.btn-quitar').forEach(btn =>
    btn.addEventListener('click', () => { carrito.splice(+btn.dataset.idx, 1); renderCarrito(); })
  );
}

document.querySelectorAll('.btn-agregar:not(.btn-agregar-off)').forEach(btn => {
  btn.addEventListener('click', () => {
    carrito.push({ id: btn.dataset.id, nombre: btn.dataset.nombre, precio: +btn.dataset.precio });
    renderCarrito();
    showToast('+ ' + btn.dataset.nombre + ' agregada al carrito');
    btn.textContent = 'Agregado';
    btn.style.cssText = 'background:var(--red);color:white;border-color:var(--red)';
    setTimeout(() => { btn.textContent = 'Agregar'; btn.style.cssText = ''; }, 1400);
  });
});

/* ── TOAST ── */
let toastTimer;
function showToast(msg) {
  const t = document.getElementById('toast');
  if (!t) return;
  t.textContent = msg; t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 2600);
}

/* ── FORM PEDIDO ── */
const formPedido = document.getElementById('form-pedido');
if (formPedido) {
  formPedido.addEventListener('submit', async e => {
    e.preventDefault();
    if (!carrito.length) { showToast('Agrega al menos una pizza primero!'); return; }
    const btn = document.getElementById('btn-pedido');
    btn.disabled = true; btn.textContent = 'Creando pedido...';
    try {
      const res  = await fetch('/api/pedido', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nombre:    document.getElementById('nombre').value,
          telefono:  document.getElementById('telefono').value,
          email:     document.getElementById('email').value,
          direccion: document.getElementById('direccion').value,
          items: carrito,
          total: carrito.reduce((s, i) => s + i.precio, 0)
        })
      });
      const data = await res.json();
      if (data.ok) { window.location.href = data.pago_url; }
      else { showToast('Error: ' + (data.error || 'intenta de nuevo')); btn.disabled = false; btn.textContent = 'Ir a pagar'; }
    } catch { showToast('Error de conexion.'); btn.disabled = false; btn.textContent = 'Ir a pagar'; }
  });
}

/* ── WHATSAPP FLOTANTE ── */
(function() {
  const fab    = document.getElementById('wsp-fab');
  const popup  = document.getElementById('wsp-popup');
  const cerrar = document.getElementById('wsp-cerrar');
  const badge  = document.getElementById('wsp-badge');
  if (!fab) return;
  setTimeout(() => { popup.classList.add('visible'); if (badge) badge.style.display = 'none'; }, 5000);
  fab.addEventListener('click', () => {
    popup.classList.toggle('visible');
    if (badge) badge.style.display = 'none';
  });
  cerrar.addEventListener('click', e => { e.stopPropagation(); popup.classList.remove('visible'); });
})();

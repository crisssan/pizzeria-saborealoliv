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
  const btnPedir = document.getElementById('btn-pedido');
  if (!lista) return;

  if (!carrito.length) {
    lista.innerHTML = '<p class="carrito-vacio">Agrega pizzas desde el menu arriba</p>';
    if (totalBox) totalBox.style.display = 'none';
    if (btnPedir) btnPedir.disabled = true;
    return;
  }

  lista.innerHTML = carrito.map((item, i) => `
    <div class="carrito-item">
      <span class="carrito-item-nombre">${item.nombre}</span>
      <span class="carrito-item-precio">${fmt(item.precio)}</span>
      <button class="btn-quitar" data-idx="${i}">✕</button>
    </div>`).join('');

  const total = carrito.reduce((s, i) => s + i.precio, 0);
  if (document.getElementById('total-valor'))
    document.getElementById('total-valor').textContent = fmt(total);
  if (totalBox) totalBox.style.display = 'flex';
  if (btnPedir) btnPedir.disabled = false;

  document.querySelectorAll('.btn-quitar').forEach(btn =>
    btn.addEventListener('click', () => { carrito.splice(+btn.dataset.idx, 1); renderCarrito(); })
  );
}

document.querySelectorAll('.btn-agregar:not(.btn-agregar-off)').forEach(btn => {
  btn.addEventListener('click', () => {
    carrito.push({ id: btn.dataset.id, nombre: btn.dataset.nombre, precio: +btn.dataset.precio });
    renderCarrito();
    showToast('+ ' + btn.dataset.nombre + ' agregada');
    btn.textContent = '✓ Agregado';
    btn.style.cssText = 'background:var(--rojo);color:white;border-color:var(--rojo)';
    setTimeout(() => { btn.textContent = '+ Agregar'; btn.style.cssText = ''; }, 1400);
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

/* ── GENERAR CODIGO PEDIDO ── */
function generarCodigo() {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  let codigo = 'OL-';
  for (let i = 0; i < 6; i++) codigo += chars[Math.floor(Math.random() * chars.length)];
  return codigo;
}

/* ── FORM: redirigir a WhatsApp ── */
const formPedido = document.getElementById('form-pedido');
if (formPedido) {
  formPedido.addEventListener('submit', e => {
    e.preventDefault();
    if (!carrito.length) { showToast('Agrega al menos una pizza primero!'); return; }

    const nombre    = document.getElementById('nombre').value.trim();
    const telefono  = document.getElementById('telefono').value.trim();
    const codigo    = generarCodigo();
    const total     = carrito.reduce((s, i) => s + i.precio, 0);
    // Agrupar pizzas repetidas
    const agrupado = {};
    carrito.forEach(i => {
      if (agrupado[i.nombre]) {
        agrupado[i.nombre].cantidad++;
        agrupado[i.nombre].subtotal += i.precio;
      } else {
        agrupado[i.nombre] = { cantidad: 1, precio: i.precio, subtotal: i.precio };
      }
    });
    const items = Object.entries(agrupado).map(([nombre, d]) =>
      d.cantidad > 1
        ? `- ${d.cantidad}x ${nombre}: ${fmt(d.subtotal)}`
        : `- ${nombre}: ${fmt(d.precio)}`
    ).join('\n');

    const mensaje =
`🍕 *NUEVO PEDIDO ${codigo}*

💰 Total: *${fmt(total)}*
👤 ${nombre}
📞 ${telefono}
📍 Retiro en local: Roque Esteban Scarpa 2125, Colina

*Pizzas:*
${items}

_Esperando confirmacion y datos de transferencia_`;

    guardarPedido(codigo, nombre, telefono, carrito, total);
    const url = 'https://wa.me/56939629467?text=' + encodeURIComponent(mensaje);
    window.open(url, '_blank');
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

/* ── Guardar pedido en BD al enviar a WhatsApp ── */
async function guardarPedido(codigo, nombre, telefono, items, total) {
  try {
    await fetch('/api/pedido', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ codigo, nombre, telefono, items, total })
    });
  } catch(e) { console.log('Error guardando pedido:', e); }
}

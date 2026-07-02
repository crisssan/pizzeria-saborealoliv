/* ── NAV scroll ── */
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => nav.classList.toggle('scrolled', window.scrollY > 60));

/* ── FILTROS menú ── */
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

function fmt(n) { return '$' + n.toLocaleString('es-CL'); }

function renderCarrito() {
  const lista    = document.getElementById('carrito-items');
  const totalBox = document.getElementById('carrito-total');
  if (carrito.length === 0) {
    lista.innerHTML = '<p class="carrito-vacio">Aún no has agregado nada. Explora el menú arriba ↑</p>';
    totalBox.style.display = 'none'; return;
  }
  lista.innerHTML = carrito.map((item, i) => `
    <div class="carrito-item">
      <span class="carrito-item-nombre">${item.nombre}</span>
      <span class="carrito-item-precio">${fmt(item.precio)}</span>
      <button class="btn-quitar" data-idx="${i}" title="Quitar">✕</button>
    </div>`).join('');
  const total = carrito.reduce((s, i) => s + i.precio, 0);
  document.getElementById('total-valor').textContent = fmt(total);
  totalBox.style.display = 'flex';
  document.querySelectorAll('.btn-quitar').forEach(btn =>
    btn.addEventListener('click', () => { carrito.splice(+btn.dataset.idx, 1); renderCarrito(); })
  );
}

document.querySelectorAll('.btn-agregar').forEach(btn => {
  btn.addEventListener('click', () => {
    carrito.push({ id: btn.dataset.id, nombre: btn.dataset.nombre, precio: +btn.dataset.precio });
    renderCarrito();
    showToast(`✓ ${btn.dataset.nombre} agregada`);
    btn.textContent = '✓';
    btn.style.cssText = 'background:var(--red);color:var(--white)';
    setTimeout(() => { btn.textContent = 'Agregar'; btn.style.cssText = ''; }, 1200);
  });
});

/* ── TOAST ── */
let toastTimer;
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 2400);
}

/* ── FORM: crear pedido → redirigir a pago ── */
document.getElementById('form-pedido').addEventListener('submit', async e => {
  e.preventDefault();
  if (!carrito.length) { showToast('¡Agrega al menos una pizza primero!'); return; }

  const btn = document.getElementById('btn-pedido');
  btn.disabled = true; btn.textContent = 'Creando pedido…';

  try {
    const res  = await fetch('/api/pedido', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        nombre:    document.getElementById('nombre').value,
        telefono:  document.getElementById('telefono').value,
        direccion: document.getElementById('direccion').value,
        items: carrito,
        total: carrito.reduce((s, i) => s + i.precio, 0)
      })
    });
    const data = await res.json();
    if (data.ok) { window.location.href = data.pago_url; }
    else { showToast('Error: ' + (data.error || 'intenta de nuevo')); }
  } catch { showToast('Error de conexión. Intenta de nuevo.'); }
  finally { btn.disabled = false; btn.textContent = 'Ir a pagar 🔥'; }
});

/* ── WHATSAPP FLOTANTE ── */
(function() {
  const NUMERO  = '56939629467'; // sin + ni espacios
  const MENSAJE_ABIERTO  = '¡Hola! Quiero hacer un pedido 🍕🔥';
  const MENSAJE_AUSENCIA = '¡Hola! Vi su página y quiero hacer un pedido. ¿Cuándo están disponibles?';

  // Horario: Lun-Dom 12:00-23:00
  function estaAbierto() {
    const now  = new Date();
    const hora = now.getHours();
    return hora >= 12 && hora < 23;
  }

  const abierto  = estaAbierto();
  const mensaje  = encodeURIComponent(abierto ? MENSAJE_ABIERTO : MENSAJE_AUSENCIA);
  const urlWsp   = `https://wa.me/${NUMERO}?text=${mensaje}`;

  const fab      = document.getElementById('wsp-fab');
  const popup    = document.getElementById('wsp-popup');
  const cerrar   = document.getElementById('wsp-cerrar');
  const badge    = document.getElementById('wsp-badge');
  const ausencia = document.getElementById('wsp-ausencia');
  const btnChat  = document.getElementById('wsp-btn-chat');
  const estadoEl = popup.querySelector('.wsp-estado');

  // Mostrar mensaje de ausencia si está cerrado
  if (!abierto) {
    ausencia.style.display = 'block';
    estadoEl.textContent   = '🔴 Ahora cerrado';
  }

  btnChat.href = urlWsp;

  // Abrir popup automáticamente después de 4 segundos
  setTimeout(() => {
    popup.classList.add('visible');
    badge.style.display = 'none';
  }, 4000);

  fab.addEventListener('click', () => {
    const visible = popup.classList.contains('visible');
    popup.classList.toggle('visible', !visible);
    badge.style.display = 'none';
  });

  cerrar.addEventListener('click', e => {
    e.stopPropagation();
    popup.classList.remove('visible');
  });
})();

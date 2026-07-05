const ICONOS = { recibido:'📋', preparando:'👨‍🍳', en_horno:'🔥', listo:'✅', entregado:'🍕' };
const TIEMPOS = { recibido:'Confirmando tu pedido…', preparando:'Preparando tus ingredientes frescos…', en_horno:'En el horno, casi lista!', listo:'Tu pizza esta lista! Puedes venir a buscarla ✅', entregado:'Gracias por elegirnos. Buen provecho! 🍕' };

let ultimoEstado = null;
let intervalo;

function fmt(n) { return '$' + Number(n).toLocaleString('es-CL'); }

function actualizarTracker(idx) {
  const steps = document.querySelectorAll('.step');
  steps.forEach((s, i) => {
    s.classList.remove('done', 'active');
    if (i < idx)  s.classList.add('done');
    if (i === idx) s.classList.add('active');
  });
  // Barra de progreso: de 0 a 100 en 4 pasos
  const pct = idx === 0 ? 0 : (idx / (steps.length - 1)) * 100;
  document.getElementById('tracker-progress').style.width = pct + '%';
}

async function poll() {
  try {
    const res  = await fetch(`/api/pedido/${CODIGO}/estado`);
    const data = await res.json();
    if (!data.ok) return;

    // Header
    document.getElementById('seg-nombre').textContent = `Pedido de ${data.nombre}`;

    // Tracker
    actualizarTracker(data.estado_idx);

    // Estado actual
    document.getElementById('estado-icon').textContent  = ICONOS[data.estado] || '⏳';
    document.getElementById('estado-label').textContent = data.estado_label;
    document.getElementById('estado-tiempo').textContent = TIEMPOS[data.estado] || '';

    // Items (solo primera vez)
    if (!ultimoEstado) {
      const cont = document.getElementById('seg-items');
      cont.innerHTML = data.items.map(it =>
        `<div class="seg-item"><span>${it.nombre}</span><span class="seg-item-precio">${fmt(it.precio)}</span></div>`
      ).join('');
      document.getElementById('seg-total').innerHTML =
        `<span>Total pagado</span><span>${fmt(data.total)}</span>`;
    }

    // Si entregado, dejar de hacer polling
    if (data.estado === 'entregado') clearInterval(intervalo);
    ultimoEstado = data.estado;

  } catch(e) { console.error('Error polling:', e); }
}

poll();
intervalo = setInterval(poll, 8000); // cada 8 segundos

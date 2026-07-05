function showToast(msg, ok) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.style.borderColor = ok ? 'var(--gold)' : 'var(--red)';
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2800);
}

async function cambiarEstado(codigo, nuevoEstado, btnEl) {
  // Deshabilitar todos los botones de esta card
  const card = document.getElementById('card-' + codigo);
  const btns = card.querySelectorAll('.btn-estado');
  btns.forEach(b => b.classList.add('cargando'));

  try {
    const res  = await fetch(`/admin/pedido/${codigo}/estado`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ estado: nuevoEstado })
    });
    const data = await res.json();

    if (data.ok) {
      // Actualizar botones
      btns.forEach(b => {
        b.classList.remove('activo', 'cargando');
        if (b.dataset.estado === nuevoEstado) b.classList.add('activo');
      });
      // Actualizar label
      document.getElementById('label-' + codigo).textContent = data.label;
      // Resaltar card
      card.classList.add('actualizado');
      setTimeout(() => card.classList.remove('actualizado'), 2000);
      showToast('Estado actualizado y WhatsApp enviado al cliente', true);
    } else {
      btns.forEach(b => b.classList.remove('cargando'));
      showToast('Error al actualizar', false);
    }
  } catch {
    btns.forEach(b => b.classList.remove('cargando'));
    showToast('Error de conexion', false);
  }
}

// Auto-refresh cada 60 segundos para ver pedidos nuevos
setTimeout(() => location.reload(), 60000);

/* ── BOTON CERRAR/ABRIR TIENDA ── */
const btnTienda = document.getElementById('btn-tienda');
if (btnTienda) {
  btnTienda.addEventListener('click', async () => {
    const estadoActual = btnTienda.dataset.estado;
    const cerrando = estadoActual === 'abierta';

    const confirmMsg = cerrando
      ? '¿Seguro que quieres CERRAR la tienda?\nNo se recibirán más pedidos hasta que la abras de nuevo.'
      : '¿Seguro que quieres ABRIR la tienda?\nLos clientes podrán hacer pedidos.';

    if (!confirm(confirmMsg)) return;

    const accion = cerrando ? 'cerrar' : 'abrir';
    try {
      const res  = await fetch('/admin/tienda', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ accion })
      });
      const data = await res.json();
      if (data.ok) {
        const badge = document.getElementById('tienda-badge');
        if (data.abierta) {
          btnTienda.textContent = '🟢 Cerrar tienda';
          btnTienda.className   = 'btn-tienda btn-tienda-cerrar';
          btnTienda.dataset.estado = 'abierta';
          badge.textContent    = '✅ Tienda abierta — recibiendo pedidos';
          badge.className      = 'tienda-badge tienda-abierta';
          showToast('Tienda abierta ✅', true);
        } else {
          btnTienda.textContent = '🔴 Abrir tienda';
          btnTienda.className   = 'btn-tienda btn-tienda-abrir';
          btnTienda.dataset.estado = 'cerrada';
          badge.textContent    = '⛔ Tienda cerrada — no se reciben pedidos';
          badge.className      = 'tienda-badge tienda-cerrada';
          showToast('Tienda cerrada ⛔', true);
        }
      }
    } catch { showToast('Error de conexion', false); }
  });
}

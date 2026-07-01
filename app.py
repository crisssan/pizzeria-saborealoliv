<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Seguimiento — Forno Nero</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/static/css/style.css">
  <link rel="stylesheet" href="/static/css/seguimiento.css">
</head>
<body class="page-seguimiento">

  <nav class="nav scrolled">
    <div class="nav-inner">
      <a href="/" class="logo">Forno Nero</a>
    </div>
  </nav>

  <main class="seguimiento-main">
    <div class="seguimiento-card">
      <div class="seg-header">
        <p class="eyebrow">Estado de tu pedido</p>
        <h1 id="seg-codigo">{{ codigo }}</h1>
        <p id="seg-nombre" class="seg-cliente"></p>
      </div>

      <!-- TRACKER -->
      <div class="tracker">
        <div class="tracker-steps" id="tracker-steps">
          <div class="step" data-idx="0"><div class="step-dot"></div><div class="step-label">Recibido</div></div>
          <div class="step" data-idx="1"><div class="step-dot"></div><div class="step-label">Preparando</div></div>
          <div class="step" data-idx="2"><div class="step-dot"></div><div class="step-label">En el horno</div></div>
          <div class="step" data-idx="3"><div class="step-dot"></div><div class="step-label">En camino</div></div>
          <div class="step" data-idx="4"><div class="step-dot"></div><div class="step-label">Entregado</div></div>
        </div>
        <div class="tracker-bar"><div class="tracker-progress" id="tracker-progress"></div></div>
      </div>

      <div class="estado-actual" id="estado-actual">
        <div class="estado-icon" id="estado-icon">⏳</div>
        <div>
          <p class="estado-label" id="estado-label">Cargando…</p>
          <p class="estado-tiempo" id="estado-tiempo"></p>
        </div>
      </div>

      <!-- Resumen items -->
      <div class="seg-items" id="seg-items"></div>

      <div class="seg-total" id="seg-total"></div>

      <a href="/" class="btn-volver">← Volver al inicio</a>
    </div>
  </main>

  <script>
    const CODIGO = "{{ codigo }}";
  </script>
  <script src="/static/js/seguimiento.js"></script>
</body>
</html>

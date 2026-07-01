<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Forno Nero — Pizzería Artesanal</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Inter:wght@300;400;500&family=Cormorant+Garamond:ital,wght@1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>

  <nav class="nav" id="nav">
    <div class="nav-inner">
      <a href="#" class="logo">Forno Nero</a>
      <ul class="nav-links">
        <li><a href="#menu">Menú</a></li>
        <li><a href="#historia">Nosotros</a></li>
        <li><a href="#pedido" class="btn-nav">Pedir ahora</a></li>
      </ul>
    </div>
  </nav>

  <section class="hero">
    <div class="fire-container">
      <div class="flame flame-1"></div><div class="flame flame-2"></div><div class="flame flame-3"></div>
      <div class="ember ember-1"></div><div class="ember ember-2"></div><div class="ember ember-3"></div>
    </div>
    <div class="hero-content">
      <p class="hero-eyebrow">Horno de leña · Masa madre · 72 horas de fermentación</p>
      <h1 class="hero-title">Pizza que<br><em>vale la espera</em></h1>
      <p class="hero-sub">Elaboramos cada pizza con ingredientes seleccionados y técnica napolitana auténtica. Sin atajos, sin prisa.</p>
      <a href="#menu" class="btn-hero">Ver carta</a>
    </div>
    <div class="hero-scroll">↓</div>
  </section>

  <section class="pilares">
    <div class="container">
      <div class="pilar"><span class="pilar-icon">🌾</span><h3>Masa madre</h3><p>Fermentada 72 horas para una digestión perfecta y sabor profundo</p></div>
      <div class="pilar"><span class="pilar-icon">🔥</span><h3>Horno de leña</h3><p>450°C durante 90 segundos. El único método que logra esa costra perfecta</p></div>
      <div class="pilar"><span class="pilar-icon">🇮🇹</span><h3>Ingredientes DOC</h3><p>Tomate San Marzano, mozzarella fior di latte, aceite de oliva de origen</p></div>
    </div>
  </section>

  <section class="menu-section" id="menu">
    <div class="container">
      <div class="section-header"><p class="eyebrow">La carta</p><h2>Nuestras pizzas</h2></div>
      <div class="filtros">
        <button class="filtro activo" data-cat="todas">Todas</button>
        <button class="filtro" data-cat="clásica">Clásicas</button>
        <button class="filtro" data-cat="especial">Especiales</button>
        <button class="filtro" data-cat="gourmet">Gourmet</button>
      </div>
      <div class="menu-grid">
        {% for pizza in menu %}
        <article class="pizza-card" data-cat="{{ pizza.categoria }}">
          <div class="pizza-emoji">{{ pizza.emoji }}</div>
          <div class="pizza-info">
            <div class="pizza-header">
              <h3>{{ pizza.nombre }}</h3>
              <span class="badge-cat">{{ pizza.categoria }}</span>
            </div>
            <p class="pizza-desc">{{ pizza.descripcion }}</p>
            <div class="pizza-footer">
              <span class="pizza-precio">${{ "{:,.0f}".format(pizza.precio).replace(",", ".") }}</span>
              <button class="btn-agregar" data-id="{{ pizza.id }}" data-nombre="{{ pizza.nombre }}" data-precio="{{ pizza.precio }}">Agregar</button>
            </div>
          </div>
        </article>
        {% endfor %}
      </div>
    </div>
  </section>

  <section class="historia" id="historia">
    <div class="container historia-inner">
      <div class="historia-texto">
        <p class="eyebrow">Nuestra historia</p>
        <h2>Nació en un viaje a Nápoles</h2>
        <p>En 2018, Marco Ferrante viajó a la cuna de la pizza y volvió obsesionado con la simplicidad. No con recetas complicadas, sino con la idea de que buenos ingredientes y técnica honesta son todo lo que se necesita.</p>
        <p>Forno Nero abrió en 2020 en Santiago con un solo horno de leña importado directamente de Cava de' Tirreni. Hoy seguimos haciendo lo mismo: una masa, un horno, mucho tiempo.</p>
        <div class="stats">
          <div class="stat"><span class="stat-num">72h</span><span class="stat-label">Fermentación</span></div>
          <div class="stat"><span class="stat-num">450°</span><span class="stat-label">Temperatura</span></div>
          <div class="stat"><span class="stat-num">6</span><span class="stat-label">Pizzas en carta</span></div>
        </div>
      </div>
      <div class="historia-img">
        <div class="horno-visual">
          <div class="horno-mouth"><div class="horno-fire">🔥</div></div>
          <div class="horno-text">Horno napolitano<br><em>desde 2020</em></div>
        </div>
      </div>
    </div>
  </section>

  <section class="pedido-section" id="pedido">
    <div class="container">
      <div class="section-header"><p class="eyebrow">Tu pedido</p><h2>¿Qué llevas hoy?</h2></div>
      <div class="pedido-layout">
        <div class="carrito-box">
          <h3>Tu carrito</h3>
          <div id="carrito-items">
            <p class="carrito-vacio">Aún no has agregado nada. Explora el menú arriba ↑</p>
          </div>
          <div class="carrito-total" id="carrito-total" style="display:none">
            <span>Total</span><span id="total-valor">$0</span>
          </div>
        </div>
        <form class="form-pedido" id="form-pedido">
          <h3>Tus datos</h3>
          <div class="campo"><label for="nombre">Nombre</label><input type="text" id="nombre" placeholder="¿Cómo te llamamos?" required></div>
          <div class="campo"><label for="telefono">Teléfono</label><input type="tel" id="telefono" placeholder="+56 9 XXXX XXXX" required></div>
          <div class="campo"><label for="direccion">Dirección de entrega</label><input type="text" id="direccion" placeholder="Calle, número, comuna" required></div>
          <button type="submit" class="btn-pedido" id="btn-pedido">Ir a pagar 🔥</button>
        </form>
      </div>
    </div>
  </section>

  <div class="toast" id="toast"></div>

  <!-- BOTÓN FLOTANTE WHATSAPP -->
  <div class="wsp-container" id="wsp-container">
    <div class="wsp-popup" id="wsp-popup">
      <div class="wsp-popup-header">
        <div class="wsp-avatar">🍕</div>
        <div>
          <p class="wsp-nombre">Forno Nero</p>
          <p class="wsp-estado">🟢 En línea ahora</p>
        </div>
        <button class="wsp-cerrar" id="wsp-cerrar">✕</button>
      </div>
      <div class="wsp-popup-body">
        <div class="wsp-burbuja">
          👋 ¡Hola! Bienvenido a <strong>Forno Nero</strong>.<br><br>
          Estamos aquí para tomar tu pedido 🍕🔥<br><br>
          <em>Horario: Lun–Dom 12:00–23:00</em>
        </div>
        <div class="wsp-burbuja wsp-ausencia" id="wsp-ausencia" style="display:none">
          😴 Ahora estamos cerrados, pero escríbenos y te respondemos apenas abramos.
        </div>
      </div>
      <a class="wsp-btn-chat" id="wsp-btn-chat" href="#" target="_blank">
        Iniciar chat →
      </a>
    </div>
    <button class="wsp-fab" id="wsp-fab" title="Escríbenos por WhatsApp">
      <svg viewBox="0 0 24 24" fill="white" width="28" height="28">
        <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
        <path d="M12 0C5.373 0 0 5.373 0 12c0 2.117.549 4.107 1.51 5.833L.057 23.077a.75.75 0 00.866.866l5.244-1.453A11.953 11.953 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.75a9.715 9.715 0 01-4.953-1.355l-.355-.21-3.676 1.018 1.018-3.676-.21-.355A9.715 9.715 0 012.25 12C2.25 6.615 6.615 2.25 12 2.25S21.75 6.615 21.75 12 17.385 21.75 12 21.75z"/>
      </svg>
      <span class="wsp-badge" id="wsp-badge">1</span>
    </button>
  </div>

  <footer class="footer">
    <div class="container">
      <p class="footer-logo">Forno Nero</p>
      <p>Av. Italia 1247, Providencia · Lun–Dom 12:00–23:00</p>
      <p>+56 9 8765 4321 · hola@fornonero.cl</p>
      <p class="footer-copy">© 2025 Forno Nero. Hecho con 🔥 y masa madre.</p>
    </div>
  </footer>

  <script src="/static/js/app.js"></script>
</body>
</html>

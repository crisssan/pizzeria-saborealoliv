/* ── TOKENS ── */
:root {
  --carbon:  #1A1A1A;
  --smoke:   #2D2D2D;
  --charcoal:#3D3D3D;
  --cream:   #F5EDD6;
  --cream2:  #EDE0C4;
  --red:     #C0392B;
  --red-dark:#96281B;
  --gold:    #E8A838;
  --gold-lt: #F2C56A;
  --white:   #FDFAF4;
  --text-lt: rgba(245,237,214,0.7);

  --ff-display: 'Playfair Display', Georgia, serif;
  --ff-body:    'Inter', system-ui, sans-serif;
  --ff-italic:  'Cormorant Garamond', Georgia, serif;

  --r: 4px;
  --transition: 0.25s ease;
}

/* ── RESET ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: var(--ff-body);
  background: var(--carbon);
  color: var(--cream);
  line-height: 1.6;
  overflow-x: hidden;
}
a { text-decoration: none; color: inherit; }
img { display: block; max-width: 100%; }
button { cursor: pointer; font-family: var(--ff-body); border: none; }

/* ── LAYOUT ── */
.container { max-width: 1100px; margin: 0 auto; padding: 0 24px; }

/* ── NAV ── */
.nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  padding: 20px 0;
  transition: background var(--transition), padding var(--transition);
}
.nav.scrolled {
  background: rgba(26,26,26,0.97);
  backdrop-filter: blur(12px);
  padding: 12px 0;
  border-bottom: 1px solid var(--charcoal);
}
.nav-inner {
  max-width: 1100px; margin: 0 auto; padding: 0 24px;
  display: flex; align-items: center; justify-content: space-between;
}
.logo {
  font-family: var(--ff-display);
  font-size: 1.5rem; font-weight: 900;
  color: var(--gold);
  letter-spacing: -0.02em;
}
.nav-links {
  list-style: none; display: flex; gap: 32px; align-items: center;
}
.nav-links a {
  font-size: 0.875rem; font-weight: 400; letter-spacing: 0.04em;
  color: var(--cream); opacity: 0.8;
  transition: opacity var(--transition);
}
.nav-links a:hover { opacity: 1; }
.btn-nav {
  background: var(--red);
  color: var(--white) !important; opacity: 1 !important;
  padding: 8px 20px; border-radius: var(--r);
  font-weight: 500; font-size: 0.875rem;
  transition: background var(--transition);
}
.btn-nav:hover { background: var(--red-dark); }

/* ── HERO ── */
.hero {
  position: relative; min-height: 100vh;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
  background: radial-gradient(ellipse at 50% 80%, #3D1A0A 0%, #1A0A05 40%, var(--carbon) 100%);
}

/* Flames */
.fire-container {
  position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);
  width: 600px; height: 300px;
  pointer-events: none;
}
.flame {
  position: absolute; bottom: 0;
  border-radius: 50% 50% 30% 30%;
  filter: blur(8px);
  animation: flicker 1.8s ease-in-out infinite alternate;
  transform-origin: bottom center;
}
.flame-1 {
  width: 120px; height: 200px; left: 50%; transform: translateX(-50%);
  background: radial-gradient(ellipse at 50% 100%, #FF6B00, #FF3D00, transparent);
  animation-duration: 1.4s;
}
.flame-2 {
  width: 80px; height: 150px; left: 42%; transform: translateX(-50%);
  background: radial-gradient(ellipse at 50% 100%, #FFD700, #FF6B00, transparent);
  animation-duration: 1.9s; animation-delay: 0.3s;
}
.flame-3 {
  width: 90px; height: 170px; left: 58%; transform: translateX(-50%);
  background: radial-gradient(ellipse at 50% 100%, #FF8C00, #FF4500, transparent);
  animation-duration: 1.6s; animation-delay: 0.7s;
}
.ember {
  position: absolute;
  width: 4px; height: 4px; border-radius: 50%;
  background: var(--gold);
  animation: rise 2.5s ease-in infinite;
}
.ember-1 { left: 45%; bottom: 120px; animation-delay: 0.5s; }
.ember-2 { left: 52%; bottom: 100px; animation-delay: 1.1s; }
.ember-3 { left: 48%; bottom: 140px; animation-delay: 1.8s; }

@keyframes flicker {
  0%   { transform: translateX(-50%) scaleX(1) scaleY(1); opacity: 0.9; }
  100% { transform: translateX(-50%) scaleX(0.85) scaleY(1.1); opacity: 1; }
}
@keyframes rise {
  0%   { opacity: 1; transform: translateY(0) scale(1); }
  100% { opacity: 0; transform: translateY(-200px) scale(0.3) translateX(30px); }
}

.hero-content {
  position: relative; z-index: 2;
  text-align: center; max-width: 720px; padding: 0 24px;
  padding-bottom: 120px;
}
.hero-eyebrow {
  font-size: 0.75rem; font-weight: 500; letter-spacing: 0.15em;
  text-transform: uppercase; color: var(--gold); margin-bottom: 20px;
}
.hero-title {
  font-family: var(--ff-display);
  font-size: clamp(3rem, 8vw, 6rem);
  font-weight: 900; line-height: 1.05;
  color: var(--white); margin-bottom: 20px;
  letter-spacing: -0.03em;
}
.hero-title em {
  font-family: var(--ff-italic);
  font-style: italic; font-weight: 400;
  color: var(--gold-lt);
}
.hero-sub {
  font-size: 1.05rem; font-weight: 300;
  color: var(--text-lt); max-width: 480px; margin: 0 auto 36px;
}
.btn-hero {
  display: inline-block;
  background: var(--red); color: var(--white);
  padding: 14px 36px; border-radius: var(--r);
  font-weight: 500; font-size: 0.95rem; letter-spacing: 0.04em;
  transition: background var(--transition), transform var(--transition);
}
.btn-hero:hover { background: var(--red-dark); transform: translateY(-2px); }

.hero-scroll {
  position: absolute; bottom: 32px; left: 50%;
  transform: translateX(-50%);
  color: var(--text-lt); font-size: 1.2rem;
  animation: bounce 2s ease-in-out infinite;
}
@keyframes bounce {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50%       { transform: translateX(-50%) translateY(8px); }
}

/* ── PILARES ── */
.pilares {
  background: var(--smoke);
  border-top: 1px solid var(--charcoal);
  border-bottom: 1px solid var(--charcoal);
  padding: 64px 0;
}
.pilares .container {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 48px;
}
.pilar { text-align: center; }
.pilar-icon { font-size: 2rem; display: block; margin-bottom: 12px; }
.pilar h3 {
  font-family: var(--ff-display); font-size: 1.15rem; font-weight: 700;
  color: var(--gold); margin-bottom: 8px;
}
.pilar p { font-size: 0.875rem; color: var(--text-lt); line-height: 1.6; }

/* ── SECTION HEADER ── */
.section-header { text-align: center; margin-bottom: 48px; }
.eyebrow {
  font-size: 0.7rem; font-weight: 500; letter-spacing: 0.18em;
  text-transform: uppercase; color: var(--gold); margin-bottom: 10px;
}
.section-header h2 {
  font-family: var(--ff-display); font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 900; color: var(--white); letter-spacing: -0.02em;
}

/* ── MENU ── */
.menu-section { padding: 96px 0; }

.filtros {
  display: flex; gap: 10px; justify-content: center; margin-bottom: 48px; flex-wrap: wrap;
}
.filtro {
  background: transparent; border: 1px solid var(--charcoal);
  color: var(--text-lt); padding: 8px 20px; border-radius: 100px;
  font-size: 0.8rem; letter-spacing: 0.06em; font-weight: 500;
  transition: all var(--transition);
}
.filtro:hover, .filtro.activo {
  background: var(--red); border-color: var(--red); color: var(--white);
}

.menu-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px;
}
.pizza-card {
  display: flex; gap: 16px;
  background: var(--smoke); border: 1px solid var(--charcoal);
  border-radius: 8px; padding: 20px;
  transition: border-color var(--transition), transform var(--transition);
}
.pizza-card:hover { border-color: var(--gold); transform: translateY(-2px); }
.pizza-card.oculta { display: none; }

.pizza-emoji { font-size: 2.4rem; flex-shrink: 0; line-height: 1; padding-top: 2px; }
.pizza-info { flex: 1; }
.pizza-header { display: flex; align-items: flex-start; gap: 8px; margin-bottom: 6px; }
.pizza-header h3 {
  font-family: var(--ff-display); font-size: 1.05rem; font-weight: 700;
  color: var(--white); flex: 1;
}
.badge-cat {
  font-size: 0.65rem; font-weight: 500; letter-spacing: 0.08em;
  text-transform: uppercase; padding: 2px 8px; border-radius: 100px;
  background: var(--charcoal); color: var(--text-lt); white-space: nowrap;
  margin-top: 3px;
}
.pizza-desc { font-size: 0.8rem; color: var(--text-lt); line-height: 1.55; margin-bottom: 14px; }
.pizza-footer { display: flex; align-items: center; justify-content: space-between; }
.pizza-precio {
  font-family: var(--ff-display); font-size: 1.15rem; font-weight: 700; color: var(--gold);
}
.btn-agregar {
  background: transparent; border: 1px solid var(--red); color: var(--red);
  padding: 6px 16px; border-radius: var(--r); font-size: 0.8rem; font-weight: 500;
  transition: all var(--transition);
}
.btn-agregar:hover { background: var(--red); color: var(--white); }

/* ── HISTORIA ── */
.historia { padding: 96px 0; background: var(--smoke); }
.historia-inner { display: grid; grid-template-columns: 1fr 1fr; gap: 80px; align-items: center; }
.historia-texto .eyebrow { text-align: left; display: block; margin-bottom: 10px; }
.historia-texto h2 {
  font-family: var(--ff-display); font-size: clamp(1.8rem, 3.5vw, 2.5rem);
  font-weight: 900; letter-spacing: -0.02em; color: var(--white); margin-bottom: 20px;
}
.historia-texto p { font-size: 0.9rem; color: var(--text-lt); line-height: 1.75; margin-bottom: 16px; }
.stats { display: flex; gap: 32px; margin-top: 32px; }
.stat { display: flex; flex-direction: column; }
.stat-num {
  font-family: var(--ff-display); font-size: 2rem; font-weight: 900; color: var(--gold); line-height: 1;
}
.stat-label { font-size: 0.75rem; color: var(--text-lt); letter-spacing: 0.06em; margin-top: 4px; }

/* Horno visual */
.horno-visual {
  width: 100%; aspect-ratio: 1;
  max-width: 360px; margin: 0 auto;
  background: radial-gradient(ellipse at 50% 100%, #3D1A0A 0%, var(--carbon) 70%);
  border: 2px solid var(--charcoal); border-radius: 50% 50% 8px 8px;
  display: flex; flex-direction: column; align-items: center; justify-content: flex-end;
  padding-bottom: 32px; position: relative; overflow: hidden;
}
.horno-mouth {
  width: 120px; height: 80px;
  background: #0A0400; border-radius: 50% 50% 0 0;
  border: 2px solid #5A3010; border-bottom: none;
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 16px;
}
.horno-fire { font-size: 2.5rem; animation: flicker-emoji 1s ease-in-out infinite alternate; }
@keyframes flicker-emoji {
  0%   { transform: scale(1); }
  100% { transform: scale(1.15) translateY(-4px); }
}
.horno-text {
  font-size: 0.8rem; color: var(--text-lt); text-align: center; letter-spacing: 0.06em;
}
.horno-text em { font-family: var(--ff-italic); font-style: italic; font-size: 0.9rem; color: var(--gold-lt); }

/* ── PEDIDO ── */
.pedido-section { padding: 96px 0; }
.pedido-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; margin-top: 48px; }

.carrito-box {
  background: var(--smoke); border: 1px solid var(--charcoal); border-radius: 8px; padding: 28px;
}
.carrito-box h3 {
  font-family: var(--ff-display); font-size: 1.2rem; font-weight: 700;
  color: var(--gold); margin-bottom: 20px; padding-bottom: 14px; border-bottom: 1px solid var(--charcoal);
}
.carrito-vacio { font-size: 0.85rem; color: var(--text-lt); text-align: center; padding: 32px 0; }
.carrito-item {
  display: flex; justify-content: space-between; align-items: center;
  padding: 10px 0; border-bottom: 1px solid var(--charcoal);
  font-size: 0.875rem;
}
.carrito-item-nombre { color: var(--cream); flex: 1; }
.carrito-item-precio { color: var(--gold); font-weight: 600; }
.btn-quitar {
  background: none; border: none; color: var(--charcoal); font-size: 1rem;
  margin-left: 12px; transition: color var(--transition);
}
.btn-quitar:hover { color: var(--red); }
.carrito-total {
  display: flex; justify-content: space-between; align-items: center;
  margin-top: 16px; padding-top: 16px;
  font-family: var(--ff-display); font-size: 1.15rem; font-weight: 700;
  color: var(--white); border-top: 1px solid var(--charcoal);
}
#total-valor { color: var(--gold); }

/* FORM */
.form-pedido {
  background: var(--smoke); border: 1px solid var(--charcoal); border-radius: 8px; padding: 28px;
}
.form-pedido h3 {
  font-family: var(--ff-display); font-size: 1.2rem; font-weight: 700;
  color: var(--gold); margin-bottom: 20px; padding-bottom: 14px; border-bottom: 1px solid var(--charcoal);
}
.campo { margin-bottom: 18px; }
.campo label {
  display: block; font-size: 0.75rem; font-weight: 500;
  letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-lt); margin-bottom: 7px;
}
.campo input {
  width: 100%; background: var(--carbon);
  border: 1px solid var(--charcoal); border-radius: var(--r);
  padding: 12px 14px; color: var(--cream); font-size: 0.9rem; font-family: var(--ff-body);
  transition: border-color var(--transition);
}
.campo input:focus { outline: none; border-color: var(--gold); }
.campo input::placeholder { color: var(--charcoal); }
.btn-pedido {
  width: 100%; background: var(--red); color: var(--white);
  padding: 14px; border-radius: var(--r); font-size: 1rem; font-weight: 600;
  letter-spacing: 0.03em; margin-top: 8px;
  transition: background var(--transition), transform var(--transition);
}
.btn-pedido:hover { background: var(--red-dark); transform: translateY(-1px); }
.btn-pedido:disabled { background: var(--charcoal); cursor: not-allowed; transform: none; }

/* ── TOAST ── */
.toast {
  position: fixed; bottom: 28px; left: 50%; transform: translateX(-50%) translateY(80px);
  background: var(--smoke); border: 1px solid var(--gold);
  color: var(--cream); padding: 14px 28px; border-radius: 6px;
  font-size: 0.9rem; font-weight: 500; z-index: 999;
  transition: transform 0.4s cubic-bezier(0.34,1.56,0.64,1);
  white-space: nowrap;
}
.toast.show { transform: translateX(-50%) translateY(0); }

/* ── FOOTER ── */
.footer {
  background: #111; border-top: 1px solid var(--charcoal);
  padding: 48px 0; text-align: center;
}
.footer-logo {
  font-family: var(--ff-display); font-size: 1.5rem; font-weight: 900;
  color: var(--gold); margin-bottom: 16px;
}
.footer p { font-size: 0.8rem; color: var(--text-lt); margin-bottom: 6px; line-height: 1.8; }
.footer-copy { margin-top: 24px; opacity: 0.5; }

/* ── RESPONSIVE ── */
@media (max-width: 768px) {
  .nav-links { display: none; }
  .pilares .container { grid-template-columns: 1fr; gap: 32px; }
  .menu-grid { grid-template-columns: 1fr; }
  .historia-inner { grid-template-columns: 1fr; }
  .horno-visual { display: none; }
  .pedido-layout { grid-template-columns: 1fr; }
  .stats { gap: 20px; }
}
@media (prefers-reduced-motion: reduce) {
  .flame, .ember, .hero-scroll, .horno-fire { animation: none; }
}

/* ── WHATSAPP FLOTANTE ── */
.wsp-container {
  position: fixed; bottom: 28px; right: 28px; z-index: 200;
  display: flex; flex-direction: column; align-items: flex-end; gap: 12px;
}

/* FAB */
.wsp-fab {
  width: 60px; height: 60px; border-radius: 50%;
  background: #25D366; border: none; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 20px rgba(37,211,102,0.5);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  position: relative;
}
.wsp-fab:hover { transform: scale(1.08); box-shadow: 0 6px 28px rgba(37,211,102,0.6); }
.wsp-badge {
  position: absolute; top: -4px; right: -4px;
  background: var(--red); color: white;
  width: 20px; height: 20px; border-radius: 50%;
  font-size: 0.7rem; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  animation: bounce-badge 1.5s ease-in-out infinite;
}
@keyframes bounce-badge {
  0%, 100% { transform: scale(1); }
  50%       { transform: scale(1.2); }
}

/* POPUP */
.wsp-popup {
  width: 300px;
  background: var(--smoke); border: 1px solid var(--charcoal);
  border-radius: 12px; overflow: hidden;
  box-shadow: 0 8px 32px rgba(0,0,0,0.4);
  transform: scale(0.8) translateY(20px);
  transform-origin: bottom right;
  opacity: 0; pointer-events: none;
  transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1);
}
.wsp-popup.visible { transform: scale(1) translateY(0); opacity: 1; pointer-events: all; }

.wsp-popup-header {
  background: #075E54; padding: 14px 16px;
  display: flex; align-items: center; gap: 10px;
}
.wsp-avatar {
  width: 40px; height: 40px; border-radius: 50%;
  background: #25D366; display: flex; align-items: center;
  justify-content: center; font-size: 1.3rem; flex-shrink: 0;
}
.wsp-nombre { font-size: 0.9rem; font-weight: 600; color: white; }
.wsp-estado { font-size: 0.72rem; color: rgba(255,255,255,0.75); margin-top: 2px; }
.wsp-cerrar {
  margin-left: auto; background: none; border: none;
  color: rgba(255,255,255,0.7); font-size: 1rem; cursor: pointer;
  padding: 4px; transition: color 0.2s;
}
.wsp-cerrar:hover { color: white; }

.wsp-popup-body { padding: 16px; background: #ECE5DD; }
.wsp-burbuja {
  background: white; border-radius: 8px 8px 8px 0;
  padding: 12px 14px; font-size: 0.82rem; color: #303030;
  line-height: 1.55; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  margin-bottom: 8px;
}
.wsp-ausencia { background: #FFF8E1; }

.wsp-btn-chat {
  display: block; background: #25D366; color: white;
  text-align: center; padding: 13px;
  font-weight: 600; font-size: 0.9rem;
  transition: background 0.2s;
}
.wsp-btn-chat:hover { background: #1DA851; }

@media (max-width: 400px) {
  .wsp-container { bottom: 16px; right: 16px; }
  .wsp-popup { width: 260px; }
}

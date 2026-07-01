.page-seguimiento { background: var(--carbon); min-height: 100vh; }

.seguimiento-main {
  max-width: 640px; margin: 0 auto;
  padding: 100px 24px 60px;
}
.seguimiento-card {
  background: var(--smoke); border: 1px solid var(--charcoal); border-radius: 12px; padding: 40px 36px;
}
.seg-header { text-align: center; margin-bottom: 40px; }
.seg-header .eyebrow { margin-bottom: 8px; }
.seg-header h1 { font-family: var(--ff-display); font-size: 2rem; color: var(--gold); letter-spacing: 0.06em; }
.seg-cliente { font-size: 0.9rem; color: var(--text-lt); margin-top: 6px; }

/* TRACKER */
.tracker { margin-bottom: 32px; position: relative; }
.tracker-steps { display: flex; justify-content: space-between; position: relative; z-index: 2; margin-bottom: 10px; }
.step { display: flex; flex-direction: column; align-items: center; flex: 1; }
.step-dot {
  width: 18px; height: 18px; border-radius: 50%;
  border: 2px solid var(--charcoal); background: var(--carbon);
  transition: all 0.5s ease; margin-bottom: 6px;
  position: relative; z-index: 2;
}
.step.done .step-dot   { background: var(--gold); border-color: var(--gold); }
.step.active .step-dot { background: var(--red); border-color: var(--red); box-shadow: 0 0 0 4px rgba(192,57,43,0.25); animation: pulse-dot 1.4s ease-in-out infinite; }
.step-label { font-size: 0.65rem; color: var(--text-lt); text-align: center; letter-spacing: 0.04em; transition: color 0.4s; }
.step.done .step-label, .step.active .step-label { color: var(--cream); }

.tracker-bar {
  height: 3px; background: var(--charcoal); border-radius: 2px;
  margin: 0 9px; position: relative; margin-top: -22px; z-index: 1;
}
.tracker-progress {
  height: 100%; background: linear-gradient(90deg, var(--gold), var(--red));
  border-radius: 2px; width: 0%; transition: width 1s ease;
}

@keyframes pulse-dot {
  0%, 100% { box-shadow: 0 0 0 4px rgba(192,57,43,0.25); }
  50%       { box-shadow: 0 0 0 8px rgba(192,57,43,0.1); }
}

/* Estado actual */
.estado-actual {
  display: flex; align-items: center; gap: 16px;
  background: rgba(232,168,56,0.07); border: 1px solid rgba(232,168,56,0.2);
  border-radius: 8px; padding: 18px 20px; margin-bottom: 28px;
}
.estado-icon { font-size: 2rem; flex-shrink: 0; }
.estado-label { font-size: 1rem; font-weight: 600; color: var(--white); margin-bottom: 4px; }
.estado-tiempo { font-size: 0.8rem; color: var(--text-lt); }

/* Items */
.seg-items { border-top: 1px solid var(--charcoal); padding-top: 20px; margin-bottom: 12px; }
.seg-item { display: flex; justify-content: space-between; font-size: 0.85rem; padding: 7px 0; color: var(--cream); border-bottom: 1px solid rgba(61,61,61,0.5); }
.seg-item-precio { color: var(--gold); }
.seg-total { display: flex; justify-content: space-between; font-family: var(--ff-display); font-size: 1.05rem; font-weight: 700; color: var(--white); padding: 14px 0; margin-bottom: 24px; }
.seg-total span:last-child { color: var(--gold); }

.btn-volver {
  display: block; text-align: center;
  border: 1px solid var(--charcoal); border-radius: var(--r);
  padding: 11px; font-size: 0.875rem; color: var(--text-lt);
  transition: all var(--transition);
}
.btn-volver:hover { border-color: var(--gold); color: var(--gold); }

@media (max-width: 500px) {
  .seguimiento-card { padding: 28px 18px; }
  .step-label { font-size: 0.55rem; }
}

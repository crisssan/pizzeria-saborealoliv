from flask import Flask, render_template, request, jsonify, session, redirect
import sqlite3, os, time, random, string, json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from zoneinfo import ZoneInfo
TZ_CHILE = ZoneInfo("America/Santiago")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "saboresaloliv2025")

DB = os.path.join(os.path.dirname(__file__), "pedidos.db")

# ── CONFIGURACION ──────────────────────────────────────────────────────────────
GMAIL_USER     = os.environ.get("GMAIL_USER", "")
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD", "")
ADMIN_EMAIL    = "info.saboresitalianos@gmail.com"
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "saboresaloliv123")

NOMBRE_LOCAL   = "Sabores al Oliv"
DIRECCION      = "Roque Esteban Scarpa 2125, Colina"
TELEFONO       = "+56 9 3962 9467"
TIEMPO_ENTREGA = 20

MENU = [
    {"id": 1, "nombre": "Margarita",  "descripcion": "Salsa de tomate artesanal, mozzarella fior di latte, albahaca fresca y aceite de oliva extra virgen", "precio": 6000, "categoria": "clasica",  "emoji": "🍅", "img": "margarita.jpg"},
    {"id": 2, "nombre": "Pepperoni",  "descripcion": "Salsa de tomate, mozzarella, pepperoni italiano en rodajas generosas y oregano fresco",               "precio": 7000, "categoria": "clasica",  "emoji": "🍕", "img": "peperoni.jpg"},
    {"id": 3, "nombre": "Tocino",     "descripcion": "Base de crema, mozzarella, tocino crocante ahumado, cebolla caramelizada y ciboulette",               "precio": 7000, "categoria": "especial", "emoji": "🥓", "img": "tocino.jpg"},
    {"id": 4, "nombre": "Napolitana", "descripcion": "Salsa de tomate, mozzarella, tomates cherry frescos, anchoas, aceitunas negras y oregano",            "precio": 7000, "categoria": "especial", "emoji": "🫒", "img": "napo.jpg"},
]

ESTADOS = ["recibido", "preparando", "en_horno", "en_camino", "entregado"]
ESTADO_LABEL = {
    "recibido":   "Pedido recibido",
    "preparando": "Preparando tu pizza",
    "en_horno":   "En el horno",
    "en_camino":  "En camino",
    "entregado":  "Entregado",
}
ESTADO_EMOJI = {
    "recibido": "📋", "preparando": "👨‍🍳", "en_horno": "🔥", "en_camino": "🛵", "entregado": "🍕"
}
# Minutos reales para cada estado (total ~20 min)
ESTADO_MINUTOS = {"recibido": 0, "preparando": 2, "en_horno": 8, "en_camino": 15, "entregado": 20}

# ── HORARIO ────────────────────────────────────────────────────────────────────
def esta_abierto():
    if os.environ.get("FORZAR_ABIERTO","").lower() == "true":
        return True
    ahora = datetime.now(TZ_CHILE)
    # 3=Jueves, 4=Viernes, 5=Sabado
    if ahora.weekday() not in [3, 4, 5]:
        return False
    hora = ahora.hour + ahora.minute / 60
    return 18 <= hora < 23

def proximo_horario():
    dias = {3: "Jueves", 4: "Viernes", 5: "Sabado"}
    ahora = datetime.now(TZ_CHILE)
    for i in range(1, 8):
        dia = (ahora.weekday() + i) % 7
        if dia in dias:
            return f"{dias[dia]} desde las 18:00"
    return "Jueves desde las 18:00"

# ── BASE DE DATOS ──────────────────────────────────────────────────────────────
def get_db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = get_db()
    con.executescript("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo      TEXT    NOT NULL UNIQUE,
            nombre      TEXT    NOT NULL,
            telefono    TEXT,
            direccion   TEXT    NOT NULL,
            items_json  TEXT    NOT NULL,
            total       INTEGER NOT NULL,
            estado      TEXT    NOT NULL DEFAULT 'recibido',
            pago_estado TEXT    NOT NULL DEFAULT 'pendiente',
            pago_token  TEXT,
            created_at  REAL    NOT NULL
        );
    """)
    con.commit(); con.close()

init_db()

def codigo_pedido():
    return "OL-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

def fmt_pesos(n):
    return "$" + f"{int(n):,}".replace(",", ".")

# ── EMAIL ──────────────────────────────────────────────────────────────────────
def enviar_email(asunto, cuerpo_html, destinatario=None):
    if not GMAIL_USER or not GMAIL_PASSWORD:
        print("Email no configurado. Asunto:", asunto)
        return
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = asunto
        msg["From"]    = GMAIL_USER
        msg["To"]      = destinatario or ADMIN_EMAIL
        msg.attach(MIMEText(cuerpo_html, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as srv:
            srv.login(GMAIL_USER, GMAIL_PASSWORD)
            srv.send_message(msg)
    except Exception as e:
        print("Error email:", e)

def email_nuevo_pedido(pedido, items):
    lineas = "".join([f"<tr><td style='padding:8px 12px;border-bottom:1px solid #eee'>{i['nombre']}</td><td style='padding:8px 12px;border-bottom:1px solid #eee;text-align:right'>{fmt_pesos(i['precio'])}</td></tr>" for i in items])
    html = f"""
    <div style="font-family:sans-serif;max-width:500px;margin:0 auto">
      <div style="background:#1A1A1A;padding:24px;text-align:center">
        <h1 style="color:#E8A838;margin:0;font-size:1.4rem">Sabores al Oliv</h1>
        <p style="color:#aaa;margin:6px 0 0;font-size:0.85rem">Nuevo pedido pagado</p>
      </div>
      <div style="background:#fff;padding:24px">
        <p style="background:#e8f5e9;border-left:4px solid #4CAF50;padding:12px;border-radius:4px;font-weight:600">
          Codigo: {pedido['codigo']}
        </p>
        <p><strong>Cliente:</strong> {pedido['nombre']}</p>
        <p><strong>Telefono:</strong> {pedido.get('telefono','no indicado')}</p>
        <p><strong>Direccion:</strong> {pedido['direccion']}</p>
        <table style="width:100%;border-collapse:collapse;margin:16px 0">{lineas}</table>
        <p style="font-size:1.1rem;font-weight:700;text-align:right">
          Total: {fmt_pesos(pedido['total'])}
        </p>
        <hr style="border:none;border-top:1px solid #eee;margin:16px 0">
        <p style="color:#666;font-size:0.85rem">Cambia el estado del pedido en tu panel de admin.</p>
      </div>
    </div>"""
    enviar_email(f"Nuevo pedido {pedido['codigo']} — {fmt_pesos(pedido['total'])}", html)

def email_estado_cliente(pedido, nuevo_estado):
    label = ESTADO_LABEL.get(nuevo_estado, nuevo_estado)
    emoji = ESTADO_EMOJI.get(nuevo_estado, "")
    color = {"recibido":"#2196F3","preparando":"#FF9800","en_horno":"#f44336","en_camino":"#9C27B0","entregado":"#4CAF50"}.get(nuevo_estado,"#333")
    html = f"""
    <div style="font-family:sans-serif;max-width:500px;margin:0 auto">
      <div style="background:#1A1A1A;padding:24px;text-align:center">
        <h1 style="color:#E8A838;margin:0;font-size:1.4rem">Sabores al Oliv</h1>
      </div>
      <div style="background:#fff;padding:24px;text-align:center">
        <div style="font-size:3rem;margin-bottom:12px">{emoji}</div>
        <h2 style="color:{color};margin:0 0 8px">{label}</h2>
        <p style="color:#666">Hola <strong>{pedido['nombre']}</strong>, tu pedido <strong>{pedido['codigo']}</strong> esta en camino.</p>
        {'<p style="color:#666">Tu pizza llegara en aproximadamente <strong>' + str(TIEMPO_ENTREGA) + ' minutos</strong>.</p>' if nuevo_estado == 'en_camino' else ''}
        {'<p style="color:#4CAF50;font-weight:700">Gracias por elegirnos. Buen provecho!</p>' if nuevo_estado == 'entregado' else ''}
        <hr style="border:none;border-top:1px solid #eee;margin:16px 0">
        <p style="color:#999;font-size:0.78rem">{NOMBRE_LOCAL} — {DIRECCION} — {TELEFONO}</p>
      </div>
    </div>"""
    enviar_email(f"{emoji} Tu pedido {pedido['codigo']} — {label}", html, pedido.get("email",""))

# ── RUTAS PUBLICAS ─────────────────────────────────────────────────────────────
@app.route("/")
def index():
    abierto = esta_abierto()
    proximo = proximo_horario() if not abierto else None
    return render_template("index.html", menu=MENU, abierto=abierto, proximo=proximo,
                           nombre_local=NOMBRE_LOCAL, direccion=DIRECCION,
                           telefono=TELEFONO, tiempo_entrega=TIEMPO_ENTREGA)

@app.route("/seguimiento/<codigo>")
def seguimiento(codigo):
    return render_template("seguimiento.html", codigo=codigo, nombre_local=NOMBRE_LOCAL)

@app.route("/api/horario")
def api_horario():
    return jsonify({"abierto": esta_abierto(), "proximo": proximo_horario()})

@app.route("/api/pedido", methods=["POST"])
def crear_pedido():
    if not esta_abierto():
        return jsonify({"ok": False, "error": "Lo sentimos, estamos cerrados ahora."}), 400
    data      = request.json
    nombre    = data.get("nombre", "").strip()
    items     = data.get("items", [])
    total     = data.get("total", 0)
    direccion = "Retiro en local: Roque Esteban Scarpa 2125, Colina"
    email     = data.get("email", "").strip()
    if not nombre or not items:
        return jsonify({"ok": False, "error": "Datos incompletos"}), 400
    codigo = codigo_pedido()
    token  = "tok_" + "".join(random.choices(string.hexdigits[:16], k=16))
    con = get_db()
    items_con_email = items
    con.execute(
        "INSERT INTO pedidos (codigo,nombre,telefono,direccion,items_json,total,estado,pago_estado,pago_token,created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (codigo, nombre, data.get("telefono","") + "|" + email, direccion, json.dumps(items_con_email), total, "recibido", "pendiente", token, time.time())
    )
    con.commit(); con.close()
    return jsonify({"ok": True, "codigo": codigo, "pago_url": f"/pago/checkout?token={token}&codigo={codigo}"})

@app.route("/pago/checkout")
def pago_checkout():
    token  = request.args.get("token", "")
    codigo = request.args.get("codigo", "")
    con = get_db()
    row = con.execute("SELECT * FROM pedidos WHERE codigo=? AND pago_token=?", (codigo, token)).fetchone()
    con.close()
    if not row:
        return "Sesion de pago invalida", 404
    return render_template("checkout.html", pedido=dict(row), nombre_local=NOMBRE_LOCAL)

@app.route("/api/pago/confirmar", methods=["POST"])
def confirmar_pago():
    data  = request.json
    token = data.get("token", "")
    con = get_db()
    row = con.execute("SELECT * FROM pedidos WHERE pago_token=?", (token,)).fetchone()
    if not row:
        con.close()
        return jsonify({"ok": False, "error": "Token invalido"}), 404
    con.execute("UPDATE pedidos SET pago_estado='pagado', estado='recibido' WHERE pago_token=?", (token,))
    con.commit(); con.close()
    pedido = dict(row)
    items  = json.loads(pedido["items_json"])
    email_nuevo_pedido(pedido, items)
    return jsonify({"ok": True, "codigo": pedido["codigo"], "redirect": f"/seguimiento/{pedido['codigo']}"})

@app.route("/api/pedido/<codigo>/estado")
def estado_pedido(codigo):
    con = get_db()
    row = con.execute("SELECT * FROM pedidos WHERE codigo=?", (codigo,)).fetchone()
    con.close()
    if not row:
        return jsonify({"ok": False, "error": "Pedido no encontrado"}), 404
    pedido = dict(row)
    idx = ESTADOS.index(pedido["estado"]) if pedido["estado"] in ESTADOS else 0
    return jsonify({
        "ok": True, "codigo": pedido["codigo"], "nombre": pedido["nombre"],
        "estado": pedido["estado"], "estado_label": ESTADO_LABEL.get(pedido["estado"], ""),
        "estado_idx": idx, "total_estados": len(ESTADOS),
        "pago_estado": pedido["pago_estado"],
        "items": json.loads(pedido["items_json"]),
        "total": pedido["total"], "created_at": pedido["created_at"],
        "tiempo_entrega": TIEMPO_ENTREGA,
    })

# ── ADMIN ──────────────────────────────────────────────────────────────────────
@app.route("/admin", methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("password","") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin/pedidos")
        return render_template("admin_login.html", error="Contrasena incorrecta", nombre_local=NOMBRE_LOCAL)
    if session.get("admin"):
        return redirect("/admin/pedidos")
    return render_template("admin_login.html", error=None, nombre_local=NOMBRE_LOCAL)

@app.route("/admin/salir")
def admin_salir():
    session.clear()
    return redirect("/admin")

@app.route("/admin/pedidos")
def admin_pedidos():
    if not session.get("admin"):
        return redirect("/admin")
    con = get_db()
    rows = con.execute("SELECT * FROM pedidos WHERE pago_estado='pagado' ORDER BY created_at DESC LIMIT 50").fetchall()
    con.close()
    pedidos = []
    for r in rows:
        p = dict(r)
        p["items"] = json.loads(p["items_json"])
        tel_email = p["telefono"].split("|") if "|" in p["telefono"] else [p["telefono"], ""]
        p["telefono"] = tel_email[0]
        p["email"]    = tel_email[1] if len(tel_email) > 1 else ""
        pedidos.append(p)
    return render_template("admin_pedidos.html", pedidos=pedidos, estados=ESTADOS,
                           estado_label=ESTADO_LABEL, estado_emoji=ESTADO_EMOJI,
                           nombre_local=NOMBRE_LOCAL, abierto=esta_abierto())

@app.route("/admin/pedido/<codigo>/estado", methods=["POST"])
def admin_cambiar_estado(codigo):
    if not session.get("admin"):
        return jsonify({"ok": False}), 401
    nuevo_estado = request.json.get("estado","")
    if nuevo_estado not in ESTADOS:
        return jsonify({"ok": False, "error": "Estado invalido"}), 400
    con = get_db()
    row = con.execute("SELECT * FROM pedidos WHERE codigo=?", (codigo,)).fetchone()
    if not row:
        con.close()
        return jsonify({"ok": False}), 404
    con.execute("UPDATE pedidos SET estado=? WHERE codigo=?", (nuevo_estado, codigo))
    con.commit(); con.close()
    pedido = dict(row)
    tel_email = pedido["telefono"].split("|") if "|" in pedido["telefono"] else [pedido["telefono"], ""]
    pedido["email"] = tel_email[1] if len(tel_email) > 1 else ""
    if pedido["email"]:
        email_estado_cliente(pedido, nuevo_estado)
    return jsonify({"ok": True, "estado": nuevo_estado, "label": ESTADO_LABEL.get(nuevo_estado,"")})

if __name__ == "__main__":
    app.run(debug=True)

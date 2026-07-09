from flask import Flask, render_template, request, jsonify, session, redirect
import sqlite3, os, time, random, string, json
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "saboresaloliv2025")

DB = os.path.join(os.path.dirname(__file__), "pedidos.db")
TZ_CHILE = ZoneInfo("America/Santiago")

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "saboresaloliv123")

NOMBRE_LOCAL   = "Sabores al Oliv"
DIRECCION      = "Roque Esteban Scarpa 2125, Colina"
TELEFONO       = "+56 9 3962 9467"
TIEMPO_ENTREGA = 20

MENU = [
    {"id": 1, "nombre": "Margarita",  "descripcion": "Salsa de tomate artesanal, mozzarella, albahaca fresca y aceite de oliva extra virgen",               "precio": 6000, "categoria": "clasica",  "emoji": "🍅", "img": "margarita.jpg"},
    {"id": 2, "nombre": "Pepperoni",  "descripcion": "Salsa de tomate, mozzarella, pepperoni italiano en rodajas generosas",                                "precio": 7000, "categoria": "clasica",  "emoji": "🍕", "img": "peperoni.jpg"},
    {"id": 3, "nombre": "Tocino",     "descripcion": "Base de crema, mozzarella, tocino crocante ahumado, cebolla caramelizada y ciboulette",               "precio": 7000, "categoria": "especial", "emoji": "🥓", "img": "tocino.jpg"},
    {"id": 4, "nombre": "Napo", "descripcion": "Salsa de tomate, mozzarella, jamon praga y aceitunas negras",                                               "precio": 7000, "categoria": "especial", "emoji": "🫒", "img": "napo.jpg"},
]

ESTADOS = ["recibido", "preparando", "en_horno", "listo", "entregado"]
ESTADO_LABEL = {
    "recibido":   "Pedido recibido",
    "preparando": "Preparando tu pizza",
    "en_horno":   "En el horno",
    "listo":      "Lista para retirar",
    "entregado":  "Entregada, buen provecho!",
}
ESTADO_EMOJI = {
    "recibido": "📋", "preparando": "👨‍🍳", "en_horno": "🔥", "listo": "✅", "entregado": "🍕"
}

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
            items_json  TEXT    NOT NULL,
            total       INTEGER NOT NULL,
            estado      TEXT    NOT NULL DEFAULT 'recibido',
            created_at  REAL    NOT NULL
        );
        CREATE TABLE IF NOT EXISTS config (
            clave TEXT PRIMARY KEY,
            valor TEXT NOT NULL
        );
        INSERT OR IGNORE INTO config (clave, valor) VALUES ('tienda_abierta', '1');
    """)
    con.commit(); con.close()

init_db()

def tienda_manual_abierta():
    con = get_db()
    row = con.execute("SELECT valor FROM config WHERE clave='tienda_abierta'").fetchone()
    con.close()
    return row and row["valor"] == "1"

def esta_abierto():
    if os.environ.get("FORZAR_ABIERTO","").lower() == "true":
        return True
    if not tienda_manual_abierta():
        return False
    ahora = datetime.now(TZ_CHILE)
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

def fmt_pesos(n):
    return "$" + f"{int(n):,}".replace(",", ".")

# ── RUTAS PUBLICAS ─────────────────────────────────────────────────────────────
@app.route("/")
def index():
    abierto = esta_abierto()
    manual  = tienda_manual_abierta()
    # Agotado = horario correcto pero cerrado manualmente
    ahora   = datetime.now(TZ_CHILE)
    en_horario = ahora.weekday() in [3,4,5] and 18 <= (ahora.hour + ahora.minute/60) < 23
    agotado = en_horario and not manual
    proximo = proximo_horario() if not abierto else None
    return render_template("index.html", menu=MENU, abierto=abierto, proximo=proximo,
                           agotado=agotado,
                           nombre_local=NOMBRE_LOCAL, direccion=DIRECCION,
                           telefono=TELEFONO, tiempo_entrega=TIEMPO_ENTREGA)

# Guardar pedido (llamado desde JS despues de redirigir a WhatsApp)
@app.route("/api/pedido", methods=["POST"])
def crear_pedido():
    data    = request.json
    nombre  = data.get("nombre", "").strip()
    items   = data.get("items", [])
    total   = data.get("total", 0)
    codigo  = data.get("codigo", "")
    if not nombre or not items or not codigo:
        return jsonify({"ok": False}), 400
    con = get_db()
    try:
        con.execute(
            "INSERT INTO pedidos (codigo,nombre,telefono,items_json,total,estado,created_at) VALUES (?,?,?,?,?,?,?)",
            (codigo, nombre, data.get("telefono",""), json.dumps(items), total, "recibido", time.time())
        )
        con.commit()
    except Exception as e:
        print("Error guardando pedido:", e)
    finally:
        con.close()
    return jsonify({"ok": True})

@app.route("/seguimiento/<codigo>")
def seguimiento(codigo):
    return render_template("seguimiento.html", codigo=codigo, nombre_local=NOMBRE_LOCAL)

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
        "items": json.loads(pedido["items_json"]),
        "total": pedido["total"], "tiempo_entrega": TIEMPO_ENTREGA,
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
    rows = con.execute("SELECT * FROM pedidos ORDER BY created_at DESC LIMIT 50").fetchall()
    con.close()
    pedidos = []
    for r in rows:
        p = dict(r)
        p["items"] = json.loads(p["items_json"])
        pedidos.append(p)
    return render_template("admin_pedidos.html", pedidos=pedidos, estados=ESTADOS,
                           estado_label=ESTADO_LABEL, estado_emoji=ESTADO_EMOJI,
                           nombre_local=NOMBRE_LOCAL, abierto=esta_abierto(),
                           fmt_pesos=fmt_pesos)

@app.route("/admin/pedido/<codigo>/estado", methods=["POST"])
def admin_cambiar_estado(codigo):
    if not session.get("admin"):
        return jsonify({"ok": False}), 401
    nuevo_estado = request.json.get("estado","")
    if nuevo_estado not in ESTADOS:
        return jsonify({"ok": False, "error": "Estado invalido"}), 400
    con = get_db()
    con.execute("UPDATE pedidos SET estado=? WHERE codigo=?", (nuevo_estado, codigo))
    con.commit(); con.close()
    return jsonify({"ok": True, "estado": nuevo_estado, "label": ESTADO_LABEL.get(nuevo_estado,"")})

@app.route("/admin/tienda", methods=["POST"])
def admin_tienda():
    if not session.get("admin"):
        return jsonify({"ok": False}), 401
    accion = request.json.get("accion","")
    valor  = "1" if accion == "abrir" else "0"
    con = get_db()
    con.execute("UPDATE config SET valor=? WHERE clave='tienda_abierta'", (valor,))
    con.commit(); con.close()
    return jsonify({"ok": True, "abierta": valor == "1"})

@app.route("/api/estado-tienda")
def api_estado_tienda():
    return jsonify({"abierta": esta_abierto(), "manual": tienda_manual_abierta()})

if __name__ == "__main__":
    app.run(debug=True)

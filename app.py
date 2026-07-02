from flask import Flask, render_template, request, jsonify
import sqlite3, os, time, random, string

app = Flask(__name__)
DB  = os.path.join(os.path.dirname(__file__), "pedidos.db")

MENU = [
    {"id": 1, "nombre": "Margherita al Forno",   "descripcion": "Tomate San Marzano, mozzarella fior di latte, albahaca fresca, aceite de oliva virgen",             "precio": 12900, "categoria": "clasica",  "emoji": "🍅"},
    {"id": 2, "nombre": "Funghi Selvaggi",        "descripcion": "Crema de hongos, mezcla de hongos silvestres salteados, tomillo fresco, parmesano",                 "precio": 14900, "categoria": "especial", "emoji": "🍄"},
    {"id": 3, "nombre": "Diavola",                "descripcion": "Tomate artesanal, salame picante, mozzarella, aceitunas negras, aji merken",                        "precio": 13900, "categoria": "clasica",  "emoji": "🌶️"},
    {"id": 4, "nombre": "Trufa Negra",            "descripcion": "Base de crema, mozzarella, prosciutto di Parma, rucula, aceite de trufa negra",                     "precio": 17900, "categoria": "gourmet",  "emoji": "✨"},
    {"id": 5, "nombre": "Quattro Stagioni",       "descripcion": "Tomate, jamon, alcachofa, champinones, aceitunas, cuatro quesos artesanales",                       "precio": 15900, "categoria": "especial", "emoji": "🫒"},
    {"id": 6, "nombre": "Burrata & Prosciutto",   "descripcion": "Salsa de tomates cherry, burrata fresca, jamon crudo, rucula, reduccion de balsamico",             "precio": 18900, "categoria": "gourmet",  "emoji": "🧀"},
]

ESTADOS = ["recibido", "preparando", "en_horno", "en_camino", "entregado"]
ESTADO_LABEL = {
    "recibido":   "Pedido recibido",
    "preparando": "Preparando ingredientes",
    "en_horno":   "En el horno 🔥",
    "en_camino":  "En camino 🛵",
    "entregado":  "Entregado! 🍕",
}
ESTADO_MINUTOS = {"recibido": 0, "preparando": 3, "en_horno": 10, "en_camino": 18, "entregado": 30}

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
    return "FN-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route("/")
def index():
    return render_template("index.html", menu=MENU)

@app.route("/seguimiento/<codigo>")
def seguimiento(codigo):
    return render_template("seguimiento.html", codigo=codigo)

@app.route("/api/pedido", methods=["POST"])
def crear_pedido():
    import json
    data      = request.json
    nombre    = data.get("nombre", "").strip()
    items     = data.get("items", [])
    total     = data.get("total", 0)
    direccion = data.get("direccion", "").strip()

    if not nombre or not items or not direccion:
        return jsonify({"ok": False, "error": "Datos incompletos"}), 400

    codigo = codigo_pedido()
    token  = "tok_" + "".join(random.choices(string.hexdigits[:16], k=16))

    con = get_db()
    con.execute(
        "INSERT INTO pedidos (codigo,nombre,telefono,direccion,items_json,total,estado,pago_estado,pago_token,created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (codigo, nombre, data.get("telefono",""), direccion, json.dumps(items), total, "recibido", "pendiente", token, time.time())
    )
    con.commit(); con.close()

    pago_url = f"/pago/checkout?token={token}&codigo={codigo}"
    return jsonify({"ok": True, "codigo": codigo, "pago_url": pago_url})

@app.route("/pago/checkout")
def pago_checkout():
    token  = request.args.get("token", "")
    codigo = request.args.get("codigo", "")
    con = get_db()
    row = con.execute("SELECT * FROM pedidos WHERE codigo=? AND pago_token=?", (codigo, token)).fetchone()
    con.close()
    if not row:
        return "Sesion de pago invalida", 404
    return render_template("checkout.html", pedido=dict(row))

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

    return jsonify({"ok": True, "codigo": row["codigo"], "redirect": f"/seguimiento/{row['codigo']}"})

@app.route("/api/pedido/<codigo>/estado")
def estado_pedido(codigo):
    import json
    con = get_db()
    row = con.execute("SELECT * FROM pedidos WHERE codigo=?", (codigo,)).fetchone()
    con.close()
    if not row:
        return jsonify({"ok": False, "error": "Pedido no encontrado"}), 404

    pedido = dict(row)

    if pedido["pago_estado"] == "pagado":
        elapsed = (time.time() - pedido["created_at"]) / 60
        estado_actual = "recibido"
        for e in ESTADOS:
            if elapsed >= ESTADO_MINUTOS[e]:
                estado_actual = e
        if estado_actual != pedido["estado"]:
            con2 = get_db()
            con2.execute("UPDATE pedidos SET estado=? WHERE codigo=?", (estado_actual, codigo))
            con2.commit(); con2.close()
            pedido["estado"] = estado_actual

    idx = ESTADOS.index(pedido["estado"]) if pedido["estado"] in ESTADOS else 0
    return jsonify({
        "ok":           True,
        "codigo":       pedido["codigo"],
        "nombre":       pedido["nombre"],
        "estado":       pedido["estado"],
        "estado_label": ESTADO_LABEL.get(pedido["estado"], pedido["estado"]),
        "estado_idx":   idx,
        "total_estados": len(ESTADOS),
        "pago_estado":  pedido["pago_estado"],
        "items":        json.loads(pedido["items_json"]),
        "total":        pedido["total"],
        "created_at":   pedido["created_at"],
    })

if __name__ == "__main__":
    app.run(debug=True)

import re
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from app import db
from models.reserva import Reserva
from models.configuracion import Configuracion
from routes.email_service import enviar_confirmacion, enviar_notificacion_admin

reservas_bp = Blueprint("reservas", __name__)

TELEFONO_ES = re.compile(r'^(\+34|0034)?[6789]\d{8}$')


def get_config():
    cfg = Configuracion.query.first()
    if not cfg:
        cfg = Configuracion()
        db.session.add(cfg)
        db.session.commit()
    return cfg


def generar_slots(fecha_str, cfg):
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return []

    dias_permitidos = [int(d) for d in cfg.dias_trabajo.split(",") if d]
    dia_semana = fecha.weekday() + 1
    if dia_semana not in dias_permitidos:
        return []

    apertura  = datetime.strptime(f"{fecha_str} {cfg.hora_apertura}", "%Y-%m-%d %H:%M")
    cierre    = datetime.strptime(f"{fecha_str} {cfg.hora_cierre}",   "%Y-%m-%d %H:%M")
    duracion  = timedelta(minutes=cfg.duracion_cita)

    pausa_ini = pausa_fin = None
    if cfg.pausa_inicio and cfg.pausa_fin:
        pausa_ini = datetime.strptime(f"{fecha_str} {cfg.pausa_inicio}", "%Y-%m-%d %H:%M")
        pausa_fin = datetime.strptime(f"{fecha_str} {cfg.pausa_fin}",   "%Y-%m-%d %H:%M")

    inicio_dia = datetime.strptime(f"{fecha_str} 00:00", "%Y-%m-%d %H:%M")
    fin_dia    = datetime.strptime(f"{fecha_str} 23:59", "%Y-%m-%d %H:%M")
    ocupadas   = {
        r.fecha_hora.strftime("%H:%M")
        for r in Reserva.query.filter(
            Reserva.fecha_hora >= inicio_dia,
            Reserva.fecha_hora <= fin_dia,
            Reserva.estado != "cancelada"
        ).all()
    }

    slots = []
    actual = apertura
    ahora  = datetime.now()

    while actual + duracion <= cierre:
        if pausa_ini and pausa_ini <= actual < pausa_fin:
            actual = pausa_fin
            continue
        hora_str = actual.strftime("%H:%M")
        if hora_str not in ocupadas and actual > ahora:
            slots.append(hora_str)
        actual += duracion

    return slots


@reservas_bp.route("/slots", methods=["GET"])
def get_slots():
    fecha = request.args.get("fecha")
    if not fecha:
        return jsonify({"error": "Falta el parámetro fecha"}), 400
    cfg   = get_config()
    slots = generar_slots(fecha, cfg)
    return jsonify({"slots": slots, "duracion": cfg.duracion_cita})


@reservas_bp.route("/config", methods=["GET"])
def get_config_publica():
    cfg = get_config()
    return jsonify({
        "nombre_negocio": cfg.nombre_negocio,
        "hora_apertura":  cfg.hora_apertura,
        "hora_cierre":    cfg.hora_cierre,
        "dias_trabajo":   cfg.dias_trabajo,
        "duracion_cita":  cfg.duracion_cita,
    })


@reservas_bp.route("/reservas", methods=["POST"])
def crear_reserva():
    data = request.get_json()

    errores = {}
    nombre   = (data.get("nombre") or "").strip()
    email    = (data.get("email")  or "").strip()
    telefono = (data.get("telefono") or "").strip().replace(" ", "")
    servicio = (data.get("servicio") or "")
    fecha_hora_str = (data.get("fecha_hora") or "")

    if not nombre:
        errores["nombre"] = "El nombre es obligatorio."
    if not email:
        errores["email"] = "El email es obligatorio."
    if not servicio:
        errores["servicio"] = "Selecciona un servicio."
    if not fecha_hora_str:
        errores["fecha_hora"] = "La fecha y hora son obligatorias."

    if telefono and not TELEFONO_ES.match(telefono):
        errores["telefono"] = "Teléfono inválido. Ej: 612345678 o +34612345678"

    if errores:
        return jsonify({"ok": False, "errores": errores}), 422

    try:
        fecha = datetime.fromisoformat(fecha_hora_str)
    except ValueError:
        return jsonify({"ok": False, "errores": {"fecha_hora": "Formato inválido."}}), 422

    cfg      = get_config()
    fecha_str = fecha.strftime("%Y-%m-%d")
    hora_str  = fecha.strftime("%H:%M")
    slots     = generar_slots(fecha_str, cfg)

    if hora_str not in slots:
        return jsonify({"ok": False, "errores": {
            "fecha_hora": "Ese horario ya no está disponible. Elige otro."
        }}), 409

    reserva = Reserva(
        nombre     = nombre,
        email      = email.lower(),
        telefono   = telefono or None,
        servicio   = servicio,
        fecha_hora = fecha,
    )
    db.session.add(reserva)
    db.session.commit()

    enviar_confirmacion(reserva)
    enviar_notificacion_admin(reserva)

    return jsonify({"ok": True, "reserva": reserva.to_dict()}), 201


@reservas_bp.route("/reservas", methods=["GET"])
def listar_reservas():
    estado = request.args.get("estado")
    query  = Reserva.query.order_by(Reserva.fecha_hora.asc())
    if estado:
        query = query.filter_by(estado=estado)
    return jsonify([r.to_dict() for r in query.all()])


@reservas_bp.route("/reservas/<int:id>/estado", methods=["PATCH"])
def cambiar_estado(id):
    reserva = Reserva.query.get_or_404(id)
    nuevo   = request.get_json().get("estado")
    if nuevo not in ("pendiente", "confirmada", "cancelada"):
        return jsonify({"ok": False, "error": "Estado inválido."}), 400
    reserva.estado = nuevo
    db.session.commit()
    return jsonify({"ok": True, "reserva": reserva.to_dict()})


@reservas_bp.route("/reservas/<int:id>", methods=["DELETE"])
def eliminar_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    db.session.delete(reserva)
    db.session.commit()
    return jsonify({"ok": True})
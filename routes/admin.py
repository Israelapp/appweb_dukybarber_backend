import os
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.reserva import Reserva
from models.configuracion import Configuracion
from app import db
from routes.email_service import enviar_cambio_estado

admin_bp = Blueprint("admin", __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated


def get_config():
    cfg = Configuracion.query.first()
    if not cfg:
        cfg = Configuracion()
        db.session.add(cfg)
        db.session.commit()
    return cfg


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        clave   = request.form.get("clave", "")
        if (usuario == os.getenv("ADMIN_USERNAME", "admin") and
                clave == os.getenv("ADMIN_PASSWORD", "admin123")):
            session["admin_logged_in"] = True
            return redirect(url_for("admin.panel"))
        error = "Credenciales incorrectas."
    return render_template("admin/login.html", error=error)


@admin_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@login_required
def panel():
    estado   = request.args.get("estado", "todas")
    query    = Reserva.query.order_by(Reserva.fecha_hora.asc())
    if estado != "todas":
        query = query.filter_by(estado=estado)

    reservas    = query.all()
    totales     = Reserva.query.count()
    pendientes  = Reserva.query.filter_by(estado="pendiente").count()
    confirmadas = Reserva.query.filter_by(estado="confirmada").count()
    canceladas  = Reserva.query.filter_by(estado="cancelada").count()
    cfg         = get_config()

    return render_template("admin/panel.html",
        reservas=reservas, estado_filtro=estado,
        totales=totales, pendientes=pendientes,
        confirmadas=confirmadas, canceladas=canceladas,
        cfg=cfg,
    )


@admin_bp.route("/reservas/<int:id>/estado", methods=["POST"])
@login_required
def cambiar_estado(id):
    reserva = Reserva.query.get_or_404(id)
    nuevo   = request.form.get("estado")
    mensaje = request.form.get("mensaje", "").strip()

    if nuevo in ("pendiente", "confirmada", "cancelada"):
        reserva.estado = nuevo
        db.session.commit()

        # Enviar email al cliente si se confirma o cancela
        if nuevo in ("confirmada", "cancelada"):
            enviar_cambio_estado(reserva, mensaje_personalizado=mensaje)

        flash(f"Reserva de {reserva.nombre} actualizada a '{nuevo}'. Email enviado.", "success")
    return redirect(url_for("admin.panel", estado=request.form.get("filtro_actual", "todas")))


@admin_bp.route("/reservas/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar(id):
    reserva = Reserva.query.get_or_404(id)
    nombre  = reserva.nombre
    db.session.delete(reserva)
    db.session.commit()
    flash(f"Reserva de {nombre} eliminada.", "info")
    return redirect(url_for("admin.panel"))


@admin_bp.route("/configuracion", methods=["GET", "POST"])
@login_required
def configuracion():
    cfg = get_config()
    if request.method == "POST":
        cfg.nombre_negocio   = request.form.get("nombre_negocio", "").strip()
        cfg.email_negocio    = request.form.get("email_negocio", "").strip()
        cfg.telefono_negocio = request.form.get("telefono_negocio", "").strip()
        cfg.direccion        = request.form.get("direccion", "").strip()
        cfg.hora_apertura    = request.form.get("hora_apertura", "09:00")
        cfg.hora_cierre      = request.form.get("hora_cierre", "20:00")
        cfg.duracion_cita    = int(request.form.get("duracion_cita", 30))
        cfg.pausa_inicio     = request.form.get("pausa_inicio", "").strip()
        cfg.pausa_fin        = request.form.get("pausa_fin", "").strip()

        dias = request.form.getlist("dias_trabajo")
        cfg.dias_trabajo = ",".join(dias)

        db.session.commit()
        flash("Configuración guardada correctamente.", "success")
        return redirect(url_for("admin.configuracion"))

    dias_activos = [int(d) for d in cfg.dias_trabajo.split(",") if d]
    return render_template("admin/configuracion.html", cfg=cfg, dias_activos=dias_activos)
from flask_mail import Message
from app import mail


def enviar_confirmacion(reserva):
    """Envía email de confirmación al cliente."""
    try:
        msg = Message(
            subject="✂️ Reserva confirmada — Duky Barber",
            recipients=[reserva.email],
        )
        msg.html = f"""
        <div style="font-family:sans-serif;max-width:500px;margin:auto;background:#181818;color:#F0EDE6;padding:32px;border-radius:8px;">
          <h1 style="font-size:2rem;color:#C9A84C;margin-bottom:4px;">Duky Barber</h1>
          <p style="color:#888880;margin-bottom:24px;">Barbería profesional · Desde 2018</p>

          <h2 style="font-size:1.1rem;margin-bottom:16px;">¡Hola, {reserva.nombre}!</h2>
          <p>Tu reserva ha sido recibida y está <strong style="color:#C9A84C;">pendiente de confirmación</strong>.</p>

          <div style="background:#222;border:1px solid rgba(201,168,76,0.3);border-radius:6px;padding:20px;margin:24px 0;">
            <p style="margin:6px 0;"><strong>Servicio:</strong> {reserva.servicio}</p>
            <p style="margin:6px 0;"><strong>Fecha y hora:</strong> {reserva.fecha_hora.strftime("%d/%m/%Y a las %H:%M")}</p>
            <p style="margin:6px 0;"><strong>Estado:</strong> Pendiente</p>
          </div>

          <p style="color:#888880;font-size:0.85rem;">
            Si necesitas cancelar o modificar tu cita, contáctanos por Instagram o Facebook.
          </p>
          <hr style="border-color:rgba(201,168,76,0.2);margin:24px 0;">
          <p style="color:#888880;font-size:0.78rem;text-align:center;">© 2026 Duky Barber · Todos los derechos reservados</p>
        </div>
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False


def enviar_notificacion_admin(reserva):
    """Avisa al barbero de una nueva reserva."""
    import os
    admin_email = os.getenv("MAIL_USERNAME")
    if not admin_email:
        return

    try:
        msg = Message(
            subject=f"🔔 Nueva reserva — {reserva.nombre}",
            recipients=[admin_email],
        )
        msg.html = f"""
        <div style="font-family:sans-serif;padding:24px;">
          <h2>Nueva reserva recibida</h2>
          <ul>
            <li><strong>Nombre:</strong> {reserva.nombre}</li>
            <li><strong>Email:</strong> {reserva.email}</li>
            <li><strong>Teléfono:</strong> {reserva.telefono or "—"}</li>
            <li><strong>Servicio:</strong> {reserva.servicio}</li>
            <li><strong>Fecha/Hora:</strong> {reserva.fecha_hora.strftime("%d/%m/%Y %H:%M")}</li>
          </ul>
        </div>
        """
        mail.send(msg)
    except Exception as e:
        print(f"[EMAIL ADMIN ERROR] {e}")

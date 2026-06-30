from flask_mail import Message
from app import mail


def enviar_confirmacion(reserva):
    """Email al crear la reserva (estado pendiente)."""
    try:
        msg = Message(
            subject="✂️ Reserva recibida — Duky Barber",
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
            Te avisaremos por email en cuanto confirmemos tu cita.
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


def enviar_cambio_estado(reserva, mensaje_personalizado=""):
    """Email al cliente cuando el barbero confirma o cancela la reserva."""
    try:
        if reserva.estado == "confirmada":
            asunto = "✅ Tu reserva fue confirmada — Duky Barber"
            titulo = "¡Tu cita está confirmada!"
            color  = "#5cb85c"
            cuerpo_estado = "Tu reserva ha sido <strong style='color:#5cb85c;'>confirmada</strong>. ¡Te esperamos!"
        elif reserva.estado == "cancelada":
            asunto = "❌ Tu reserva fue cancelada — Duky Barber"
            titulo = "Tu cita fue cancelada"
            color  = "#e05555"
            cuerpo_estado = "Lamentamos informarte que tu reserva ha sido <strong style='color:#e05555;'>cancelada</strong>."
        else:
            return False

        mensaje_extra = ""
        if mensaje_personalizado:
            mensaje_extra = f"""
            <div style="background:#222;border-left:3px solid {color};border-radius:4px;padding:16px 20px;margin:20px 0;">
              <p style="margin:0;color:#F0EDE6;font-size:0.92rem;"><strong>Mensaje del barbero:</strong></p>
              <p style="margin:8px 0 0;color:#ccc;font-size:0.9rem;">{mensaje_personalizado}</p>
            </div>
            """

        msg = Message(subject=asunto, recipients=[reserva.email])
        msg.html = f"""
        <div style="font-family:sans-serif;max-width:500px;margin:auto;background:#181818;color:#F0EDE6;padding:32px;border-radius:8px;">
          <h1 style="font-size:2rem;color:#C9A84C;margin-bottom:4px;">Duky Barber</h1>
          <p style="color:#888880;margin-bottom:24px;">Barbería profesional · Desde 2018</p>

          <h2 style="font-size:1.1rem;margin-bottom:16px;color:{color};">{titulo}</h2>
          <p>Hola {reserva.nombre}, {cuerpo_estado}</p>

          <div style="background:#222;border:1px solid rgba(201,168,76,0.3);border-radius:6px;padding:20px;margin:24px 0;">
            <p style="margin:6px 0;"><strong>Servicio:</strong> {reserva.servicio}</p>
            <p style="margin:6px 0;"><strong>Fecha y hora:</strong> {reserva.fecha_hora.strftime("%d/%m/%Y a las %H:%M")}</p>
          </div>

          {mensaje_extra}

          <p style="color:#888880;font-size:0.85rem;">
            Si tienes dudas, contáctanos por Instagram o Facebook.
          </p>
          <hr style="border-color:rgba(201,168,76,0.2);margin:24px 0;">
          <p style="color:#888880;font-size:0.78rem;text-align:center;">© 2026 Duky Barber · Todos los derechos reservados</p>
        </div>
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(f"[EMAIL CAMBIO ESTADO ERROR] {e}")
        return False
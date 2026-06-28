from app import db


class Configuracion(db.Model):
    """
    Configuración del negocio — una sola fila en la DB.
    El barbero la edita desde el panel admin.
    """
    __tablename__ = "configuracion"

    id                = db.Column(db.Integer, primary_key=True)

    # Datos del negocio
    nombre_negocio    = db.Column(db.String(120), default="Duky Barber")
    email_negocio     = db.Column(db.String(120), default="")
    telefono_negocio  = db.Column(db.String(30),  default="")
    direccion         = db.Column(db.String(200),  default="")

    # Horario de trabajo
    hora_apertura     = db.Column(db.String(5),  default="09:00")  # HH:MM
    hora_cierre       = db.Column(db.String(5),  default="20:00")  # HH:MM
    duracion_cita     = db.Column(db.Integer,    default=30)        # minutos
    dias_trabajo      = db.Column(db.String(50), default="1,2,3,4,5,6")  # 0=Dom..6=Sab

    # Pausa al mediodía (opcional)
    pausa_inicio      = db.Column(db.String(5),  default="")   # ej. "14:00"
    pausa_fin         = db.Column(db.String(5),  default="")   # ej. "16:00"

    def to_dict(self):
        return {
            "nombre_negocio":   self.nombre_negocio,
            "email_negocio":    self.email_negocio,
            "telefono_negocio": self.telefono_negocio,
            "direccion":        self.direccion,
            "hora_apertura":    self.hora_apertura,
            "hora_cierre":      self.hora_cierre,
            "duracion_cita":    self.duracion_cita,
            "dias_trabajo":     self.dias_trabajo,
            "pausa_inicio":     self.pausa_inicio,
            "pausa_fin":        self.pausa_fin,
        }

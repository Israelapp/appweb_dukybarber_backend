from app import db
from datetime import datetime


class Reserva(db.Model):
    __tablename__ = "reservas"

    id         = db.Column(db.Integer, primary_key=True)
    nombre     = db.Column(db.String(120), nullable=False)
    email      = db.Column(db.String(120), nullable=False)
    telefono   = db.Column(db.String(30),  nullable=True)
    servicio   = db.Column(db.String(100), nullable=False)
    fecha_hora = db.Column(db.DateTime,    nullable=False)
    estado     = db.Column(db.String(20),  default="pendiente")  # pendiente | confirmada | cancelada
    creada_en  = db.Column(db.DateTime,    default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":         self.id,
            "nombre":     self.nombre,
            "email":      self.email,
            "telefono":   self.telefono,
            "servicio":   self.servicio,
            "fecha_hora": self.fecha_hora.strftime("%d/%m/%Y %H:%M"),
            "estado":     self.estado,
            "creada_en":  self.creada_en.strftime("%d/%m/%Y %H:%M"),
        }

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import re
import json
import resend

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7,
)

class infoEmpresa(BaseModel):
    empresa: str
    rubro: str
    actividad: str
    necesidad: str

class solicitudPresupuesto(BaseModel):
    empresa: str
    rubro: str
    actividad: str
    necesidad: str
    preguntas: List[str]
    respuestas: List[str]

class solicitudContacto(BaseModel):
    nombre: str
    email: str
    telefono: str = ""
    mensaje: str = ""
    tipo: str
    empresa: str
    proyecto: str
    complejidad: str = ""
    tiempo_estimado: str = ""
    tecnologias: str = ""
    resumen: str = ""
    funcionalidades: str = ""
    beneficios: str = ""

@app.get("/")
def root():
    return {"status": "EstimAI backend corriendo"}

@app.post("/questions")
def generarPreguntas(info: infoEmpresa):
    system = "Eres un consultor experto en levantamiento de requerimientos para proyectos de software. Respondes únicamente con JSON válido, sin markdown ni backticks."
    prompt = f"""Con base en esta información de un cliente:
- Empresa: {info.empresa}
- Rubro = {info.rubro}
- Actividad principal = {info.actividad}
- Necesidad inicial = {info.necesidad}

Genera exactamente 6 preguntas específicas para profundizar el levantamiento de requerimientos. Deben ser progresivas, contextualizadas al rubro, y escritas en español profesional pero accesible.

Responde SOLO con este JSON:
{{"preguntas": ["pregunta1", "pregunta2", "pregunta3", "pregunta4", "pregunta5", "pregunta6"]}}"""
    
    response = llm.invoke([SystemMessage(content=system), HumanMessage(content=prompt)])
    text = response.content.strip()
    text = re.sub(r"```json|```", "", text).strip()
    data = json.loads(text)
    return data

@app.post("/estimate")
def generarEstimacion(req: solicitudPresupuesto):
    system = "Eres un consultor senior en desarrollo de software. Respondes únicamente con JSON válido, sin markdown ni backticks."
    dyn_context = "\n".join(
        [f"P: {q}\nR: {r}" for q, r in zip(req.preguntas, req.respuestas)]
    )
    prompt = f"""Analiza este levantamiento de requerimientos y genera una propuesta técnica:
    
EMPRESA: {req.empresa}
RUBRO: {req.rubro}
ACTIVIDAD: {req.actividad}
NECESIDAD: {req.necesidad}

PREGUNTAS Y RESPUESTAS:
{dyn_context}

Responde SOLO con este JSON:
{{
  "titulo_proyecto": "nombre descriptivo del sistema en máx 8 palabras",
  "resumen_ejecutivo": "2-3 oraciones claras para un cliente no técnico",
  "funcionalidades_clave": ["func1", "func2", "func3", "func4", "func5"],
  "tecnologias_sugeridas": ["tech1", "tech2", "tech3"],
  "complejidad": "Baja o Media o Alta",
  "tiempo_estimado": "rango de tiempo ej: 2-3 meses",
  "beneficios": "2 oraciones sobre el impacto en el negocio",
  "proximos_pasos": "qué debería pasar después de confirmar esta propuesta"
}}"""
    
    response = llm.invoke([SystemMessage(content=system), HumanMessage(content=prompt)])
    text = response.content.strip()
    text = re.sub(r"```json|```", "", text).strip()
    data = json.loads(text)
    return data

@app.post("/contact")
def enviarContacto(req: solicitudContacto):
    resend.api_key = os.getenv("RESEND_API_KEY")

    tipo_label = "Propuesta confirmada" if req.tipo == "confirma" else "Idea no resuelta"
    emoji = "✅" if req.tipo == "confirma" else "⚠️"

    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background:#2D2660; padding:24px; border-radius:8px 8px 0 0;">
            <h1 style="color:#F0EFF9; margin:0; font-size:20px;">EstimAI · Nuevo contacto</h1>
            <p style="color:#B8B0F0; margin:8px 0 0; font-size:14px;">{emoji} {tipo_label}</p>
        </div>

        <div style="background:#F5F4FC; padding:24px; border:1px solid #E0DCF5;">
            <h2 style="color:#2D2660; font-size:14px; text-transform:uppercase; letter-spacing:1px; margin:0 0 12px;">Datos del cliente</h2>
            <table style="width:100%; font-size:14px; color:#333;">
                <tr><td style="padding:4px 0; color:#7C6FCD; width:140px;"><strong>Nombre</strong></td><td>{req.nombre}</td></tr>
                <tr><td style="padding:4px 0; color:#7C6FCD;"><strong>Email</strong></td><td>{req.email}</td></tr>
                <tr><td style="padding:4px 0; color:#7C6FCD;"><strong>Teléfono</strong></td><td>{req.telefono or 'No indicado'}</td></tr>
                <tr><td style="padding:4px 0; color:#7C6FCD;"><strong>Empresa</strong></td><td>{req.empresa}</td></tr>
            </table>
        </div>

        <div style="background:#fff; padding:24px; border:1px solid #E0DCF5; border-top:none;">
            <h2 style="color:#2D2660; font-size:14px; text-transform:uppercase; letter-spacing:1px; margin:0 0 12px;">Propuesta generada</h2>
            <table style="width:100%; font-size:14px; color:#333;">
                <tr><td style="padding:6px 0; color:#7C6FCD; width:140px; vertical-align:top;"><strong>Proyecto</strong></td><td><strong>{req.proyecto}</strong></td></tr>
                <tr><td style="padding:6px 0; color:#7C6FCD; vertical-align:top;"><strong>Complejidad</strong></td><td>{req.complejidad}</td></tr>
                <tr><td style="padding:6px 0; color:#7C6FCD; vertical-align:top;"><strong>Tiempo estimado</strong></td><td>{req.tiempo_estimado}</td></tr>
                <tr><td style="padding:6px 0; color:#7C6FCD; vertical-align:top;"><strong>Tecnologías</strong></td><td>{req.tecnologias}</td></tr>
                <tr><td style="padding:6px 0; color:#7C6FCD; vertical-align:top;"><strong>Resumen</strong></td><td>{req.resumen}</td></tr>
                <tr><td style="padding:6px 0; color:#7C6FCD; vertical-align:top;"><strong>Funcionalidades</strong></td><td>{req.funcionalidades}</td></tr>
                <tr><td style="padding:6px 0; color:#7C6FCD; vertical-align:top;"><strong>Beneficios</strong></td><td>{req.beneficios}</td></tr>
            </table>
            {f'<div style="margin-top:16px; padding:12px; background:#FFF3F3; border-radius:6px; font-size:14px; color:#333;"><strong style="color:#E24B4A;">Mensaje del cliente:</strong><br>{req.mensaje}</div>' if req.mensaje else ''}
        </div>

        <div style="background:#2D2660; padding:12px 24px; border-radius:0 0 8px 8px; text-align:center;">
            <p style="color:#B8B0F0; font-size:12px; margin:0;">EstimAI · Estimador de Proyectos con IA</p>
        </div>
    </div>
    """

    resend.Emails.send({
        "from": "EstimAI <onboarding@resend.dev>",
        "to": os.getenv("CONTACT_EMAIL"),
        "subject": f"EstimAI · {emoji} {tipo_label} · {req.empresa}",
        "html": html
    })

    return {"status": "enviado"}
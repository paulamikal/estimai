const URL_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export async function obtenerPreguntas(infoEmpresa) {
    const respuesta = await fetch(`${URL_BASE}/questions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(infoEmpresa)
    })
    return await respuesta.json()
}

export async function generarEstimacion(solicitud) {
    const respuesta = await fetch(`${URL_BASE}/estimate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(solicitud)
    })
    return await respuesta.json()
}

export async function enviarContacto(datosContacto) {
    const respuesta = await fetch(`${URL_BASE}/contact`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datosContacto)
    })
    return await respuesta.json()
}
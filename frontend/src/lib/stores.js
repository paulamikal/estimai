import { writable } from 'svelte/store'

export const pasoActual = writable(0)

export const datosEmpresa = writable({
    empresa: '',
    rubro: '',
    actividad: '',
    necesidad: ''
})

export const preguntasDinamicas = writable([])

export const respuestasDinamicas = writable([])

export const resultado = writable(null)

export const cargando = writable(false)

export function reiniciar() {
    pasoActual.set(0)
    datosEmpresa.set({ empresa: '', rubro: '', actividad: '', necesidad: '' })
    preguntasDinamicas.set([])
    respuestasDinamicas.set([])
    resultado.set(null)
    cargando.set(false)
}
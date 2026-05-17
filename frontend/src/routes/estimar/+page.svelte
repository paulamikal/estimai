<script>
    import { obtenerPreguntas, generarEstimacion, enviarContacto } from '$lib/api.js'
    import logo from '$lib/assets/logo.png'
    import { pasoActual, datosEmpresa, preguntasDinamicas, respuestasDinamicas, resultado, cargando, reiniciar } from '$lib/stores.js'
    import { goto } from '$app/navigation'
    import { jsPDF } from 'jspdf'

    let mostrarContacto = $state(false)
    let tipoContacto = $state('')
    let datosContacto = $state({ nombre: '', email: '', telefono: '', mensaje: '' })
    let mensajeEnviado = $state(false)
    let errorCampo = $state('')

    const pasosBase = [
        { clave: 'empresa', titulo: '¿Cuál es el nombre de tu empresa?', placeholder: 'Ej: Agrocow SpA' },
        { clave: 'rubro', titulo: '¿A qué rubro o industria pertenece?', placeholder: 'Ej: Agronomía, Retail, Salud...' },
        { clave: 'actividad', titulo: '¿Cuál es la actividad principal de tu empresa?', placeholder: 'Ej: Cosecha y venta de avena, gestión administrativa...' },
        { clave: 'necesidad', titulo: '¿Qué necesitas automatizar o mejorar?', placeholder: 'Ej: Automatizar el inventario según fechas de cosecha...' }
    ]

    let totalPasos = $derived(pasosBase.length + $preguntasDinamicas.length)
    let progreso = $derived($pasoActual === 0 ? 0 : Math.round(($pasoActual / (totalPasos + 1)) * 100))

    async function siguiente() {
        const paso = pasosBase[$pasoActual]
        if (paso && !$datosEmpresa[paso.clave]) {
            errorCampo = 'Este campo es obligatorio'
            return
        }
        errorCampo = ''

        if ($pasoActual === pasosBase.length - 1) {
            $cargando = true
            const res = await obtenerPreguntas($datosEmpresa)
            $preguntasDinamicas = res.preguntas
            $respuestasDinamicas = new Array(res.preguntas.length).fill('')
            $cargando = false
        }

        $pasoActual++

        if ($pasoActual === totalPasos) {
            await generarResultado()
        }
    }

    async function generarResultado() {
        $cargando = true
        const res = await generarEstimacion({
            ...$datosEmpresa,
            preguntas: $preguntasDinamicas,
            respuestas: $respuestasDinamicas
        })
        $resultado = res
        $cargando = false
    }

    function anterior() {
        if ($pasoActual > 0) $pasoActual--
        errorCampo = ''
        mostrarContacto = false
    }

    function abrirContacto(tipo) {
        tipoContacto = tipo
        mostrarContacto = true
        mensajeEnviado = false
    }

    async function enviar() {
        if (!datosContacto.nombre || !datosContacto.email) {
            errorCampo = 'Nombre y correo son obligatorios'
            return
        }
        errorCampo = ''
        $cargando = true
        await enviarContacto({
            ...datosContacto,
            tipo: tipoContacto,
            empresa: $datosEmpresa.empresa,
            proyecto: $resultado?.titulo_proyecto || '',
            complejidad: $resultado?.complejidad || '',
            tiempo_estimado: $resultado?.tiempo_estimado || '',
            tecnologias: $resultado?.tecnologias_sugeridas?.join(', ') || '',
            resumen: $resultado?.resumen_ejecutivo || '',
            funcionalidades: $resultado?.funcionalidades_clave?.join(' · ') || '',
            beneficios: $resultado?.beneficios || ''
        })
        $cargando = false
        mensajeEnviado = true
    }

    function claseInsignia(complejidad) {
        if (complejidad === 'Alta') return 'insignia insignia-alta'
        if (complejidad === 'Media') return 'insignia insignia-media'
        return 'insignia insignia-baja'
    }

    function exportarPDF() {
        const r = $resultado
        const doc = new jsPDF()

        const azul = [45, 38, 96]
        const violeta = [124, 111, 205]
        const lavanda = [184, 176, 240]
        const gris = [160, 155, 184]
        const blanco = [240, 239, 249]
        const fondoClaro = [245, 244, 252]
        const oscuro = [30, 25, 60]

        // Header principal
        doc.setFillColor(...azul)
        doc.rect(0, 0, 210, 50, 'F')

        doc.setFillColor(124, 111, 205)
        doc.rect(0, 46, 210, 4, 'F')

        doc.setFontSize(22)
        doc.setTextColor(...blanco)
        doc.setFont('helvetica', 'bold')
        doc.text($datosEmpresa.empresa, 15, 22)

        doc.setFontSize(12)
        doc.setFont('helvetica', 'normal')
        doc.setTextColor(...lavanda)
        doc.text($datosEmpresa.rubro, 15, 32)

        doc.setFontSize(9)
        doc.setTextColor(...gris)
        doc.text('Propuesta de proyecto generada por EstimAI', 15, 42)

        doc.setFontSize(9)
        doc.setTextColor(...gris)
        doc.text(new Date().toLocaleDateString('es-CL', { year: 'numeric', month: 'long', day: 'numeric' }), 195, 42, { align: 'right' })

        let y = 62

        // Título del proyecto destacado
        doc.setFillColor(...fondoClaro)
        doc.roundedRect(12, y - 6, 186, 22, 4, 4, 'F')
        doc.setFontSize(14)
        doc.setTextColor(...oscuro)
        doc.setFont('helvetica', 'bold')
        doc.text(r.titulo_proyecto, 15, y + 8)
        y += 26

        function fila(etiqueta, valor, fondoAlternado = false) {
            const altoFila = 10
            const lineas = doc.splitTextToSize(valor, 130)
            const alto = Math.max(altoFila, lineas.length * 6 + 6)

            if (fondoAlternado) {
                doc.setFillColor(...fondoClaro)
                doc.rect(12, y - 4, 186, alto, 'F')
            }

            doc.setFontSize(8)
            doc.setTextColor(...violeta)
            doc.setFont('helvetica', 'bold')
            doc.text(etiqueta.toUpperCase(), 15, y + 2)

            doc.setFontSize(10)
            doc.setTextColor(...oscuro)
            doc.setFont('helvetica', 'normal')
            doc.text(lineas, 65, y + 2)

            doc.setDrawColor(200, 196, 230)
            doc.setLineWidth(0.2)
            doc.line(12, y + alto, 198, y + alto)

            y += alto + 4

            if (y > 265) {
                doc.addPage()
                y = 20
            }
        }

        fila('Resumen', r.resumen_ejecutivo, false)
        fila('Complejidad', r.complejidad, true)
        fila('Tiempo estimado', r.tiempo_estimado, false)
        fila('Tecnologías', r.tecnologias_sugeridas.join(' · '), true)
        fila('Beneficios', r.beneficios, false)

        // Funcionalidades como lista visual
        y += 4
        doc.setFontSize(8)
        doc.setTextColor(...violeta)
        doc.setFont('helvetica', 'bold')
        doc.text('FUNCIONALIDADES CLAVE', 15, y)
        y += 6

        r.funcionalidades_clave.forEach((func, i) => {
            if (y > 265) { doc.addPage(); y = 20 }
            const alterno = i % 2 === 0
            if (alterno) {
                doc.setFillColor(...fondoClaro)
                doc.rect(12, y - 3, 186, 10, 'F')
            }
            doc.setFillColor(...violeta)
            doc.circle(19, y + 2, 1.5, 'F')
            doc.setFontSize(10)
            doc.setTextColor(...oscuro)
            doc.setFont('helvetica', 'normal')
            const lineas = doc.splitTextToSize(func, 160)
            doc.text(lineas, 24, y + 2)
            y += lineas.length * 6 + 4
        })

        y += 4
        fila('Próximos pasos', r.proximos_pasos, false)

        // Footer
        doc.setFillColor(...azul)
        doc.rect(0, 285, 210, 12, 'F')
        doc.setFontSize(8)
        doc.setTextColor(...lavanda)
        doc.setFont('helvetica', 'normal')
        doc.text('EstimAI · Estimador de Proyectos con IA', 15, 293)
        doc.text('estimai.app', 195, 293, { align: 'right' })

        doc.save(`EstimAI_${$datosEmpresa.empresa.replace(/\s/g, '_')}.pdf`)
    }

</script>

<main style="min-height:100vh; padding: 2rem 1rem; display:flex; align-items:flex-start; justify-content:center;">
    <div style="width:100%; max-width:680px;">

        <div style="display:flex; align-items:center; gap:10px; margin-bottom:2rem;">
        <img src={logo} alt="EstimAI logo" style="height:36px; width:auto;">
        <span style="font-size:20px; font-weight:500; color:#F0EFF9; letter-spacing:-0.3px;">EstimAI</span>
        </div>

        {#if $resultado}
            <div class="barra-progreso"><div class="barra-progreso-relleno" style="width:100%"></div></div>
        {:else}
            <div class="barra-progreso"><div class="barra-progreso-relleno" style="width:{progreso}%"></div></div>
        {/if}

        {#if $cargando}
            <div class="tarjeta" style="display:flex; align-items:center; gap:12px;">
                <div class="spinner"></div>
                <span style="color:#A09BB8; font-size:14px;">
                    {$pasoActual === pasosBase.length ? 'Generando preguntas específicas...' : 'Generando tu propuesta...'}
                </span>
            </div>

        {:else if $resultado}
            <div class="tarjeta" style="padding:0; overflow:hidden;">
                <div style="background:#2D2660; padding:1.5rem; border-bottom: 0.5px solid #3D3570;">
                    <p style="font-size:12px; color:rgba(255,255,255,0.7); margin-bottom:4px;">Propuesta generada</p>
                    <p style="font-size:22px; font-weight:500; color:#fff;">{$datosEmpresa.empresa}</p>
                    <p style="font-size:13px; color:rgba(255,255,255,0.75);">{$datosEmpresa.rubro}</p>
                </div>

                <div style="padding:1.5rem;">
                    <div style="margin-bottom:1.2rem; padding-bottom:1.2rem; border-bottom:1px solid #2D2660;">
                        <p class="etiqueta">Proyecto</p>
                        <p style="font-size:20px; font-weight:300; color:#fff;">{$resultado.titulo_proyecto}</p>
                    </div>

                    <div style="margin-bottom:1.2rem; padding-bottom:1.2rem; border-bottom:1px solid #2D2660;">
                        <p class="etiqueta">Resumen ejecutivo</p>
                        <p style="font-size:14px; color:#A09BB8; line-height:1.6;">{$resultado.resumen_ejecutivo}</p>
                    </div>

                    <div style="margin-bottom:1.2rem; padding-bottom:1.2rem; border-bottom:1px solid #2D2660;">
                        <p class="etiqueta">Funcionalidades clave</p>
                        <ul style="list-style:none; padding:0; margin-top:6px;">
                            {#each $resultado.funcionalidades_clave as func}
                                <li style="font-size:14px; color:#A09BB8; margin-bottom:4px;">· {func}</li>
                            {/each}
                        </ul>
                    </div>

                    <div style="display:flex; gap:2rem; margin-bottom:1.2rem; padding-bottom:1.2rem; border-bottom:1px solid #2D2660; flex-wrap:wrap;">
                        <div>
                            <p class="etiqueta">Complejidad</p>
                            <span class={claseInsignia($resultado.complejidad)}>{$resultado.complejidad}</span>
                        </div>
                        <div>
                            <p class="etiqueta">Tiempo estimado</p>
                            <p style="font-size:14px; font-weight:500; color:#fff;">{$resultado.tiempo_estimado}</p>
                        </div>
                    </div>

                    <div style="margin-bottom:1.2rem; padding-bottom:1.2rem; border-bottom:1px solid #2D2660;">
                        <p class="etiqueta">Tecnologías sugeridas</p>
                        <div style="display:flex; gap:6px; flex-wrap:wrap; margin-top:6px;">
                            {#each $resultado.tecnologias_sugeridas as tech}
                                <span class="etiqueta-tech">{tech}</span>
                            {/each}
                        </div>
                    </div>

                    <div style="margin-bottom:1.2rem; padding-bottom:1.2rem; border-bottom:1px solid #2D2660;">
                        <p class="etiqueta">Beneficios esperados</p>
                        <p style="font-size:14px; color:#A09BB8; line-height:1.6;">{$resultado.beneficios}</p>
                    </div>

                    <div style="margin-bottom:1.5rem;">
                        <p class="etiqueta">Próximos pasos</p>
                        <p style="font-size:14px; color:#A09BB8; line-height:1.6;">{$resultado.proximos_pasos}</p>
                    </div>

                    <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center;">
                        <button class="btn-peligro" onclick={() => abrirContacto('no-resuelta')}>
                            ⚠ Idea no resuelta
                        </button>
                        <div style="flex:1"></div>
                        <button class="btn-secundario" onclick={exportarPDF}>↓ Exportar PDF</button>
                        <button class="btn-secundario" onclick={reiniciar}>Nueva estimación</button>
                        <button class="btn-primario" onclick={() => abrirContacto('confirma')}>
                            ✓ ¡Esta es mi idea!
                        </button>
                    </div>

                    {#if mostrarContacto}
                        <div class="tarjeta-clara" style="margin-top:1.5rem;">
                            {#if tipoContacto === 'confirma'}
                                <p style="font-size:14px; font-weight:500; color:#7C6FCD; margin-bottom:0.3rem;">¡Excelente! Ya podemos comenzar</p>
                                <p style="font-size:13px; color:#A09BB8; margin-bottom:1rem;">Completa tus datos y nuestro equipo te contactará pronto.</p>
                            {:else}
                                <p style="font-size:14px; font-weight:500; color:#E24B4A; margin-bottom:0.3rem;">Idea no resuelta</p>
                                <p style="font-size:13px; color:#A09BB8; margin-bottom:1rem;">Cuéntanos qué faltó y un especialista te contactará.</p>
                            {/if}

                            <div style="display:flex; flex-direction:column; gap:0.8rem;">
                                <div>
                                    <p class="etiqueta">Nombre completo</p>
                                    <input type="text" bind:value={datosContacto.nombre} placeholder="Tu nombre">
                                </div>
                                <div>
                                    <p class="etiqueta">Correo electrónico</p>
                                    <input type="email" bind:value={datosContacto.email} placeholder="tu@correo.com">
                                </div>
                                <div>
                                    <p class="etiqueta">Teléfono (opcional)</p>
                                    <input type="text" bind:value={datosContacto.telefono} placeholder="+56 9 xxxx xxxx">
                                </div>
                                {#if tipoContacto === 'no-resuelta'}
                                    <div>
                                        <p class="etiqueta">¿Qué faltó o no quedó claro?</p>
                                        <textarea bind:value={datosContacto.mensaje} rows="3" placeholder="Describe brevemente..."></textarea>
                                    </div>
                                {/if}

                                {#if errorCampo}
                                    <p style="color:#F09595; font-size:13px;">{errorCampo}</p>
                                {/if}

                                {#if mensajeEnviado}
                                    <div class="mensaje-exito">✓ Mensaje enviado correctamente. Nos pondremos en contacto pronto.</div>
                                    <div style="display:flex; gap:10px; margin-top:1rem;">
                                            <button class="btn-secundario" onclick={reiniciar}>Nueva estimación</button>
                                            <button class="btn-primario" onclick={() => goto('/')}>← Volver al inicio</button>
                                </div>
                                {:else}
                                    <div style="display:flex; gap:10px;">
                                        <button class="btn-primario" onclick={enviar} disabled={$cargando}>
                                            {$cargando ? 'Enviando...' : 'Enviar mensaje'}
                                        </button>
                                        <button class="btn-secundario" onclick={() => mostrarContacto = false}>Cancelar</button>
                                    </div>
                                {/if}
                            </div>
                        </div>
                    {/if}
                </div>
            </div>

        {:else if $pasoActual < pasosBase.length}
            <div class="tarjeta">
                <p class="etiqueta">Paso {$pasoActual + 1} de {pasosBase.length}</p>
                <h2 style="font-size:22px; font-weight:300; color:#fff; margin-bottom:0.4rem; line-height:1.3;">
                    {pasosBase[$pasoActual].titulo}
                </h2>
                <p style="font-size:13px; color:#A09BB8; margin-bottom:1.5rem;">Cuanta más información, mejor la estimación.</p>

                {#if $pasoActual === 2 || $pasoActual === 3}
                    <textarea
                        rows="4"
                        placeholder={pasosBase[$pasoActual].placeholder}
                        bind:value={$datosEmpresa[pasosBase[$pasoActual].clave]}
                    ></textarea>
                {:else}
                    <input
                        type="text"
                        placeholder={pasosBase[$pasoActual].placeholder}
                        bind:value={$datosEmpresa[pasosBase[$pasoActual].clave]}
                    />
                {/if}

                {#if errorCampo}
                    <p style="color:#F09595; font-size:13px; margin-top:6px;">{errorCampo}</p>
                {/if}

                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:1.5rem;">
                    {#if $pasoActual > 0}
                        <button class="btn-secundario" onclick={anterior}>← Atrás</button>
                    {:else}
                        <button class="btn-secundario" onclick={() => goto('/')}>← Inicio</button>
                    {/if}
                    <button class="btn-primario" onclick={siguiente}>
                        Continuar →
                    </button>
                </div>
            </div>

        {:else}
            {@const idxDinamico = $pasoActual - pasosBase.length}
            <div class="tarjeta">
                <p class="etiqueta">Pregunta {idxDinamico + 1} de {$preguntasDinamicas.length} · Profundizando tu proyecto</p>
                <h2 style="font-size:20px; font-weight:300; color:#fff; margin-bottom:0.4rem; line-height:1.3;">
                    {$preguntasDinamicas[idxDinamico]}
                </h2>
                <p style="font-size:13px; color:#A09BB8; margin-bottom:1.5rem;">Cuanta más información, mejor la estimación.</p>

                <textarea
                    rows="4"
                    placeholder="Tu respuesta..."
                    bind:value={$respuestasDinamicas[idxDinamico]}
                ></textarea>

                {#if errorCampo}
                    <p style="color:#F09595; font-size:13px; margin-top:6px;">{errorCampo}</p>
                {/if}

                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:1.5rem;">
                    <button class="btn-secundario" onclick={anterior}>← Atrás</button>
                    <button class="btn-primario" onclick={siguiente}>
                        {idxDinamico === $preguntasDinamicas.length - 1 ? 'Generar propuesta →' : 'Continuar →'}
                    </button>
                </div>
            </div>
        {/if}

    </div>
</main>
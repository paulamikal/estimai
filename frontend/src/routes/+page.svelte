<script>
    import logo from '$lib/assets/logo.png'
</script>

<main style="min-height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 2rem 1rem; position:relative; overflow:hidden;">

    <div style="position:absolute; width:600px; height:600px; border-radius:50%; background:rgba(124,111,205,0.06); top:-100px; left:-150px; pointer-events:none;"></div>
    <div style="position:absolute; width:400px; height:400px; border-radius:50%; background:rgba(124,111,205,0.05); bottom:-80px; right:-100px; pointer-events:none;"></div>

    <div style="text-align:center; max-width:580px; position:relative; z-index:1;">

        <div style="display:flex; align-items:center; justify-content:center; gap:12px; margin-bottom:3rem;">
            <img src={logo} alt="EstimAI logo" style="height:48px; width:auto;">
            <span style="font-size:26px; font-weight:500; color:#F0EFF9; letter-spacing:-0.5px;">EstimAI</span>
        </div>

        <h1 style="font-size:42px; font-weight:500; color:#F0EFF9; line-height:1.15; letter-spacing:-1px; margin-bottom:1.2rem;">
            Convierte tu idea en una<br>
            <span style="color:#7C6FCD;">propuesta real</span>
        </h1>

        <p style="font-size:17px; color:#A09BB8; line-height:1.7; margin-bottom:2.5rem; max-width:460px; margin-left:auto; margin-right:auto;">
            Responde unas preguntas simples y nuestra IA generará un levantamiento de requerimientos completo para tu proyecto de software, sin reuniones innecesarias.
        </p>

        <a href="/estimar" style="display:inline-block; background:#7C6FCD; color:#F0EFF9; text-decoration:none; border-radius:10px; padding:14px 36px; font-size:16px; font-weight:500; transition:background 0.2s; letter-spacing:-0.2px;">
            Comenzar estimación →
        </a>

        <div style="display:flex; justify-content:center; gap:2.5rem; margin-top:4rem; flex-wrap:wrap;">
            <div style="text-align:center;">
                <p style="font-size:22px; font-weight:500; color:#B8B0F0;">5 min</p>
                <p style="font-size:12px; color:#A09BB8; margin-top:2px;">tiempo promedio</p>
            </div>
            <div style="width:0.5px; background:#2D2660;"></div>
            <div style="text-align:center;">
                <p style="font-size:22px; font-weight:500; color:#B8B0F0;">100%</p>
                <p style="font-size:12px; color:#A09BB8; margin-top:2px;">guiado por IA</p>
            </div>
            <div style="width:0.5px; background:#2D2660;"></div>
            <div style="text-align:center;">
                <p style="font-size:22px; font-weight:500; color:#B8B0F0;">0 reuniones</p>
                <p style="font-size:12px; color:#A09BB8; margin-top:2px;">para empezar</p>
            </div>
        </div>

    </div>

    <p style="position:absolute; bottom:1.5rem; font-size:12px; color:#3D3570;">
        © 2026 EstimAI · Made with love | Paula Mikal · Todos los derechos reservados
    </p>

</main>
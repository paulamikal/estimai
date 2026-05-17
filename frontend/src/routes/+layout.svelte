<script>
    import '../app.css'

    let { children } = $props()
</script>

<svelte:head>
    <title>EstimAI · Estimador de Proyectos</title>
</svelte:head>

{@render children()}
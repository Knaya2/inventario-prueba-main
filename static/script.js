// Efecto de animación al cargar la página
document.addEventListener("DOMContentLoaded", () => {
    console.log("Inventario cargado 🚀");

    // Animación rápida de tabla
    const rows = document.querySelectorAll("tbody tr");
    rows.forEach((row, i) => {
        row.style.opacity = 0;
        setTimeout(() => {
            row.style.transition = "opacity 0.5s ease";
            row.style.opacity = 1;
        }, i * 150);
    });
});

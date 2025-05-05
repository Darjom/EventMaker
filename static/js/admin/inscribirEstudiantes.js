console.log("Este js se lee correctamentee")
document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("modal-inscripcion");
    const btnAbrir = document.getElementById("btn-abrir-modal");
    const btnCerrar = document.getElementById("btn-cerrar-modal");
    const main = document.getElementById("main-content");
  
    // 1) Abrir modal SOLO al hacer clic en ese botón
    btnAbrir.addEventListener("click", function (e) {
      e.preventDefault();               // evita que href="#" navegue
      modal.style.display = "block";
      modal.style.display = "flex";
      main.style.filter  = "blur(3px)";
    });
  
    // 2) Cerrar modal con el botón “Cancelar”
    btnCerrar.addEventListener("click", function () {
      modal.style.display = "none";
      main.style.filter  = "none";
    });
  
    // 3) Cerrar modal si clicas fuera de él
    window.addEventListener("click", function (e) {
      if (e.target === modal) {
        modal.style.display = "none";
        main.style.filter  = "none";
      }
    });
  });
  
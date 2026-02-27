const API_BASE_URL = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
  ? "http://127.0.0.1:8000"
  : window.location.origin;

const form = document.getElementById("form-evaluacion");
const btnEvaluar = document.getElementById("btn-evaluar");
const spinner = document.getElementById("spinner");
const resultadoContenido = document.getElementById("resultado-contenido");
const nivelRiesgoEl = document.getElementById("nivel-riesgo");
const mensajeErrorEl = document.getElementById("mensaje-error");
const detalleValoresEl = document.getElementById("detalle-valores");
const estadoApiEl = document.getElementById("estado-api");

const inputSueno = document.getElementById("sueño");
const inputCarga = document.getElementById("carga");
const inputAnsiedad = document.getElementById("ansiedad");

const gifContainer = document.getElementById("gif-resultado");
const gifImage = document.getElementById("imagen-gif");

function conectarSlider(input, outputId) {
  const output = document.getElementById(outputId);
  output.textContent = input.value;

  input.addEventListener("input", () => {
    output.textContent = input.value;
  });
}

conectarSlider(inputSueno, "valor-sueño");
conectarSlider(inputCarga, "valor-carga");
conectarSlider(inputAnsiedad, "valor-ansiedad");


verificarEstadoApi();

function setCargando(estado) {
  spinner.classList.toggle("hidden", !estado);
  btnEvaluar.disabled = estado;
}

function clasNombreClaseRiesgo(nivel) {
  const texto = nivel.toLowerCase();
  if (texto.includes("alto")) return "alto";
  if (texto.includes("moderado")) return "medio";
  if (texto.includes("leve")) return "leve";
  return "";
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const sueno = parseInt(inputSueno.value);
  const carga = parseInt(inputCarga.value);
  const ansiedad = parseInt(inputAnsiedad.value);

  if (isNaN(sueno) || isNaN(carga) || isNaN(ansiedad)) {
    mensajeErrorEl.textContent = "Todos los campos son obligatorios.";
    mensajeErrorEl.classList.remove("hidden");
    return;
  }

  setCargando(true);
  mensajeErrorEl.classList.add("hidden");
  resultadoContenido.classList.add("hidden");

  try {
    const response = await fetch(
      `${API_BASE_URL}/api/evaluar-estres?sueno=${sueno}&carga=${carga}&ansiedad=${ansiedad}`
    );

    const data = await response.json();

    nivelRiesgoEl.textContent = data.nivel;
    nivelRiesgoEl.className = "resultado-valor";


    const clase = clasNombreClaseRiesgo(data.nivel);
    if (clase) nivelRiesgoEl.classList.add(clase);

    detalleValoresEl.innerHTML = `
      <li>Horas de sueño: ${sueno}</li>
      <li>Número de materias: ${carga}</li>
      <li>Nivel de ansiedad: ${ansiedad}</li>
      <li>Valor difuso: ${data.valor_fuzzy}</li>
    `;

    resultadoContenido.classList.remove("hidden");

    // --- Mostrar GIF según nivel ---

    gifContainer.classList.add("hidden");
    gifImage.src = "";

    const claseGif = clasNombreClaseRiesgo(data.nivel);

    if (claseGif === "leve") {
      gifImage.src = "../assets/bajo2.gif";
      gifContainer.classList.remove("hidden");
    }
    else if (claseGif === "medio") {
      gifImage.src = "../assets/medio2.gif";
      gifContainer.classList.remove("hidden");
    }
    else if (claseGif === "alto") {
      gifImage.src = "../assets/alto2.gif";
      gifContainer.classList.remove("hidden");
    }

  } catch (err) {
    mensajeErrorEl.textContent =
      "Error al conectar con la API. Verifica que esté corriendo.";
    mensajeErrorEl.classList.remove("hidden");
  } finally {
    setCargando(false);
  }
});
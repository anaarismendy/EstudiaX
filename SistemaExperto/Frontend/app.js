// Cambia esto si tu API corre en otro host/puerto.
const API_BASE_URL = "http://127.0.0.1:8000";

const form = document.getElementById("form-evaluacion");
const btnEvaluar = document.getElementById("btn-evaluar");
const spinner = document.getElementById("spinner");
const resultadoContenido = document.getElementById("resultado-contenido");
const nivelRiesgoEl = document.getElementById("nivel-riesgo");
const mensajeErrorEl = document.getElementById("mensaje-error");
const detalleValoresEl = document.getElementById("detalle-valores");
const estadoApiEl = document.getElementById("estado-api");

const gifContainer = document.getElementById("gif-resultado");
const gifImage = document.getElementById("imagen-gif");


// Inputs
const inputPromedio = document.getElementById("promedio");
const inputInasistencias = document.getElementById("inasistencias");
const inputParticipacion = document.getElementById("participacion");
const inputHorasEstudio = document.getElementById("horas_estudio");

function activarSlider(inputId, outputId) {
  const input = document.getElementById(inputId);
  const output = document.getElementById(outputId);

  output.textContent = input.value;

  input.addEventListener("input", () => {
    output.textContent = input.value;
  });
}

activarSlider("inasistencias", "valor-inasistencias");
activarSlider("participacion", "valor-participacion");
activarSlider("horas_estudio", "valor-horas_estudio");

// Detectar estado de la API en el inicio
async function verificarEstadoApi() {
  try {
    const res = await fetch(`${API_BASE_URL}/`);
    if (!res.ok) throw new Error("Respuesta no OK");
    const data = await res.json();
    estadoApiEl.textContent = `Estado API: ${data.mensaje ?? "Activa"}`;
  } catch (err) {
    estadoApiEl.textContent =
      "Estado API: No disponible. Verifica que el servidor FastAPI esté corriendo.";
    estadoApiEl.style.color = "#f97373";
  }
}

verificarEstadoApi();

// Helpers de UI
function limpiarMensajesError() {
  mensajeErrorEl.classList.add("hidden");
  mensajeErrorEl.textContent = "";

  document
    .querySelectorAll(".error-message")
    .forEach((el) => (el.textContent = ""));
  [inputPromedio, inputInasistencias, inputParticipacion, inputHorasEstudio].forEach(
    (input) => input.classList.remove("error")
  );
}

function mostrarErrorGeneral(mensaje) {
  mensajeErrorEl.textContent = mensaje;
  mensajeErrorEl.classList.remove("hidden");
}

function setCargando(isLoading) {
  if (isLoading) {
    spinner.classList.remove("hidden");
    btnEvaluar.disabled = true;
  } else {
    spinner.classList.add("hidden");
    btnEvaluar.disabled = false;
  }
}

function clasNombreClaseRiesgo(nivel) {
  const texto = (nivel || "").toLowerCase();
  if (texto.includes("alto")) return "alto";
  if (texto.includes("medio")) return "medio";
  if (texto.includes("bajo")) return "bajo";
  return "";
}

function actualizarDetalleValores(valores) {
  detalleValoresEl.innerHTML = "";
  Object.entries(valores).forEach(([clave, valor]) => {
    const li = document.createElement("li");
    li.textContent = `${clave}: ${valor}`;
    detalleValoresEl.appendChild(li);
  });
}

// Validación sencilla de los campos antes de enviar al backend
function validarCampos() {
  let valido = true;
  limpiarMensajesError();

  const setError = (input, mensaje) => {
    const errorEl = document.querySelector(
      `.error-message[data-error-for="${input.id}"]`
    );
    if (errorEl) errorEl.textContent = mensaje;
    input.classList.add("error");
    valido = false;
  };

  const promedioVal = parseFloat(inputPromedio.value);
  if (isNaN(promedioVal)) {
    setError(inputPromedio, "Ingresa un promedio numérico.");
  } else if (promedioVal < 0 || promedioVal > 5) {
    setError(inputPromedio, "El promedio debe estar entre 0.0 y 5.0.");
  }

  const inasistenciasVal = parseInt(inputInasistencias.value, 10);
  if (isNaN(inasistenciasVal) || inasistenciasVal < 0) {
    setError(inputInasistencias, "Ingresa un entero mayor o igual a 0.");
  }

  const participacionVal = parseInt(inputParticipacion.value, 10);
  if (isNaN(participacionVal)) {
    setError(inputParticipacion, "Ingresa un valor entre 1 y 10.");
  } else if (participacionVal < 1 || participacionVal > 10) {
    setError(inputParticipacion, "La participación debe estar entre 1 y 10.");
  }

  const horasVal = parseFloat(inputHorasEstudio.value);
  if (isNaN(horasVal) || horasVal < 0) {
    setError(
      inputHorasEstudio,
      "Ingresa una cantidad de horas mayor o igual a 0."
    );
  }

  return valido;
}

// Manejo de envío del formulario
form.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!validarCampos()) {
    return;
  }

  const payload = {
    promedio: parseFloat(inputPromedio.value),
    inasistencias: parseInt(inputInasistencias.value, 10),
    participacion: parseInt(inputParticipacion.value, 10),
    horas_estudio: parseFloat(inputHorasEstudio.value),
  };

  setCargando(true);
  resultadoContenido.classList.add("hidden");
  nivelRiesgoEl.textContent = "";
  nivelRiesgoEl.className = "resultado-valor";

  try {
    const response = await fetch(`${API_BASE_URL}/evaluar-riesgo`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      let detalle = "";
      try {
        const errData = await response.json();
        detalle = errData.detail || JSON.stringify(errData);
      } catch {
        // ignorar error de parseo
      }
      throw new Error(
        `Error al llamar a la API (${response.status}). ${detalle}`
      );
    }

    const data = await response.json();
    const nivel = data.nivel_riesgo || "No determinado";

    nivelRiesgoEl.textContent = nivel;
    const claseRiesgo = clasNombreClaseRiesgo(nivel);
    if (claseRiesgo) {
      nivelRiesgoEl.classList.add(claseRiesgo);
    }

    resultadoContenido.classList.remove("hidden");
    actualizarDetalleValores(payload);
    // --- MANEJO DE GIF SEGÚN NIVEL ---

    // Ocultamos primero por seguridad
    gifContainer.classList.add("hidden");

    const claseGif = clasNombreClaseRiesgo(nivel);

    if (claseGif === "bajo") {
      gifImage.src = "assets/gifs/bajo.gif";
      gifContainer.classList.remove("hidden");
    }

    if (claseGif === "medio") {
      gifImage.src = "assets/gifs/medio.gif";
      gifContainer.classList.remove("hidden");
    }

    if (claseGif === "alto") {
      gifImage.src = "assets/gifs/alto.gif";
      gifContainer.classList.remove("hidden");
    }

  } catch (err) {
    console.error(err);
    mostrarErrorGeneral(
      "No se pudo obtener el resultado. Verifica que la API esté activa y vuelve a intentarlo."
    );


    gifContainer.classList.remove("hidden");
  } finally {
    setCargando(false);
  }

});
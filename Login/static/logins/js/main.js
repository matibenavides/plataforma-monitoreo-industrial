
const charts = {};

// ---------------------------------------------------
// Función Debounce para mejorar rendimiento de redimensión
// ---------------------------------------------------
function debounce(func, wait, immediate) {
  var timeout;
  return function() {
    var context = this, args = arguments;
    var later = function() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    var callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
};

// ---------------------------------------------------
// Chart Cloracion de Hipoclorito y Ácido
// ---------------------------------------------------

const getOptionChartHipoAci= async (params = {})=>{
  const query = new URLSearchParams(params);
  try{
    const response = await fetch("http://127.0.0.1:8000/grafico_cloracion/?" + query.toString())
    return await response.json();
  }catch(ex) {
    alert("Error al botener los datos: " + ex);
  }
};

const initChartHipoAci = async (params = {}) => {

  if (!charts.hipoAci) {
    charts.hipoAci = echarts.init(document.getElementById("chartCloroAcido"));
  }
  
  let option = await getOptionChartHipoAci(params);
  charts.hipoAci.setOption(option);
};

// ---------------------------------------------------
// Chart Temperatura
// ---------------------------------------------------

const getOptionChartTemperatura= async (params = {})=>{
  const query = new URLSearchParams(params);
  try{
    const response = await fetch("http://127.0.0.1:8000/grafico_temp/?" + query.toString())
    return await response.json();
  }catch(ex) {
    alert("Error al botener los datos: " + ex);
  }
};

const initChartTemperatura = async (params = {}) => {
  if (!charts.temperatura) {
    charts.temperatura = echarts.init(document.getElementById("chartTemperatura"));
  }
  
  let option = await getOptionChartTemperatura(params);

  if (option.xAxis && option.xAxis.type !== 'value') {
    option.xAxis.type = 'value';
    option.xAxis.min = 0;
    option.xAxis.max = 24;
    option.xAxis.interval = 3;
  }

  option.xAxis.axisLabel = {
    fontSize: 12,
    formatter: function(value) {
      const hora = Math.floor(value);
      return hora + ':00';
    }
  };



  option.tooltip.formatter = function(params) {
    const total = params.value[0];
    const hora = Math.floor(total);
    const minutos = Math.round((total - hora) * 60);

    const minutosformateado = minutos < 10 ? '0' + minutos : minutos;


    return `${params.seriesName}<br/>
            Hora: ${hora}:${minutosformateado}<br/>
            Temperatura: ${params.value[1]}°C`;
  };

  charts.temperatura.setOption(option);
};



// ---------------------------------------------------
// Chart PPM
// ---------------------------------------------------

const getOptionChartPPM= async (params = {})=>{
  const query = new URLSearchParams(params);
  try{
    const response = await fetch("http://127.0.0.1:8000/grafico_ppm/?" + query.toString())
    return await response.json();
  }catch(ex) {
    alert("Error al obtener datos de PPM" + ex);
  }
};

const initChartPPM = async (params = {}) => {
  if (!charts.ppm) {
    charts.ppm = echarts.init(document.getElementById("chartPPM"));
  }
  
  let option = await getOptionChartPPM(params);


  if (option.xAxis && option.xAxis.type !== 'value') {
    option.xAxis.type = 'value';
    option.xAxis.min = 0;
    option.xAxis.max = 24;
    option.xAxis.interval = 3;
  }

  option.xAxis.axisLabel = {
    fontSize: 12,
    formatter: function(value) {
      const hora = Math.floor(value);
      return hora + ':00';
    }
  };



  option.tooltip.formatter = function(params) {
    // Maneja params como array u objeto
    const pointParams = Array.isArray(params) ? params[0] : params;

    if (!pointParams || !pointParams.value || pointParams.value.length < 2) {
        return 'Información no disponible';
    }

    const seriesName = pointParams.seriesName; // Ej: "Estanque"
    const seriesId = pointParams.seriesId;     // Ej: "estanque-ppm", "corta-ph"
    const numericalTime = pointParams.value[0]; // Ej: 8.5, 9.0
    const value = pointParams.value[1];        // Ej: 120, 6.8

    


    // formateo de hora
    const hora = Math.floor(numericalTime);
    const minutosDecimal = (numericalTime - hora) * 60;
    const minutos = Math.round(minutosDecimal);
    const minutosFormateado = minutos < 10 ? '0' + minutos : minutos;
    const timeStr = `${hora}:${minutosFormateado}`;

    // metrica para valor ppm o ph
    let metricLabel = '';

    // según id de 'series' de json backend
    if (seriesId && seriesId.includes('-ppm')) { // Verificar si y contiene '-ppm'
        metricLabel = 'PPM';
    } else if (seriesId && seriesId.includes('-ph')) {
        metricLabel = 'pH';
    } else {
        metricLabel = 'Valor'; //por si acaso
    }

    // Construir el contenido HTML del tooltip
    // Usamos seriesName (Ej: "Estanque") como título principal
    return `${seriesName}<br/>
            Hora: ${timeStr}<br/>
            ${metricLabel}: ${value}`;
};

  charts.ppm.setOption(option);
};

// ---------------------------------------------------
// Chart Kilogramos Anual.
// ---------------------------------------------------

const getOptionChartKGS= async (params = {})=>{
  const query = new URLSearchParams(params);
  try{
    const response = await fetch("http://127.0.0.1:8000/grafico_kgs/?" + query.toString())
    return await response.json();
  }catch(ex) {
    alert("Error al obtener datos de Kilogramos" + ex);
  }
};

const initChartKGS = async (params = {}) => {
  if (!charts.kgs) {
    charts.kgs = echarts.init(document.getElementById("chartKilos"));
  }
  
  let option = await getOptionChartKGS(params);
  charts.kgs.setOption(option);
};

// ---------------------------------------------------
// Filtros Generales

document.getElementById("btn-filtrar").addEventListener("click", async () => {
  const linea_id = document.getElementById("linea-select").value;
  const turno_id = document.getElementById("turno-select").value;
  const dia = document.getElementById("dia-input").value;
  const year = document.getElementById("year-select-ml").value;

  const params = {};
  if (linea_id) params.linea_id = linea_id;
  if (turno_id) params.turno_id = turno_id;
  if (dia) params.dia_id = dia;
  if (year) params.year = year;

  await initChartTemperatura(params);
  await initChartPPM(params);
  await initChartHipoAci(params);
  await initChartKGS(params);

  await fetchAndUpdateKpis(params);
});

// Función para cargar los años disponibles
const loadAvailableYears = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/anio_disponible/");
    const data = await response.json();
    
    const yearSelect = document.getElementById("year-select-ml");
    // Mantener la opción "Todos los años"
    yearSelect.innerHTML = '<option value="">Todos los años</option>';
    
    // Agregar cada año disponible
    data.years.forEach(year => {
      const option = document.createElement('option');
      option.value = year;
      option.textContent = year;
      yearSelect.appendChild(option);
    });
  } catch(ex) {
    console.error("Error al cargar los años disponibles:", ex);
  }
};

document.addEventListener('DOMContentLoaded', loadAvailableYears);




// ---------------------------------------------------

// Función para redimensionar todos los gráficos
function resizeAllCharts() {
  for (const key in charts) {
    if (charts[key]) {
      charts[key].resize();
    }
  }
}

// ---------------------------------------------------

// Evento para redimensionar todos los charts, junto a la optm debounce
window.addEventListener('resize', debounce(resizeAllCharts, 250));

// ---------------------------------------------------
// Inicialización
window.addEventListener("load", async() =>{
  await initChartTemperatura();
  await initChartPPM();
  await initChartHipoAci();
  await initChartKGS();
  
  // inicialización kpis js/kpis.js
  await fetchAndUpdateKpis();
});


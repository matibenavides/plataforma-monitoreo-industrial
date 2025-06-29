// ---------------------------------------------------
// Función para actualizar los KPIs en las Tarjetas
// ---------------------------------------------------

const fetchAndUpdateKpis = async (params = {}) => {
    const query = new URLSearchParams(params);
    // Asegúrate que la URL coincida con la que definiste en urls.py
    const url = `/kpi_general/?${query.toString()}`; // Usar ruta relativa es mejor
  
    console.log("Fetching KPI data with params:", params); // Para depuración
  
    // Opcional: Mostrar algún indicador de carga en los KPIs
    document.getElementById("kpi-shbr230-total").textContent = 'Cargando...';
    document.getElementById("kpi-shbr430-total").textContent = 'Cargando...';
    document.getElementById("kpi-shbrpyr-total").textContent = 'Cargando...';
    document.getElementById("kpi-cera-total").textContent = 'Cargando...';
    document.getElementById("kpi-agua-total").textContent = 'Cargando...';
    document.getElementById("kpi-retards-total").textContent = 'Cargando...';
    document.getElementById("kpi-produccion-total").textContent = 'Cargando...';
    document.getElementById("kpi-bins-total").textContent = 'Cargando...';
  
  
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        const kpiData = await response.json();
        console.log("KPI data received:", kpiData); // Para depuración
  
        // --- Actualizar el HTML ---
        // Formatear números con separador de miles y añadir unidad
        const formatNumber = (num) => num.toLocaleString('es-CL') + ' L'; // Ajusta 'L' si la unidad es otra (ej: 'CC')
        const formatKilos = (num) => num.toLocaleString('es-Cl') + ' kg';
  
        // Actualizar cada KPI con los datos recibidos
        const elShbr230 = document.getElementById("kpi-shbr230-total");
        if (elShbr230) elShbr230.textContent = formatNumber(kpiData.shbr230_total || 0);
  
        const elShbrTebu = document.getElementById("kpi-shbr430-total");
        if (elShbrTebu) elShbrTebu.textContent = formatNumber(kpiData.shbr430_total || 0);
  
        const elShbrPyr = document.getElementById("kpi-shbrpyr-total");
        if (elShbrPyr) elShbrPyr.textContent = formatNumber(kpiData.shbrpyr_total || 0);
  
        const elCera = document.getElementById("kpi-cera-total");
        if (elCera) elCera.textContent = formatNumber(kpiData.total_cera || 0);

        const elAgua = document.getElementById("kpi-agua-total");
        if (elAgua) elAgua.textContent = formatNumber(kpiData.total_agua || 0);

        const elRetard = document.getElementById("kpi-retards-total");
        if (elRetard) elRetard.textContent = kpiData.total_retards;

        const laProduc = document.getElementById("kpi-produccion-total");
        if (laProduc) laProduc.textContent = formatKilos(kpiData.total_kilos || 0);

        const losBins = document.getElementById("kpi-bins-total");
        if (losBins) losBins.textContent = kpiData.total_bins;
  
  
    } catch (error) {
        console.error("Error al obtener o actualizar KPIs:", error);
        // Mostrar mensaje de error en los KPIs
        const errorMessage = 'Error';
        const elShbr230 = document.getElementById("kpi-shbr230-total");
        if (elShbr230) elShbr230.textContent = errorMessage;

         const elShbrTebu = document.getElementById("kpi-shbrtebu-total");
        if (elShbrTebu) elShbrTebu.textContent = errorMessage;

         const elShbrPyr = document.getElementById("kpi-shbrpyr-total");
        if (elShbrPyr) elShbrPyr.textContent = errorMessage;

        const elCera = document.getElementById("kpi-cera-total");
        if (elCera) elCera.textContent = errorMessage;

        const elAgua = document.getElementById("kpi-agua-total");
        if (elAgua) elAgua.textContent = errorMessage;

        const elRetard = document.getElementById("kpi-retards-total");
        if (elRetard) elRetard.textContent = errorMessage;

        const laProduc = document.getElementById("kpi-produccion-total");
        if (laProduc) laProduc.textContent = errorMessage;

        const losBins = document.getElementById("kpi-bins-total");
        if (losBins) losBins.textContent = errorMessage;


        alert(`No se pudieron cargar los datos de KPI: ${error.message}`);
    }
  };
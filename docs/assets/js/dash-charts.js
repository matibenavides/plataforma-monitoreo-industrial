
const charts = {};

function debounce(func, wait) {
  var timeout;
  return function() {
    var context = this, args = arguments;
    clearTimeout(timeout);
    timeout = setTimeout(function() { func.apply(context, args); }, wait);
  };
}

// ─── Colores del proyecto ───────────────────────────
const C = {
  primary:   '#0c0689',
  secondary: '#ac86e9',
  accent:    '#8a47f5',
  tertiary:  '#e0d0f8',
  contrast1: '#1a0050',
  contrast2: '#8a47f5',
  contrast3: '#ede8fb',
};

// ─── Chart Kilogramos por Especie (barras apiladas por mes) ──
function initChartKilos() {
  if (!charts.kgs) {
    charts.kgs = echarts.init(document.getElementById('chartKilos'));
  }

  const option = {
    legend: {
      data: ['Ciruela', 'Pera', 'Cereza', 'Nectarine'],
      textStyle: { color: C.primary }
    },
    toolbox: {
      feature: {
        magicType: { type: ['stack', 'line', 'bar'] },
        dataView: { readOnly: false },
        saveAsImage: { show: true }
      },
      top: 5,
      iconStyle: { borderColor: C.primary }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: C.tertiary,
      borderColor: C.secondary,
      textStyle: { color: C.primary }
    },
    xAxis: {
      data: ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'],
      axisLine: { lineStyle: { color: C.primary } },
      axisLabel: { color: C.primary }
    },
    yAxis: {
      type: 'value',
      name: 'Kg',
      axisLine: { lineStyle: { color: C.primary } },
      axisLabel: {
        color: C.primary,
        fontSize: 10,
        formatter: function(v) {
          if (v >= 1e6) return (v/1e6).toFixed(1)+'M';
          if (v >= 1e3) return (v/1e3).toFixed(1)+'K';
          return v;
        }
      }
    },
    grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true },
    series: [
      {
        name: 'Ciruela', type: 'bar', stack: 'total',
        itemStyle: { color: C.primary },
        emphasis: { focus: 'series', itemStyle: { shadowBlur: 10, shadowColor: C.accent } },
        data: [0,0,12400,38200,51000,43000,0,0,0,0,0,0]
      },
      {
        name: 'Pera', type: 'bar', stack: 'total',
        itemStyle: { color: C.secondary },
        emphasis: { focus: 'series', itemStyle: { shadowBlur: 10, shadowColor: C.accent } },
        data: [0,0,0,8500,22300,31000,28000,14000,0,0,0,0]
      },
      {
        name: 'Cereza', type: 'bar', stack: 'total',
        itemStyle: { color: C.accent },
        emphasis: { focus: 'series', itemStyle: { shadowBlur: 10, shadowColor: C.accent } },
        data: [0,0,0,0,0,0,0,0,0,18000,62000,47000]
      },
      {
        name: 'Nectarine', type: 'bar', stack: 'total',
        itemStyle: { color: C.tertiary },
        emphasis: { focus: 'series', itemStyle: { shadowBlur: 10, shadowColor: C.accent } },
        data: [0,0,0,5200,14000,19500,22000,11000,0,0,0,0]
      }
    ]
  };
  charts.kgs.setOption(option);
}

// ─── Chart Temperatura (líneas múltiples por hora) ──
function initChartTemperatura() {
  if (!charts.temperatura) {
    charts.temperatura = echarts.init(document.getElementById('chartTemperatura'));
  }

  // datos ficticios: [hora_decimal, temperatura]
  const pulpa_data     = [[6,4.2],[7,4.5],[8,5.1],[9,5.8],[10,6.2],[11,6.8],[12,7.1],[13,7.4],[14,7.8],[15,7.2],[16,6.9],[17,6.3],[18,5.8]];
  const vaciado_data   = [[6,8.1],[7,8.4],[8,9.0],[9,9.5],[10,10.1],[11,10.6],[12,11.0],[13,11.3],[14,11.7],[15,11.1],[16,10.8],[17,10.2],[18,9.7]];
  const camara_data    = [[6,2.1],[7,2.3],[8,2.8],[9,3.2],[10,3.7],[11,4.0],[12,4.4],[13,4.6],[14,5.0],[15,4.5],[16,4.2],[17,3.8],[18,3.3]];
  const fungicida_data = [[6,12.0],[7,12.4],[8,13.1],[9,13.8],[10,14.5],[11,15.0],[12,15.6],[13,15.9],[14,16.3],[15,15.8],[16,15.2],[17,14.7],[18,14.1]];

  const option = {
    legend: {
      orient: 'horizontal',
      data: ['T° Pulpa', 'T° Vaciado', 'T° Camara', 'T° Fungicida'],
      selected: { 'T° Pulpa': true, 'T° Vaciado': true, 'T° Camara': true, 'T° Fungicida': true },
      textStyle: { fontSize: 12 }
    },
    grid: { left: 40, right: 8, top: 32, bottom: 24 },
    dataZoom: [{ type: 'inside', xAxisIndex: 0, filterMode: 'none' }],
    xAxis: {
      type: 'value', min: 0, max: 24, interval: 3,
      axisLine: { lineStyle: { width: 1 } },
      axisLabel: {
        fontSize: 12,
        formatter: function(v) { return Math.floor(v) + ':00'; }
      }
    },
    yAxis: {
      type: 'value', min: -5, max: 20,
      axisLabel: { formatter: '{value} °C' },
      axisLine: { show: true, lineStyle: { width: 1 } },
      splitLine: { show: true, lineStyle: { type: 'dashed' } },
      axisTick: { show: true }
    },
    tooltip: {
      trigger: 'item',
      formatter: function(params) {
        const total = params.value[0];
        const hora = Math.floor(total);
        const min = Math.round((total - hora) * 60);
        const minStr = min < 10 ? '0' + min : min;
        return params.seriesName + '<br/>Hora: ' + hora + ':' + minStr + '<br/>Temperatura: ' + params.value[1] + '°C';
      }
    },
    series: [
      { name: 'T° Pulpa',    type: 'line', smooth: true, data: pulpa_data,     itemStyle: { color: '#059669' } },
      { name: 'T° Vaciado',  type: 'line', smooth: true, data: vaciado_data,   itemStyle: { color: '#34d399' } },
      { name: 'T° Camara',   type: 'line', smooth: true, data: camara_data,    itemStyle: { color: '#0d9488' } },
      { name: 'T° Fungicida',type: 'line', smooth: true, data: fungicida_data, itemStyle: { color: '#0e3a38' } }
    ]
  };
  charts.temperatura.setOption(option);
}

// ─── Chart PPM y pH (líneas múltiples por hora, doble eje Y) ──
function initChartPPM() {
  if (!charts.ppm) {
    charts.ppm = echarts.init(document.getElementById('chartPPM'));
  }

  const estanque_ppm   = [[6,95],[7.5,102],[9,118],[10.5,125],[12,131],[13.5,128],[15,122],[16.5,115],[18,108]];
  const estanque_ph    = [[6,6.8],[7.5,6.9],[9,7.0],[10.5,7.1],[12,7.2],[13.5,7.1],[15,7.0],[16.5,6.9],[18,6.8]];
  const corta_ppm      = [[6,88],[7.5,94],[9,105],[10.5,112],[12,118],[13.5,114],[15,108],[16.5,101],[18,95]];
  const corta_ph       = [[6,6.7],[7.5,6.8],[9,6.9],[10.5,7.0],[12,7.1],[13.5,7.0],[15,6.9],[16.5,6.8],[18,6.7]];
  const retorno_ppm    = [[6,75],[7.5,82],[9,91],[10.5,98],[12,104],[13.5,100],[15,94],[16.5,87],[18,81]];
  const retorno_ph     = [[6,6.5],[7.5,6.6],[9,6.8],[10.5,6.9],[12,7.0],[13.5,6.9],[15,6.8],[16.5,6.7],[18,6.6]];
  const fungi_ppm      = [[6,140],[8,155],[10,168],[12,175],[14,171],[16,162],[18,150]];
  const fungi_ph       = [[6,6.4],[8,6.5],[10,6.7],[12,6.8],[14,6.7],[16,6.6],[18,6.5]];

  const option = {
    legend: {
      data: ['Estanque', 'Corta Pedicelo', 'Retorno', 'Fungicida'],
      selected: { 'Estanque': true, 'Corta Pedicelo': true, 'Retorno': true, 'Fungicida': true },
      selectedMode: 'multiple',
      textStyle: { fontSize: 12 }
    },
    tooltip: {
      trigger: 'item',
      formatter: function(params) {
        const pointParams = Array.isArray(params) ? params[0] : params;
        if (!pointParams || !pointParams.value || pointParams.value.length < 2) return 'Sin datos';
        const t = pointParams.value[0];
        const hora = Math.floor(t);
        const min = Math.round((t - hora) * 60);
        const minStr = min < 10 ? '0' + min : min;
        const sid = pointParams.seriesId || '';
        const metrica = sid.includes('-ppm') ? 'PPM' : sid.includes('-ph') ? 'pH' : 'Valor';
        return pointParams.seriesName + '<br/>Hora: ' + hora + ':' + minStr + '<br/>' + metrica + ': ' + pointParams.value[1];
      }
    },
    grid: { left: 44, right: 44, top: 32, bottom: 24 },
    dataZoom: [{ type: 'inside', xAxisIndex: 0, filterMode: 'none' }],
    xAxis: {
      type: 'value', min: 0, max: 24, interval: 3,
      axisLine: { lineStyle: { width: 1 } },
      axisLabel: { fontSize: 12, formatter: function(v) { return Math.floor(v) + ':00'; } }
    },
    yAxis: [
      {
        type: 'value', name: 'PPM', nameTextStyle: { padding: [0,40,0,0] },
        min: 0, max: 300, position: 'left',
        axisLine: { show: true, lineStyle: { width: 1 } },
        splitLine: { show: true, lineStyle: { color: '#eee', type: 'solid' } },
        axisTick: { show: false }, axisLabel: { fontSize: 11 }
      },
      {
        type: 'value', name: 'pH', nameTextStyle: { padding: [0,0,0,30] },
        min: 0, max: 8, position: 'right',
        axisLine: { show: true, lineStyle: { width: 1 } },
        axisLabel: { formatter: '{value}.0', fontSize: 11 },
        splitLine: { show: false }, axisTick: { show: false }
      }
    ],
    series: [
      { id: 'estanque-ppm',  name: 'Estanque',       type: 'line', yAxisIndex: 0, smooth: true, symbol: 'emptyCircle', itemStyle: { color: '#16a34a' }, emphasis: { focus: 'series', scale: true }, blur: { itemStyle: { opacity: 0.1 } }, data: estanque_ppm },
      { id: 'estanque-ph',   name: 'Estanque',       type: 'line', yAxisIndex: 1, smooth: true, symbol: 'emptyCircle', itemStyle: { color: '#16a34a' }, emphasis: { focus: 'series', scale: true }, blur: { itemStyle: { opacity: 0.1 } }, data: estanque_ph },
      { id: 'corta-ppm',     name: 'Corta Pedicelo', type: 'line', yAxisIndex: 0, smooth: true, symbol: 'emptyCircle', itemStyle: { color: '#22c55e' }, emphasis: { focus: 'series', scale: true }, blur: { itemStyle: { opacity: 0.1 } }, data: corta_ppm },
      { id: 'corta-ph',      name: 'Corta Pedicelo', type: 'line', yAxisIndex: 1, smooth: true, symbol: 'emptyCircle', itemStyle: { color: '#22c55e' }, emphasis: { focus: 'series', scale: true }, blur: { itemStyle: { opacity: 0.1 } }, data: corta_ph },
      { id: 'retorno-ppm',   name: 'Retorno',        type: 'line', yAxisIndex: 0, smooth: true, symbol: 'emptyCircle', itemStyle: { color: '#4ade80' }, emphasis: { focus: 'series', scale: true }, blur: { itemStyle: { opacity: 0.1 } }, data: retorno_ppm },
      { id: 'retorno-ph',    name: 'Retorno',        type: 'line', yAxisIndex: 1, smooth: true, symbol: 'emptyCircle', itemStyle: { color: '#4ade80' }, emphasis: { focus: 'series', scale: true }, blur: { itemStyle: { opacity: 0.1 } }, data: retorno_ph },
      { id: 'fungicida-ppm', name: 'Fungicida',      type: 'line', yAxisIndex: 0, smooth: true, symbol: 'emptyCircle', itemStyle: { color: '#166534' }, emphasis: { focus: 'series', scale: true }, blur: { itemStyle: { opacity: 0.1 } }, data: fungi_ppm },
      { id: 'fungicida-ph',  name: 'Fungicida',      type: 'line', yAxisIndex: 1, smooth: true, symbol: 'emptyCircle', itemStyle: { color: '#166534' }, emphasis: { focus: 'series', scale: true }, blur: { itemStyle: { opacity: 0.1 } }, data: fungi_ph }
    ]
  };
  charts.ppm.setOption(option);
}

// ─── Chart Cloración: doble pie (ácido=interno, hipoclorito=anillo) ──
function initChartCloroAcido() {
  if (!charts.hipoAci) {
    charts.hipoAci = echarts.init(document.getElementById('chartCloroAcido'));
  }

  const option = {
    tooltip: { trigger: 'item', formatter: '{a} <br/>{b}: {c} ({d}%)' },
    legend: {
      orient: 'horizontal',
      data: ['Linea 11', 'Linea 10', 'Linea 5']
    },
    series: [
      {
        name: 'Ácido (Lts)',
        type: 'pie',
        selectedMode: 'single',
        radius: [0, '30%'],
        label: { show: true, position: 'inner', formatter: '{b}' },
        labelLine: { show: false },
        data: [
          { value: 142, name: 'Linea 11', itemStyle: { color: C.contrast1 } },
          { value: 98,  name: 'Linea 10', itemStyle: { color: C.contrast2 } },
          { value: 67,  name: 'Linea 5',  itemStyle: { color: C.contrast3 } }
        ]
      },
      {
        name: 'Hipoclorito (Lts)',
        type: 'pie',
        radius: ['45%', '60%'],
        label: { show: false },
        labelLine: { show: false },
        data: [
          { value: 620, name: 'Linea 11', itemStyle: { color: '#6c47d4' } },
          { value: 410, name: 'Linea 10', itemStyle: { color: '#b39ddb' } },
          { value: 285, name: 'Linea 5',  itemStyle: { color: '#d5caee' } }
        ]
      }
    ]
  };
  charts.hipoAci.setOption(option);
}

// ─── Resize ──────────────────────────────────────────
function resizeAllCharts() {
  for (const key in charts) {
    if (charts[key]) charts[key].resize();
  }
}
window.addEventListener('resize', debounce(resizeAllCharts, 250));

// ─── Init ─────────────────────────────────────────────
window.addEventListener('load', function() {
  initChartKilos();
  initChartTemperatura();
  initChartPPM();
  initChartCloroAcido();
});

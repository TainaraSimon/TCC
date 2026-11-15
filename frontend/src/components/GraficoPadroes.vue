<template>
  <div ref="elemento" class="grafico" />
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import { CATEGORIAS, CORES_CATEGORIAS } from '@/utils/emocoes'

const props = defineProps({
  rotulos: { type: Array, required: true }, // nomes dos períodos no eixo X
  periodos: { type: Array, required: true } // períodos retornados pela rota /padroes
})

const elemento = ref(null)
let grafico = null

// Gráfico de barras: uma barra por emoção em cada período
function desenhar () {
  grafico.setOption({
    tooltip: { trigger: 'axis' },
    legend: { type: 'scroll', bottom: 0 },
    textStyle: { fontFamily: 'Nunito, sans-serif' },
    grid: { left: 40, right: 16, top: 16, bottom: 48 },
    xAxis: { type: 'category', data: props.rotulos },
    yAxis: { type: 'value', minInterval: 1 },
    series: CATEGORIAS.map((categoria) => ({
      name: categoria,
      type: 'bar',
      color: CORES_CATEGORIAS[categoria],
      data: props.periodos.map((periodo) => periodo.frequencia[categoria])
    }))
  })
}

function redimensionar () {
  grafico.resize()
}

onMounted(() => {
  grafico = echarts.init(elemento.value)
  desenhar()
  window.addEventListener('resize', redimensionar)
})

// Redesenha quando os dados mudam (ex.: troca de semanal para mensal)
watch(() => props.periodos, desenhar)

onBeforeUnmount(() => {
  window.removeEventListener('resize', redimensionar)
  grafico.dispose()
})
</script>

<style scoped>
.grafico {
  width: 100%;
  height: 320px;
}
</style>
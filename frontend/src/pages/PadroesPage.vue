<template>
  <q-page padding>
    <div class="conteudo">
        <div class="row items-center justify-between q-mb-md">
        <div class="titulo-pagina col-12 col-sm q-mb-sm">Padrões emocionais</div>
        <q-btn-toggle
          v-model="periodo"
          :options="opcoesPeriodo"
          toggle-color="primary"
          no-caps
          @update:model-value="carregar"
        />
      </div>

      <div v-if="carregando && !padroes" class="text-center q-pa-lg">
        <q-spinner size="lg" color="primary" />
      </div>

      <div v-else-if="padroes && padroes.total_analisados === 0" class="text-grey-7">
        Ainda não há registros analisados.
        <router-link to="/">Faça um registro</router-link> para começar a acompanhar seus padrões.
      </div>

      <template v-else-if="padroes">
        <!-- Frequência de cada categoria (RF10/RF11) -->
        <q-card class="q-mb-md">
          <q-card-section>
            <div class="text-subtitle1">Frequência de cada emoção</div>
            <div class="text-caption text-grey-7">
              {{ padroes.total_analisados }} registros analisados nos últimos
              {{ padroes.periodos.length }} períodos com registros
            </div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            <div v-for="categoria in CATEGORIAS" :key="categoria" class="q-mb-sm">
              <div class="row justify-between text-body2">
                <span>{{ categoria }}</span>
                <span>{{ padroes.frequencia_geral[categoria] }}</span>
              </div>
              <div class="barra">
                <div
                  class="barra-preenchida"
                  :style="{
                    width: `${(padroes.frequencia_geral[categoria] / maiorFrequencia) * 100}%`,
                    backgroundColor: CORES_CATEGORIAS[categoria]
                  }"
                />
              </div>
            </div>

            <div v-if="padroes.mais_frequente" class="q-mt-md">
              A emoção que mais apareceu nos seus registros foi <b>{{ padroes.mais_frequente }}</b>.
            </div>
          </q-card-section>
        </q-card>

        <!-- Emoções e contextos: em que área da vida cada emoção costuma aparecer -->
        <q-card class="q-mb-md">
          <q-card-section>
            <div class="text-subtitle1">Emoções e contextos</div>
            <div class="text-caption text-grey-7">
              Situações da sua vida em que a mesma emoção apareceu em mais de um registro
            </div>
          </q-card-section>

          <q-list v-if="padroes.contextos.length" separator>
            <q-item v-for="item in padroes.contextos" :key="`${item.categoria}-${item.contexto}`">
              <q-item-section avatar>
                <q-avatar
                  :icon="CONTEXTOS[item.contexto].icone"
                  :style="{ backgroundColor: CORES_CATEGORIAS[item.categoria] }"
                  text-color="white"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label><b>{{ item.categoria }}</b> {{ CONTEXTOS[item.contexto].frase }}</q-item-label>
              </q-item-section>
              <q-item-section side>{{ item.total }} registros</q-item-section>
            </q-item>
          </q-list>

          <q-card-section v-else class="q-pt-none text-grey-7">
            Ainda não há padrões de contexto. Eles aparecem quando a mesma emoção surge em pelo menos
            2 registros sobre o mesmo assunto (por exemplo, ansiedade em 2 registros sobre trabalho).
          </q-card-section>
        </q-card>

        <!-- Gráfico por período -->
        <q-card class="q-mb-md">
          <q-card-section>
            <div class="text-subtitle1">Frequência por {{ periodo === 'semana' ? 'semana' : 'mês' }}</div>
            <div class="text-caption text-grey-7">Quantidade de registros em que cada emoção apareceu</div>
          </q-card-section>
          <q-card-section class="q-pt-none">
            <GraficoPadroes :rotulos="rotulos" :periodos="padroes.periodos" />
          </q-card-section>
        </q-card>

        <!-- Variação em relação ao período anterior -->
        <q-card class="q-mb-md">
          <q-card-section>
            <div class="text-subtitle1">Variação</div>
            <div class="text-caption text-grey-7">{{ textoVariacao }}</div>
          </q-card-section>
          <q-list separator>
            <q-item v-for="item in padroes.variacao" :key="item.categoria">
              <q-item-section avatar>
                <q-icon :name="iconeVariacao(item.diferenca)" :style="{ color: CORES_CATEGORIAS[item.categoria] }" />
              </q-item-section>
              <q-item-section>{{ item.categoria }}</q-item-section>
              <q-item-section side>
                {{ item.anterior }} → {{ item.atual }} ({{ formatarDiferenca(item.diferenca) }})
              </q-item-section>
            </q-item>
          </q-list>
        </q-card>

        <div class="text-caption text-grey-7">
          Os padrões são calculados a partir das análises automáticas dos seus registros e servem como
          apoio ao autoconhecimento. Eles não representam diagnóstico.
        </div>
      </template>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { api, mensagemDeErro } from '@/boot/axios'
import { CATEGORIAS, CORES_CATEGORIAS, CONTEXTOS } from '@/utils/emocoes'
import GraficoPadroes from '@/components/GraficoPadroes.vue'

const $q = useQuasar()

const opcoesPeriodo = [
  { label: 'Semanal', value: 'semana' },
  { label: 'Mensal', value: 'mes' }
]

const periodo = ref('semana')
const padroes = ref(null)
const carregando = ref(false)

// Nome de cada período no gráfico: semana "dd/mm" (segunda-feira) ou mês "mm/aaaa"
function rotuloDoPeriodo (inicio) {
  const [ano, mes, dia] = inicio.split('-')
  return periodo.value === 'semana' ? `${dia}/${mes}` : `${mes}/${ano}`
}

const rotulos = computed(() => (padroes.value ? padroes.value.periodos.map((p) => rotuloDoPeriodo(p.inicio)) : []))

// Usado para calcular o tamanho das barras (a maior frequência ocupa 100%)
const maiorFrequencia = computed(() => Math.max(1, ...Object.values(padroes.value.frequencia_geral)))

const textoVariacao = computed(() => {
  const ultimo = padroes.value.periodos[padroes.value.periodos.length - 1]
  const rotulo = rotuloDoPeriodo(ultimo.inicio)
  return periodo.value === 'semana'
    ? `Semana de ${rotulo} comparada com a semana anterior`
    : `Mês ${rotulo} comparado com o mês anterior`
})

function iconeVariacao (diferenca) {
  if (diferenca > 0) return 'trending_up'
  if (diferenca < 0) return 'trending_down'
  return 'trending_flat'
}

function formatarDiferenca (diferenca) {
  return diferenca > 0 ? `+${diferenca}` : `${diferenca}`
}

// RF10/RF11: busca os padrões calculados pelo back-end
async function carregar () {
  carregando.value = true
  try {
    const resposta = await api.get('/padroes', { params: { periodo: periodo.value, quantidade: 6 } })
    padroes.value = resposta.data
  } catch (erro) {
    $q.notify({ type: 'negative', message: mensagemDeErro(erro) })
  } finally {
    carregando.value = false
  }
}

onMounted(carregar)
</script>

<style scoped>
.conteudo {
  max-width: 900px;
  margin: 0 auto;
}

.barra {
  height: 10px;
  border-radius: 5px;
  background-color: #EEF1EF;
  overflow: hidden;
}

.barra-preenchida {
  height: 100%;
  border-radius: 5px;
}
</style>
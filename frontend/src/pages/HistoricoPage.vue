<template>
  <q-page padding>
    <div class="conteudo">
      <div class="row items-center q-mb-md">
        <div class="titulo-pagina col">Histórico de registros</div>
        <q-btn flat round icon="refresh" :loading="carregando" @click="carregar">
          <q-tooltip>Atualizar</q-tooltip>
        </q-btn>
      </div>

      <div v-if="!carregando && registros.length === 0" class="text-grey-7">
        Você ainda não tem registros. <router-link to="/">Faça o primeiro registro</router-link>.
      </div>

      <q-card v-for="registro in registros" :key="registro.id_registro" class="q-mb-md">
        <q-card-section class="row items-center q-pb-none">
          <q-icon :name="registro.tipo === 'voz' ? 'mic' : 'edit'" color="grey-7" class="q-mr-sm" />
          <div class="col text-caption text-grey-8">
            {{ formatarDataHora(registro.data_hora) }} ·
            {{ registro.tipo === 'voz' ? 'Voz (transcrito)' : 'Texto' }}
          </div>
          <q-btn flat round dense icon="edit" @click="abrirEdicao(registro)">
            <q-tooltip>Editar</q-tooltip>
          </q-btn>
          <q-btn flat round dense icon="delete" color="negative" @click="excluir(registro)">
            <q-tooltip>Excluir</q-tooltip>
          </q-btn>
        </q-card-section>

        <q-card-section>
          <div class="texto-registro">{{ registro.conteudo_texto }}</div>
        </q-card-section>

        <q-separator />

        <q-card-section>
          <ResultadoAnalise :analise="registro.analise" />
          <q-btn
            v-if="!registro.analise || !registro.analise.contexto"
            class="q-mt-sm"
            outline
            color="primary"
            icon="psychology"
            label="Analisar novamente"
            :loading="analisando === registro.id_registro"
            @click="reanalisar(registro)"
          />
        </q-card-section>
      </q-card>
    </div>

    <!-- Edição do registro (RF06) -->
    <q-dialog v-model="edicao.aberta" persistent :maximized="$q.screen.lt.sm">
      <q-card class="cartao-edicao">
        <q-card-section class="text-h6">Editar registro</q-card-section>
        <q-card-section class="q-pt-none">
          <q-input v-model="edicao.texto" type="textarea" outlined autogrow counter maxlength="10000" />
          <div class="text-caption text-grey-7 q-mt-sm">
            Ao salvar, o registro será analisado novamente.
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" :disable="edicao.salvando" v-close-popup />
          <q-btn
            color="primary"
            label="Salvar"
            :loading="edicao.salvando"
            :disable="!edicao.texto.trim()"
            @click="salvarEdicao"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { api, mensagemDeErro } from '@/boot/axios'
import { formatarDataHora } from '@/utils/formatacao'
import ResultadoAnalise from '@/components/ResultadoAnalise.vue'

const $q = useQuasar()

const registros = ref([])
const carregando = ref(false)
const analisando = ref(null) // id do registro que está sendo analisado
const edicao = reactive({ aberta: false, id: null, texto: '', salvando: false })

// RF08: consulta o histórico (do mais recente para o mais antigo)
async function carregar () {
  carregando.value = true
  try {
    const resposta = await api.get('/registros')
    registros.value = resposta.data
  } catch (erro) {
    $q.notify({ type: 'negative', message: mensagemDeErro(erro) })
  } finally {
    carregando.value = false
  }
}

// Troca um registro da lista pela versão atualizada vinda do back-end
function atualizarNaLista (registroAtualizado) {
  const posicao = registros.value.findIndex((r) => r.id_registro === registroAtualizado.id_registro)
  if (posicao !== -1) {
    registros.value[posicao] = registroAtualizado
  }
}

function abrirEdicao (registro) {
  edicao.id = registro.id_registro
  edicao.texto = registro.conteudo_texto
  edicao.aberta = true
}

// RF06: edita o registro; o back-end refaz a análise
async function salvarEdicao () {
  edicao.salvando = true
  try {
    const resposta = await api.put(`/registros/${edicao.id}`, { conteudo_texto: edicao.texto })
    atualizarNaLista(resposta.data)
    edicao.aberta = false
    if (resposta.data.aviso) {
      $q.notify({ type: 'warning', message: resposta.data.aviso })
    } else {
      $q.notify({ type: 'positive', message: 'Registro atualizado e analisado novamente.' })
    }
  } catch (erro) {
    $q.notify({ type: 'negative', message: mensagemDeErro(erro) })
  } finally {
    edicao.salvando = false
  }
}

// RF07: exclui o registro (RN08: a análise é excluída junto)
function excluir (registro) {
  $q.dialog({
    title: 'Excluir registro',
    message: 'Tem certeza? O registro e a sua análise serão excluídos e não poderão ser recuperados.',
    cancel: { label: 'Cancelar', flat: true },
    ok: { label: 'Excluir', color: 'negative' },
    persistent: true
  }).onOk(async () => {
    try {
      await api.delete(`/registros/${registro.id_registro}`)
      registros.value = registros.value.filter((r) => r.id_registro !== registro.id_registro)
      $q.notify({ type: 'positive', message: 'Registro excluído.' })
    } catch (erro) {
      $q.notify({ type: 'negative', message: mensagemDeErro(erro) })
    }
  })
}

// Nova tentativa de análise quando ela falhou (seção 7.4 do artigo)
async function reanalisar (registro) {
  analisando.value = registro.id_registro
  try {
    const resposta = await api.post(`/registros/${registro.id_registro}/analisar`)
    atualizarNaLista(resposta.data)
    $q.notify({ type: 'positive', message: 'Análise concluída.' })
  } catch (erro) {
    $q.notify({ type: 'negative', message: mensagemDeErro(erro) })
  } finally {
    analisando.value = null
  }
}

onMounted(carregar)
</script>

<style scoped>
.conteudo {
  max-width: 820px;
  margin: 0 auto;
}

.texto-registro {
  white-space: pre-line;
}

.cartao-edicao {
  width: 100%;
  max-width: 600px;
}
</style>
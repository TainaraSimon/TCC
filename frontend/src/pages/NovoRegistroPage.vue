<template>
  <q-page padding>
    <div class="conteudo">
      <div class="q-mb-lg">
        <div class="titulo-pagina">Como você está se sentindo hoje?</div>
        <div class="subtitulo-pagina">Escreva ou fale livremente. Este é um espaço só seu.</div>
    </div>

      <q-card>
        <q-tabs v-model="aba" align="justify" active-color="primary" indicator-color="primary">
          <q-tab name="texto" icon="edit" label="Texto" />
          <q-tab name="voz" icon="mic" label="Voz" />
        </q-tabs>
        <q-separator />

        <q-tab-panels v-model="aba" animated>
          <!-- Registro por texto (RF03) -->
          <q-tab-panel name="texto">
            <q-input
              v-model="texto"
              type="textarea"
              outlined
              autogrow
              counter
              maxlength="10000"
              label="Escreva sobre o seu dia e como você se sentiu"
              input-style="min-height: 120px"
            />
            <q-btn
              class="full-width q-mt-md"
              color="primary"
              label="Salvar registro"
              :loading="salvando"
              :disable="!texto.trim()"
              @click="salvar('texto', texto)"
            />
          </q-tab-panel>

          <!-- Registro por voz (RF04 e RF05) -->
          <q-tab-panel name="voz">
            <div v-if="transcricao === null">
              <GravadorAudio :desabilitado="transcrevendo" @gravado="transcrever" />
              <div v-if="transcrevendo" class="text-center q-mt-sm">
                <q-spinner color="primary" size="sm" class="q-mr-sm" />
                Transcrevendo o áudio...
              </div>
              <div class="text-caption text-grey-7 text-center q-mt-md">
                O áudio é usado somente para gerar o texto do registro e não é armazenado.
                O tom de voz não é analisado.
              </div>
            </div>

            <!-- Conferência da transcrição antes da análise (seção 7.4 do artigo) -->
            <div v-else>
              <div class="text-subtitle2 q-mb-sm">
                Confira o texto transcrito e corrija, se necessário:
              </div>
              <q-input v-model="transcricao" type="textarea" outlined autogrow counter maxlength="10000" />
              <div class="row items-center q-mt-md">
                <q-btn flat icon="replay" label="Gravar novamente" :disable="salvando" @click="transcricao = null" />
                <q-space />
                <q-btn
                  color="primary"
                  label="Salvar registro"
                  :loading="salvando"
                  :disable="!transcricao.trim()"
                  @click="salvar('voz', transcricao)"
                />
              </div>
            </div>
          </q-tab-panel>
        </q-tab-panels>
      </q-card>

      <!-- Resultado do registro salvo (RF11) -->
      <q-card v-if="ultimoRegistro" class="q-mt-lg">
        <q-card-section>
          <div class="text-h6">Registro salvo</div>
          <div class="text-caption text-grey-7">{{ formatarDataHora(ultimoRegistro.data_hora) }}</div>
        </q-card-section>

        <q-card-section v-if="ultimoRegistro.aviso" class="q-pt-none">
          <q-banner rounded class="bg-orange-1 text-orange-10">{{ ultimoRegistro.aviso }}</q-banner>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <ResultadoAnalise :analise="ultimoRegistro.analise" />
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useQuasar } from 'quasar'
import { api, mensagemDeErro } from '@/boot/axios'
import { formatarDataHora } from '@/utils/formatacao'
import GravadorAudio from '@/components/GravadorAudio.vue'
import ResultadoAnalise from '@/components/ResultadoAnalise.vue'

const $q = useQuasar()

const aba = ref('texto')
const texto = ref('')
const transcricao = ref(null) // null = ainda não há áudio transcrito
const transcrevendo = ref(false)
const salvando = ref(false)
const ultimoRegistro = ref(null)

// Cada navegador grava em um formato; o back-end precisa da extensão correta
function extensaoDoAudio (tipo) {
  if (tipo.includes('mp4')) return 'mp4'
  if (tipo.includes('ogg')) return 'ogg'
  return 'webm'
}

// RF05: envia o áudio para transcrição; o texto volta para o usuário conferir
async function transcrever (audio) {
  transcrevendo.value = true
  try {
    const formulario = new FormData()
    formulario.append('audio', audio, `gravacao.${extensaoDoAudio(audio.type)}`)
    const resposta = await api.post('/registros/transcrever', formulario)
    transcricao.value = resposta.data.texto
  } catch (erro) {
    $q.notify({ type: 'negative', message: mensagemDeErro(erro) })
  } finally {
    transcrevendo.value = false
  }
}

// RF03/RF04: salva o registro; o back-end faz a análise do texto (RF09)
async function salvar (tipo, conteudo) {
  salvando.value = true
  try {
    const resposta = await api.post('/registros', { tipo, conteudo_texto: conteudo })
    ultimoRegistro.value = resposta.data
    texto.value = ''
    transcricao.value = null
    $q.notify({ type: 'positive', message: 'Registro salvo!' })
  } catch (erro) {
    $q.notify({ type: 'negative', message: mensagemDeErro(erro) })
  } finally {
    salvando.value = false
  }
}
</script>

<style scoped>
.conteudo {
  max-width: 720px;
  margin: 0 auto;
}
</style>
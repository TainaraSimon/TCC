<template>
  <div class="column items-center q-py-lg">
    <div class="area-botao" :class="{ gravando }">
      <q-btn
        round
        unelevated
        size="xl"
        :color="gravando ? 'negative' : 'primary'"
        :icon="gravando ? 'stop' : 'mic'"
        :disable="desabilitado"
        :aria-label="gravando ? 'Parar gravação' : 'Iniciar gravação'"
        @click="gravando ? parar() : iniciar()"
      />
    </div>
    <div class="text-subtitle1 q-mt-md">
      {{ gravando ? `Gravando... ${tempo}` : 'Toque no microfone e fale com calma' }}
    </div>
    <div v-if="gravando" class="text-caption text-grey-7">Toque novamente para encerrar</div>
  </div>
</template>

<script setup>
import { ref, computed, onBeforeUnmount } from 'vue'
import { useQuasar } from 'quasar'

defineProps({ desabilitado: Boolean })
const emit = defineEmits(['gravado'])
const $q = useQuasar()

const LIMITE_SEGUNDOS = 300 // 5 minutos por gravação

const gravando = ref(false)
const segundos = ref(0)

let gravador = null
let partes = []
let cronometro = null

const tempo = computed(() => {
  const minutos = String(Math.floor(segundos.value / 60)).padStart(2, '0')
  const resto = String(segundos.value % 60).padStart(2, '0')
  return `${minutos}:${resto}`
})

async function iniciar () {
  // API MediaRecorder: recurso nativo do navegador para gravar áudio (RF04)
  if (!navigator.mediaDevices || typeof MediaRecorder === 'undefined') {
    $q.notify({ type: 'negative', message: 'Seu navegador não permite gravar áudio.' })
    return
  }

  let microfone
  try {
    microfone = await navigator.mediaDevices.getUserMedia({ audio: true })
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Não foi possível acessar o microfone. Verifique a permissão do navegador.'
    })
    return
  }

  partes = []
  gravador = new MediaRecorder(microfone)

  gravador.ondataavailable = (evento) => {
    if (evento.data.size > 0) {
      partes.push(evento.data)
    }
  }

  gravador.onstop = () => {
    microfone.getTracks().forEach((faixa) => faixa.stop()) // desliga o microfone
    const audio = new Blob(partes, { type: gravador.mimeType })
    emit('gravado', audio)
  }

  gravador.start()
  gravando.value = true
  segundos.value = 0
  cronometro = setInterval(() => {
    segundos.value++
    if (segundos.value >= LIMITE_SEGUNDOS) {
      parar()
    }
  }, 1000)
}

function parar () {
  clearInterval(cronometro)
  gravando.value = false
  if (gravador && gravador.state !== 'inactive') {
    gravador.stop()
  }
}

// Se o usuário sair da tela gravando, a gravação é interrompida
onBeforeUnmount(parar)
</script>


<style lang="scss" scoped>
.area-botao {
  padding: 12px;
  border-radius: 50%;
  background-color: $salvia-clara;
}

// Enquanto grava, um círculo suave "pulsa" em volta do botão
.area-botao.gravando {
  background-color: $pessego-claro;
  animation: pulsar 1.6s ease-in-out infinite;
}

@keyframes pulsar {
  0%, 100% { box-shadow: 0 0 0 0 rgba(201, 106, 100, 0.35); }
  50% { box-shadow: 0 0 0 14px rgba(201, 106, 100, 0); }
}
</style>
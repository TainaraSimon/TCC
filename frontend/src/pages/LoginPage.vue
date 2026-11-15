<template>
  <PainelAcesso titulo="Que bom ter você aqui" subtitulo="Entre para continuar seus registros">
    <q-card-section>
      <q-form class="q-gutter-md" @submit="entrar">
        <q-input
          v-model="email"
          type="email"
          label="E-mail"
          outlined
          :rules="[(v) => !!v || 'Informe seu e-mail']"
        >
          <template #prepend><q-icon name="mail_outline" /></template>
        </q-input>

        <q-input
          v-model="senha"
          :type="mostrarSenha ? 'text' : 'password'"
          label="Senha"
          outlined
          :rules="[(v) => !!v || 'Informe sua senha']"
        >
          <template #prepend><q-icon name="lock_outline" /></template>
          <template #append>
            <q-icon
              :name="mostrarSenha ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="mostrarSenha = !mostrarSenha"
            />
          </template>
        </q-input>

        <q-btn
          type="submit"
          label="Entrar"
          color="primary"
          size="lg"
          unelevated
          no-caps
          class="full-width"
          :loading="carregando"
        />
      </q-form>
    </q-card-section>

    <q-card-section class="text-center">
      Ainda não tem conta? <router-link to="/cadastro">Crie sua conta</router-link>
    </q-card-section>
  </PainelAcesso>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAutenticacaoStore } from '@/stores/autenticacao'
import { mensagemDeErro } from '@/boot/axios'
import PainelAcesso from '@/components/PainelAcesso.vue'

const $q = useQuasar()
const router = useRouter()
const autenticacao = useAutenticacaoStore()

const email = ref('')
const senha = ref('')
const mostrarSenha = ref(false)
const carregando = ref(false)

async function entrar () {
  carregando.value = true
  try {
    await autenticacao.entrar(email.value, senha.value)
    router.push('/')
  } catch (erro) {
    $q.notify({ type: 'negative', message: mensagemDeErro(erro) })
  } finally {
    carregando.value = false
  }
}
</script>
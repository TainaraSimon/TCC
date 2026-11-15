<template>
  <PainelAcesso titulo="Crie sua conta" subtitulo="Comece sua jornada de autoconhecimento">
    <q-card-section>
      <q-form class="q-gutter-md" @submit="cadastrar">
        <q-input
          v-model="nome"
          label="Nome"
          outlined
          :rules="[(v) => (v && v.trim().length >= 2) || 'Informe seu nome']"
        >
          <template #prepend><q-icon name="person_outline" /></template>
        </q-input>

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
          :rules="[(v) => (v && v.length >= 8) || 'A senha deve ter no mínimo 8 caracteres']"
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

        <q-input
          v-model="confirmacao"
          :type="mostrarSenha ? 'text' : 'password'"
          label="Confirmar senha"
          outlined
          :rules="[(v) => v === senha || 'As senhas não conferem']"
        >
          <template #prepend><q-icon name="lock_outline" /></template>
        </q-input>

        <div class="aviso-privacidade row no-wrap q-gutter-sm">
          <q-icon name="verified_user" size="sm" color="secondary" />
          <div>
            Seus relatos são dados pessoais sensíveis. Para a transcrição e a análise, apenas o áudio e o
            texto do relato são enviados ao serviço de IA (Groq Cloud), sem seus dados de identificação.
            Você pode editar ou excluir seus registros a qualquer momento.
          </div>
        </div>

        <q-btn
          type="submit"
          label="Criar conta"
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
      Já tem conta? <router-link to="/login">Entrar</router-link>
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

const nome = ref('')
const email = ref('')
const senha = ref('')
const confirmacao = ref('')
const mostrarSenha = ref(false)
const carregando = ref(false)

async function cadastrar () {
  carregando.value = true
  try {
    await autenticacao.cadastrar(nome.value, email.value, senha.value)
    await autenticacao.entrar(email.value, senha.value)
    $q.notify({ type: 'positive', message: 'Conta criada. Seja bem-vinda(o)!' })
    router.push('/')
  } catch (erro) {
    $q.notify({ type: 'negative', message: mensagemDeErro(erro) })
  } finally {
    carregando.value = false
  }
}
</script>

<style lang="scss" scoped>
.aviso-privacidade {
  padding: 12px;
  border-radius: 12px;
  background-color: $lavanda-clara;
  font-size: 0.85rem;
  color: $texto;
}
</style>
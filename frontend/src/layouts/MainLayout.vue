<template>
  <!-- "fff" minúsculo: o rodapé fica no fim da página, sem ocupar espaço fixo na tela do celular -->
  <q-layout view="hHh lpR fff">
    <q-header bordered class="bg-white text-grey-9">
      <q-toolbar>
        <q-btn flat round dense icon="menu" aria-label="Abrir menu" class="lt-md q-mr-sm" @click="menuAberto = !menuAberto" />

        <router-link to="/" class="marca">
          <LogoIntrospect :tamanho="34" />
          <span class="marca-nome">Introspect</span>
        </router-link>

        <q-space />

        <span v-if="primeiroNome" class="q-mr-md gt-xs saudacao">Olá, {{ primeiroNome }}</span>
        <q-btn flat dense no-caps color="primary" icon="logout" aria-label="Sair" @click="sair">
          <span class="gt-xs q-ml-xs">Sair</span>
        </q-btn>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="menuAberto" show-if-above bordered :width="260">
      <q-list padding class="q-px-sm">
        <q-item
          v-for="link in links"
          :key="link.rota"
          :to="link.rota"
          clickable
          v-ripple
          exact
          class="item-menu"
          active-class="item-ativo"
          @click="aoNavegar"
        >
          <q-item-section avatar>
            <q-icon :name="link.icone" />
          </q-item-section>
          <q-item-section>{{ link.titulo }}</q-item-section>
        </q-item>
      </q-list>

      <div class="frase-menu q-ma-md">
        <q-icon name="spa" size="sm" color="secondary" />
        <div>Reserve um momento para você. Cada registro é um passo no seu autoconhecimento.</div>
      </div>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer class="bg-transparent text-grey-8 text-caption text-center q-pa-md">
      Ferramenta de apoio ao autoconhecimento. Não realiza diagnóstico e não substitui profissionais de saúde.
      Se precisar de ajuda, ligue <b>188</b> (CVV).
    </q-footer>
  </q-layout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAutenticacaoStore } from '@/stores/autenticacao'
import LogoIntrospect from '@/components/LogoIntrospect.vue'

const $q = useQuasar()
const autenticacao = useAutenticacaoStore()
const router = useRouter()
const menuAberto = ref(false)

const links = [
  { titulo: 'Novo registro', icone: 'edit_note', rota: '/' },
  { titulo: 'Histórico', icone: 'history', rota: '/historico' },
  { titulo: 'Padrões emocionais', icone: 'insights', rota: '/padroes' },
]

const primeiroNome = computed(() => (autenticacao.usuario ? autenticacao.usuario.nome.split(' ')[0] : ''))

onMounted(async () => {
  // Ao recarregar a página, busca novamente os dados do usuário logado
  if (!autenticacao.usuario) {
    try {
      await autenticacao.carregarUsuario()
    } catch {
      // o interceptor já trata o caso de sessão expirada
    }
  }
})

// No celular o menu abre por cima da tela, então ele fecha depois de escolher uma opção
function aoNavegar () {
  if ($q.screen.lt.md) {
    menuAberto.value = false
  }
}

function sair () {
  autenticacao.sair()
  router.push('/login')
}
</script>

<style lang="scss" scoped>
.marca {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.marca-nome {
  font-size: 1.35rem;
  font-weight: 700;
  color: $primary;
}

.saudacao {
  color: $texto-suave;
}

.item-menu {
  border-radius: 12px;
  margin-bottom: 4px;
  color: $texto;
}

.item-ativo {
  background-color: $salvia-clara;
  color: $primary;
  font-weight: 700;
}

.frase-menu {
  display: flex;
  gap: 10px;
  padding: 14px;
  border-radius: 14px;
  background-color: $lavanda-clara;
  font-size: 0.85rem;
  color: $texto;
}
</style>
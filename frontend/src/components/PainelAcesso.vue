<template>
  <q-layout>
    <q-page-container>
      <q-page class="row">
        <!-- Boas-vindas: no celular aparece só a logo, o nome e o slogan -->
        <div class="col-12 col-md-6 boas-vindas column flex-center q-pa-lg text-center">
          <LogoIntrospect :tamanho="$q.screen.gt.sm ? 120 : 72" />
          <div class="nome-site q-mt-md">Introspect</div>
          <div class="slogan">Um espaço seguro para olhar para dentro</div>
          <p class="gt-sm texto-boas-vindas q-mt-lg">
            Registre como você se sente, por texto ou por voz, e acompanhe seus padrões emocionais ao longo
            do tempo.
          </p>
          <div class="gt-sm creditos">Desenvolvido por Tainara Paula Simon</div>
        </div>

        <!-- Formulário (conteúdo vem da página de login ou de cadastro) -->
        <div class="col-12 col-md-6 flex flex-center q-pa-md">
          <q-card class="cartao-acesso">
            <q-card-section>
              <div class="text-h5 text-weight-bold">{{ titulo }}</div>
              <div class="subtitulo-pagina">{{ subtitulo }}</div>
            </q-card-section>
            <slot />
          </q-card>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import LogoIntrospect from '@/components/LogoIntrospect.vue'

defineProps({
  titulo: { type: String, required: true },
  subtitulo: { type: String, default: '' }
})
</script>

<style lang="scss" scoped>
.boas-vindas {
  background: linear-gradient(160deg, $salvia-clara, $lavanda-clara);
}

.nome-site {
  font-size: 2rem;
  font-weight: 700;
  color: $primary;
}

.slogan {
  color: $texto-suave;
}

.texto-boas-vindas {
  max-width: 360px;
  font-size: 1.05rem;
  color: $texto;
}

.creditos {
  margin-top: 24px;
  font-size: 0.8rem;
  color: $texto-suave;
}

.cartao-acesso {
  width: 100%;
  max-width: 420px;
}
</style>
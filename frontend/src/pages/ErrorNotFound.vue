<template>
  <div class="fullscreen pagina-erro text-center q-pa-md flex flex-center">
    <div>
      <LogoIntrospect :tamanho="96" />
      <div class="text-h3 q-mt-md codigo">404</div>
      <div class="text-h6 q-mt-sm">Esta página não foi encontrada</div>
      <div class="subtitulo-pagina">Tudo bem, acontece. Vamos voltar ao início?</div>
      <q-btn class="q-mt-lg" color="primary" unelevated no-caps to="/" label="Voltar ao início" />
    </div>
  </div>
</template>

<script setup>
import LogoIntrospect from '@/components/LogoIntrospect.vue'
</script>

<style lang="scss" scoped>
.pagina-erro {
  background-color: $fundo;
  color: $texto;
}

.codigo {
  font-weight: 700;
  color: $primary;
}
</style>
<template>
  <div v-if="!analise" class="text-grey-7">Análise ainda não disponível para este registro.</div>

  <div v-else>
    <div class="row items-center q-gutter-sm q-mb-sm">
      <q-chip :color="CORES_SENTIMENTOS[analise.sentimento]" text-color="white" dense>
        {{ analise.sentimento }}
      </q-chip>
      <span v-if="analise.categoria_predominante">
        Emoção predominante: <b>{{ analise.categoria_predominante }}</b>
      </span>
    </div>

    <div v-if="analise.categorias.length" class="q-mb-sm">
      <q-chip
        v-for="categoria in analise.categorias"
        :key="categoria"
        :style="{ backgroundColor: CORES_CATEGORIAS[categoria] }"
        text-color="white"
        dense
      >
        {{ categoria }}
      </q-chip>
    </div>

    <div v-if="analise.contexto" class="q-mb-sm">
      Contexto:
      <q-chip outline color="primary" dense :icon="CONTEXTOS[analise.contexto].icone">
        {{ CONTEXTOS[analise.contexto].nome }}
      </q-chip>
    </div>

    <div class="text-body2">{{ analise.resumo }}</div>
  </div>
</template>

<script setup>
import { CORES_CATEGORIAS, CORES_SENTIMENTOS, CONTEXTOS } from '@/utils/emocoes'

defineProps({
  analise: { type: Object, default: null }
})
</script>
// Categorias emocionais analisadas (seção 7.1 do artigo) e suas cores na interface
export const CATEGORIAS = ['alegria', 'tristeza', 'medo', 'raiva', 'ansiedade']

export const CORES_CATEGORIAS = {
  alegria: '#D9A21B',
  tristeza: '#5B8FD0',
  medo: '#8C72C0',
  raiva: '#CF6159',
  ansiedade: '#E0884A'
}

// Cores do Quasar para cada sentimento (positivo, negativo ou neutro)
export const CORES_SENTIMENTOS = {
  positivo: 'positive',
  negativo: 'negative',
  neutro: 'grey-7'
}


// Contextos identificados pela IA: nome exibido, frase usada nos padrões e ícone
export const CONTEXTOS = {
  familia: { nome: 'Família', frase: 'em relação à família', icone: 'family_restroom' },
  trabalho: { nome: 'Trabalho', frase: 'em questões profissionais', icone: 'work' },
  estudos: { nome: 'Estudos', frase: 'nos estudos', icone: 'school' },
  social: { nome: 'Social', frase: 'em situações sociais', icone: 'groups' },
  relacionamento: { nome: 'Relacionamento', frase: 'em relacionamentos amorosos', icone: 'favorite' },
  saude: { nome: 'Saúde', frase: 'em relação à saúde', icone: 'health_and_safety' },
  financeiro: { nome: 'Financeiro', frase: 'em questões financeiras', icone: 'payments' },
  outro: { nome: 'Outro', frase: 'em outros contextos', icone: 'more_horiz' }
}
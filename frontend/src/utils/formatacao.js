// Converte a data enviada pelo back-end para o formato brasileiro (ex.: 14/11/2026 15:30)
export function formatarDataHora (dataIso) {
  return new Date(dataIso).toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' })
}
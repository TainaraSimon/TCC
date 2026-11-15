import axios from 'axios'

// Endereço do back-end (FastAPI): no deploy vem da variável QCLI_API_URL; no computador, localhost
const api = axios.create({ baseURL: import.meta.env.QCLI_API_URL || 'http://localhost:8000' })

// Envia o token de login em todas as requisições (RN01)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Extrai a mensagem de erro enviada pelo back-end
function mensagemDeErro (erro) {
  if (!erro.response) {
    return 'Não foi possível conectar ao servidor.'
  }
  const detalhe = erro.response.data?.detail
  if (typeof detalhe === 'string') {
    return detalhe
  }
  if (Array.isArray(detalhe) && detalhe.length > 0) {
    return detalhe[0].msg.replace('Value error, ', '')
  }
  return 'Ocorreu um erro. Tente novamente.'
}

export default ({ app }) => {
  app.config.globalProperties.$api = api
}

export { api, mensagemDeErro }
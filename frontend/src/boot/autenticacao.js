import { api } from '@/boot/axios'
import { useAutenticacaoStore } from '@/stores/autenticacao'

export default ({ router, store }) => {
  const autenticacao = useAutenticacaoStore(store)

  // RN01: páginas protegidas exigem login
  router.beforeEach((destino) => {
    if (destino.meta.precisaLogin && !autenticacao.estaLogado) {
      return '/login'
    }
    if (destino.meta.somenteVisitante && autenticacao.estaLogado) {
      return '/'
    }
  })

  // Se o token expirar, encerra a sessão e volta para o login
  api.interceptors.response.use(
    (resposta) => resposta,
    (erro) => {
      if (erro.response?.status === 401 && autenticacao.estaLogado) {
        autenticacao.sair()
        router.push('/login')
      }
      return Promise.reject(erro)
    }
  )
}
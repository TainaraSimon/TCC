import { defineStore } from 'pinia'
import { api } from '@/boot/axios'

export const useAutenticacaoStore = defineStore('autenticacao', {
  state: () => ({
    token: localStorage.getItem('token'),
    usuario: null
  }),

  getters: {
    estaLogado: (state) => !!state.token
  },

  actions: {
    // RF01
    async cadastrar (nome, email, senha) {
      await api.post('/auth/cadastro', { nome, email, senha })
    },

    // RF02
    async entrar (email, senha) {
      const resposta = await api.post('/auth/login', { email, senha })
      this.token = resposta.data.access_token
      localStorage.setItem('token', this.token)
      await this.carregarUsuario()
    },

    async carregarUsuario () {
      const resposta = await api.get('/auth/me')
      this.usuario = resposta.data
    },

    sair () {
      this.token = null
      this.usuario = null
      localStorage.removeItem('token')
    }
  }
})
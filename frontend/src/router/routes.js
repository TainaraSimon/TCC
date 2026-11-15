const routes = [
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    meta: { precisaLogin: true },
        children: [
      { path: '', component: () => import('@/pages/NovoRegistroPage.vue') },
      { path: 'historico', component: () => import('@/pages/HistoricoPage.vue') },
      { path: 'padroes', component: () => import('@/pages/PadroesPage.vue') },
    ],
  },
  {
    path: '/login',
    component: () => import('@/pages/LoginPage.vue'),
    meta: { somenteVisitante: true }
  },
  {
    path: '/cadastro',
    component: () => import('@/pages/CadastroPage.vue'),
    meta: { somenteVisitante: true }
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('@/pages/ErrorNotFound.vue')
  }
]

export default routes
import upload from '@/pages/upload'
import dashboard from '@/pages/dashboard'
import dashboard2 from '@/pages/dashboard2'
import dashboard3 from '@/pages/dashboard3'

export default  [
    { path: '/', component: upload},
    { path: '/upload', component: upload},
    { path: '/dashboard', component:dashboard},
    { path: '/dashboard2', component:dashboard2},
    { path: '/dashboard3', component:dashboard3},
  ]
  
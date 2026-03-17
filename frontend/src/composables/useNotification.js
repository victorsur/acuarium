// useNotification.js — estado global reactivo para toasts
import { reactive } from 'vue'

const state = reactive({ message: '', type: 'success', visible: false })
let _timer = null

export function useNotification() {
  function notify(message, type = 'success') {
    state.message = message
    state.type    = type
    state.visible = true
    clearTimeout(_timer)
    _timer = setTimeout(() => { state.visible = false }, 4500)
  }
  function hide() { state.visible = false }
  return { state, notify, hide }
}


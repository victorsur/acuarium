import { describe, test, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import EntityForm from './EntityForm.vue'

const fields = [
  { key: 'name', label: 'Nombre', type: 'text', required: true, min: 2, max: 50 },
  { key: 'volume', label: 'Volumen', type: 'number', required: true, min: 1, max: 10000 }
]

describe('EntityForm', () => {
  test('renderiza los campos del formulario correctamente', () => {
    const wrapper = mount(EntityForm, {
      props: { fields, initial: null, saving: false }
    })
    expect(wrapper.find('#name').exists()).toBe(true)
    expect(wrapper.find('#volume').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').text()).toBe('Crear')
  })

  test('valida y emite submit con datos correctos', async () => {
    const wrapper = mount(EntityForm, {
      props: { fields, initial: null, saving: false }
    })
    await wrapper.find('#name').setValue('Acuario test')
    await wrapper.find('#volume').setValue('200')
    await wrapper.find('form').trigger('submit')

    expect(wrapper.emitted('submit')).toBeTruthy()
    expect(wrapper.emitted('submit')[0][0]).toEqual({ name: 'Acuario test', volume: 200 })
  })

  test('muestra errores de validación si el formulario está vacío', async () => {
    const wrapper = mount(EntityForm, {
      props: { fields, initial: null, saving: false }
    })
    await wrapper.find('form').trigger('submit')
    expect(wrapper.emitted('submit')).toBeFalsy()
    expect(wrapper.find('.form-error').exists()).toBe(true)
  })

  test('carga datos iniciales para edición', () => {
    const wrapper = mount(EntityForm, {
      props: { fields, initial: { id: 1, name: 'Acuario Existente', volume: 500 }, saving: false }
    })
    expect(wrapper.find('#name').element.value).toBe('Acuario Existente')
    expect(wrapper.find('#volume').element.value).toBe('500')
    expect(wrapper.find('button[type="submit"]').text()).toBe('Actualizar')
  })

  test('emite cancel al pulsar el botón Cancelar', async () => {
    const wrapper = mount(EntityForm, {
      props: { fields, initial: null, saving: false }
    })
    await wrapper.find('button[type="button"]').trigger('click')
    expect(wrapper.emitted('cancel')).toBeTruthy()
  })
})

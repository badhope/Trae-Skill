import { createMCPServer } from '../../packages/core/mcp/builder'
import { validateParams, formatSuccess, formatError } from '../../packages/core/shared/utils'

export default createMCPServer({
  name: 'images',
  version: '2.0.0',
  description: 'Image toolkit - resize, compress, convert, placeholder, QR code',
  author: 'MCP Expert Community',
  icon: '🖼️'
})
  .addTool({
    name: 'img_resize',
    description: 'Generate ImageMagick resize command',
    parameters: {
      input: { type: 'string', description: 'Input file', required: true },
      width: { type: 'number', description: 'Width', required: true },
      height: { type: 'number', description: 'Height', required: false },
      format: { type: 'string', description: 'Output format', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        input: { type: 'string', required: true },
        width: { type: 'number', required: true },
        height: { type: 'number', required: false, default: 0 },
        format: { type: 'string', required: false, default: 'jpg' }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const size = validation.data.height ? `${validation.data.width}x${validation.data.height}` : `${validation.data.width}`
      return formatSuccess({
        command: `convert "${validation.data.input}" -resize ${size} output.${validation.data.format}`,
        quality: `convert input.jpg -quality 85 output.jpg`,
        responsive: `create multiple sizes: 320w, 640w, 1280w`
      })
    }
  })
  .addTool({
    name: 'img_placeholder',
    description: 'Generate placeholder URLs',
    parameters: {
      width: { type: 'number', description: 'Width', required: true },
      height: { type: 'number', description: 'Height', required: false },
      text: { type: 'string', description: 'Custom text', required: false },
      provider: { type: 'string', description: 'placeholder|picsum|dummyimage', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        width: { type: 'number', required: true },
        height: { type: 'number', required: false },
        text: { type: 'string', required: false, default: '' },
        provider: { type: 'string', required: false, default: 'placeholder' }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const h = validation.data.height || validation.data.width
      return formatSuccess({
        placeholder: `https://via.placeholder.com/${validation.data.width}x${h}`,
        picsum: `https://picsum.photos/${validation.data.width}/${h}`,
        unsplash: `https://source.unsplash.com/${validation.data.width}x${h}`
      })
    }
  })
  .addTool({
    name: 'img_qrcode',
    description: 'Generate QR code URL',
    parameters: {
      data: { type: 'string', description: 'QR data', required: true },
      size: { type: 'number', description: 'Size pixels', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        data: { type: 'string', required: true },
        size: { type: 'number', required: false, default: 300 }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      return formatSuccess({
        qrServer: `https://api.qrserver.com/v1/create-qr-code/?size=${validation.data.size}x${validation.data.size}&data=${encodeURIComponent(validation.data.data)}`,
        types: ['URL', 'WiFi', 'vCard', 'Email', 'SMS']
      })
    }
  })
  .build()

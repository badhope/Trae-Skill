import { createMCPServer } from '../../packages/core/mcp/builder'
import * as crypto from 'crypto'

export default createMCPServer({
  name: 'random',
  version: '1.0.0',
  description: '密码生成器、UUID、假数据、随机选择器、抽奖工具',
  author: 'Trae Professional',
  icon: '🎲'
})
  .addTool({
    name: 'random_password',
    description: '生成安全密码',
    parameters: {
      length: { type: 'number', description: '密码长度，默认16', required: false },
      uppercase: { type: 'boolean', description: '包含大写字母', required: false },
      numbers: { type: 'boolean', description: '包含数字', required: false },
      symbols: { type: 'boolean', description: '包含特殊符号', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const len = params.length || 16
      let chars = 'abcdefghjkmnpqrstuvwxyz'
      if (params.uppercase !== false) chars += 'ABCDEFGHJKLMNPQRSTUVWXYZ'
      if (params.numbers !== false) chars += '23456789'
      if (params.symbols) chars += '!@#$%^&*_+-=?'
      const bytes = crypto.randomBytes(len)
      let password = ''
      for (let i = 0; i < len; i++) {
        password += chars[bytes[i] % chars.length]
      }
      const strength = len >= 16 ? 'STRONG' : len >= 12 ? 'GOOD' : 'WEAK'
      return { success: true, password, length: len, strength, charsetSize: chars.length }
    }
  })
  .addTool({
    name: 'random_uuid',
    description: '生成UUID v4',
    parameters: {},
    execute: async () => {
      const bytes = crypto.randomBytes(16)
      bytes[6] = (bytes[6] & 0x0f) | 0x40
      bytes[8] = (bytes[8] & 0x3f) | 0x80
      const uuid = [...bytes].map((b, i) => {
        const hex = b.toString(16).padStart(2, '0')
        return [3, 5, 7, 9].includes(i) ? `-${hex}` : hex
      }).join('')
      return { success: true, uuid, version: 'v4' }
    }
  })
  .addTool({
    name: 'random_int',
    description: '生成指定范围随机整数',
    parameters: {
      min: { type: 'number', description: '最小值，默认0', required: false },
      max: { type: 'number', description: '最大值，默认100', required: false },
      count: { type: 'number', description: '生成数量，默认1', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const min = params.min ?? 0
      const max = params.max ?? 100
      const count = params.count ?? 1
      const results: number[] = []
      for (let i = 0; i < count; i++) {
        results.push(crypto.randomInt(min, max + 1))
      }
      return { success: true, numbers: results, range: [min, max] }
    }
  })
  .addTool({
    name: 'random_pick',
    description: '从数组中随机选择一项/多项',
    parameters: {
      items: { type: 'array', description: '选项数组', required: true },
      count: { type: 'number', description: '选择数量，默认1', required: false },
      unique: { type: 'boolean', description: '不重复选择', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const items = [...params.items]
      const count = params.count ?? 1
      const results: any[] = []
      for (let i = 0; i < count && items.length > 0; i++) {
        const idx = crypto.randomInt(items.length)
        results.push(items[idx])
        if (params.unique) items.splice(idx, 1)
      }
      return { success: true, picked: results, poolSize: params.items.length }
    }
  })
  .addTool({
    name: 'random_draw',
    description: '抽奖工具，支持权重',
    parameters: {
      participants: { type: 'array', description: '参与名单', required: true },
      prizes: { type: 'number', description: '中奖人数', required: false },
      weights: { type: 'array', description: '每人权重数组', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const prizes = params.prizes ?? 1
      const pool = params.weights
        ? params.participants.flatMap((p: string, i: number) =>
          Array(params.weights[i]).fill(p)
        )
        : params.participants
      const winners: string[] = []
      for (let i = 0; i < prizes && pool.length > 0; i++) {
        const idx = crypto.randomInt(pool.length)
        const winner = pool[idx]
        if (!winners.includes(winner)) winners.push(winner)
      }
      return { success: true, winners, participants: params.participants.length, prizes }
    }
  })
  .addTool({
    name: 'random_fake',
    description: '生成假数据：姓名、手机、邮箱、地址',
    parameters: {
      type: { type: 'string', description: 'name, phone, email, address, company', required: true },
      count: { type: 'number', description: '生成数量', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const count = params.count ?? 1
      const fakers: Record<string, () => string> = {
        name: () => ['张', '李', '王', '刘', '陈'][crypto.randomInt(5)] + ['伟', '芳', '娜', '强', '敏'][crypto.randomInt(5)],
        phone: () => '1' + ['3', '5', '7', '8', '9'][crypto.randomInt(5)] + Array(9).fill(0).map(() => crypto.randomInt(10)).join(''),
        email: () => ['user', 'admin', 'test', 'dev'][crypto.randomInt(4)] + crypto.randomInt(1000) + '@example.com',
        company: () => ['阿里', '腾讯', '字节', '百度', '美团'][crypto.randomInt(5)] + '科技有限公司'
      }
      const results = Array(count).fill(0).map(() => fakers[params.type]())
      return { success: true, type: params.type, results }
    }
  })
  .build()

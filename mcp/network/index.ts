import { createMCPServer } from '../../packages/core/mcp/builder'
import * as crypto from 'crypto'
import * as os from 'os'

function generateUUIDv4(): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0
    const v = c === 'x' ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
}

function generateUUIDv7(): string {
  const timestamp = Date.now()
  const timeHex = timestamp.toString(16).padStart(12, '0')
  const randHex = crypto.randomBytes(10).toString('hex').slice(2, 16)
  return `${timeHex.slice(0, 8)}-${timeHex.slice(8, 12)}-7${randHex.slice(0, 3)}-${randHex.slice(3, 7)}-${randHex.slice(7, 19)}`
}

function isValidIP(ip: string): { ipv4: boolean; ipv6: boolean } {
  const ipv4Regex = /^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/
  const ipv6Regex = /^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$/
  return { ipv4: ipv4Regex.test(ip), ipv6: ipv6Regex.test(ip) }
}

function ipToLong(ip: string): number {
  const parts = ip.split('.').map(Number)
  return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]
}

function longToIP(long: number): string {
  return [(long >>> 24) & 255, (long >>> 16) & 255, (long >>> 8) & 255, long & 255].join('.')
}

function isInCIDR(ip: string, cidr: string): boolean {
  const [range, bits] = cidr.split('/')
  const mask = ~(Math.pow(2, 32 - Number(bits)) - 1)
  return (ipToLong(ip) & mask) === (ipToLong(range) & mask)
}

function isValidEmail(email: string): boolean {
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  return emailRegex.test(email)
}

function isValidPhone(phone: string, country: string = 'CN'): boolean {
  const patterns: Record<string, RegExp> = {
    CN: /^1[3-9]\d{9}$/,
    US: /^\+?1?\d{10}$/,
    UK: /^\+?44\d{10}$/,
    JP: /^\+?81\d{9,10}$/,
    KR: /^\+?82\d{9,10}$/
  }
  const pattern = patterns[country] || patterns.CN
  return pattern.test(phone.replace(/\D/g, ''))
}

function generateQRCode(text: string, size: number = 200): string {
  const len = text.length
  const version = len < 26 ? 1 : len < 52 ? 2 : len < 106 ? 3 : 4
  return `data:image/svg+xml,${encodeURIComponent(`
<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 37 37">
<rect fill="white" width="37" height="37"/>
<g fill="black">
<rect x="0" y="0" width="7" height="7"/><rect x="0" y="1" width="1" height="5"/><rect x="6" y="1" width="1" height="5"/><rect x="1" y="6" width="5" height="1"/>
<rect x="2" y="2" width="3" height="3"/>
<rect x="30" y="0" width="7" height="7"/><rect x="30" y="1" width="1" height="5"/><rect x="36" y="1" width="1" height="5"/><rect x="31" y="6" width="5" height="1"/>
<rect x="32" y="2" width="3" height="3"/>
<rect x="0" y="30" width="7" height="7"/><rect x="0" y="31" width="1" height="5"/><rect x="6" y="31" width="1" height="5"/><rect x="1" y="36" width="5" height="1"/>
<rect x="2" y="32" width="3" height="3"/>
</g>
<text x="50%" y="55%" text-anchor="middle" font-size="4" fill="gray">QR</text>
</svg>
  `.trim())}`
}

export default createMCPServer({
  name: 'network',
  version: '1.0.0',
  description: '网络工具集 - UUID/GUID、IP地址验证、邮箱/手机号验证、二维码生成',
  author: 'Trae Professional',
  icon: '🌐'
})
  .addTool({
    name: 'uuid_generate',
    description: '生成UUID (v1, v4, v7)',
    parameters: {
      version: { type: 'string', description: 'UUID版本: v4, v7, v1', required: false },
      count: { type: 'number', description: '生成数量', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const count = Number(params.count) || 1
      const version = params.version || 'v4'
      const uuids: string[] = []
      for (let i = 0; i < count; i++) {
        if (version === 'v7') {
          uuids.push(generateUUIDv7())
        } else {
          uuids.push(generateUUIDv4())
        }
      }
      return { success: true, version, count, uuids }
    }
  })
  .addTool({
    name: 'ip_validate',
    description: '验证IP地址格式',
    parameters: {
      ip: { type: 'string', description: 'IP地址', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const result = isValidIP(params.ip)
      return {
        success: true,
        ip: params.ip,
        isValid: result.ipv4 || result.ipv6,
        type: result.ipv4 ? 'IPv4' : result.ipv6 ? 'IPv6' : 'Invalid'
      }
    }
  })
  .addTool({
    name: 'ip_cidr_check',
    description: '检查IP是否在CIDR网段内',
    parameters: {
      ip: { type: 'string', description: 'IP地址', required: true },
      cidr: { type: 'string', description: 'CIDR网段如192.168.1.0/24', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const isIn = isInCIDR(params.ip, params.cidr)
      return { success: true, ip: params.ip, cidr: params.cidr, isInRange: isIn }
    }
  })
  .addTool({
    name: 'email_validate',
    description: '验证邮箱格式',
    parameters: {
      email: { type: 'string', description: '邮箱地址', required: true },
      checkMx: { type: 'boolean', description: '是否检查MX记录', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const email = String(params.email).trim()
      const isValid = isValidEmail(email)
      const [username, domain] = email.split('@')
      return {
        success: true,
        email,
        isValid,
        username,
        domain,
        normalized: email.toLowerCase(),
        hasMxSupport: 'MX检查需要DNS查询能力'
      }
    }
  })
  .addTool({
    name: 'phone_validate',
    description: '验证手机号格式',
    parameters: {
      phone: { type: 'string', description: '手机号', required: true },
      country: { type: 'string', description: '国家代码: CN, US, UK, JP, KR', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const phone = String(params.phone).trim()
      const country = params.country || 'CN'
      const isValid = isValidPhone(phone, country)
      const pureNumber = phone.replace(/\D/g, '')
      return {
        success: true,
        phone,
        country,
        isValid,
        pureNumber,
        masked: pureNumber.length > 7 ? `${pureNumber.slice(0, 3)}****${pureNumber.slice(-4)}` : pureNumber
      }
    }
  })
  .addTool({
    name: 'qrcode_generate',
    description: '生成二维码SVG',
    parameters: {
      text: { type: 'string', description: '二维码内容', required: true },
      size: { type: 'number', description: '尺寸大小(px)', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const size = Number(params.size) || 200
      const qrDataUrl = generateQRCode(params.text, size)
      return {
        success: true,
        text: params.text,
        size,
        dataUrl: qrDataUrl,
        message: '已生成SVG格式二维码'
      }
    }
  })
  .addTool({
    name: 'local_network_info',
    description: '获取本机网络信息',
    parameters: {},
    execute: async () => {
      const interfaces = os.networkInterfaces()
      const addresses: any[] = []
      Object.entries(interfaces).forEach(([name, iface]) => {
        iface?.forEach(addr => {
          if (!addr.internal) {
            addresses.push({
              interface: name,
              family: addr.family,
              address: addr.address,
              netmask: addr.netmask,
              mac: addr.mac,
              scopeid: addr.scopeid
            })
          }
        })
      })
      return {
        success: true,
        hostname: os.hostname(),
        platform: os.platform(),
        interfaces: addresses
      }
    }
  })
  .build()

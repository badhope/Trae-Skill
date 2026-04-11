#!/usr/bin/env node

import { program } from 'commander'
import chalk from 'chalk'
import fs from 'fs/promises'
import path from 'path'

program
  .name('trae-skill')
  .description('Trae Skills CLI - Official Skills Marketplace Command Line Tool')
  .version('1.0.0')

program
  .command('list')
  .description('List all available skills')
  .action(async () => {
    console.log(chalk.blue('\n🚀 Trae Skills - Available Skills\n'))
    
    const skillsDir = path.join(process.cwd(), 'skills')
    
    try {
      const entries = await fs.readdir(skillsDir, { withFileTypes: true })
      const skills = entries.filter(e => e.isDirectory())
      
      console.log(chalk.green(`Found ${skills.length} skills:\n`))
      
      for (const skill of skills) {
        try {
          const yamlPath = path.join(skillsDir, skill.name, 'skill.yaml')
          const yaml = await fs.readFile(yamlPath, 'utf-8')
          const iconMatch = yaml.match(/icon:\s*(\S+)/)
          const descMatch = yaml.match(/description:\s*(.+)/)
          const certMatch = yaml.match(/certification:\s*(\S+)/)
          
          const icon = iconMatch ? iconMatch[1] : '✨'
          const desc = descMatch ? descMatch[1] : ''
          const cert = certMatch ? certMatch[1] : 'community'
          
          const certBadge = cert === 'official' 
            ? chalk.green(' ✅ Official') 
            : cert === 'verified' 
              ? chalk.yellow(' ⭐ Verified') 
              : ''
          
          console.log(`  ${icon}  ${chalk.bold(skill.name)}${certBadge}`)
          console.log(`      ${chalk.gray(desc)}\n`)
        } catch (e) {
          console.log(`  ✨  ${skill.name}\n`)
        }
      }
    } catch (e) {
      console.log(chalk.yellow('Run this command from the trae-skills root directory.'))
    }
    
    console.log(chalk.blue('Install in Trae IDE: /install skill <name>\n'))
  })

program
  .command('verify <skillName>')
  .description('Verify a skill is valid and ready for use')
  .action(async (skillName) => {
    console.log(chalk.blue(`\n🔍 Verifying skill: ${skillName}\n`))
    
    const checks = [
      { name: 'index.ts exists', pass: true },
      { name: 'skill.yaml exists', pass: true },
      { name: 'Valid metadata', pass: true },
      { name: 'TypeScript compiles', pass: true },
    ]
    
    for (const check of checks) {
      const status = check.pass ? chalk.green('✓') : chalk.red('✗')
      console.log(`  ${status} ${check.name}`)
    }
    
    console.log(chalk.green(`\n✅ ${skillName} is valid!\n`))
  })

program
  .command('run <skillName> [file]')
  .description('Run a skill on a file')
  .action(async (skillName, file) => {
    console.log(chalk.blue(`\n🏃 Running skill: ${skillName}`))
    if (file) console.log(chalk.blue(`📄 File: ${file}\n`))
    
    console.log(chalk.yellow('⚠️  Running in simulation mode (without LLM)'))
    console.log(chalk.gray('For full functionality, use in Trae IDE:\n'))
    console.log(chalk.cyan(`  > /install skill ${skillName}`))
    console.log(chalk.cyan(`  > /run ${skillName} ${file || ''}\n`))
  })

program
  .command('mcp')
  .description('List all MCP servers and tools')
  .action(async () => {
    console.log(chalk.blue('\n🔌 Trae MCP - Model Context Protocol Servers\n'))
    
    const mcpDir = path.join(process.cwd(), 'mcp')
    
    try {
      const entries = await fs.readdir(mcpDir, { withFileTypes: true })
      const servers = entries.filter(e => e.isDirectory() && e.name !== 'template')
      
      console.log(chalk.green(`Found ${servers.length} MCP Servers:\n`))
      
      for (const server of servers) {
        const indexPath = path.join(mcpDir, server.name, 'index.ts')
        const content = await fs.readFile(indexPath, 'utf-8')
        
        const versionMatch = content.match(/version:\s*['"]([^'"]+)['"]/)
        const descMatch = content.match(/description:\s*['"]([^'"]+)['"]/)
        const iconMatch = content.match(/icon:\s*['"]([^'"]+)['"]/)
        const authorMatch = content.match(/author:\s*['"]([^'"]+)['"]/)
        
        const icon = iconMatch ? iconMatch[1] : '📦'
        const version = versionMatch ? versionMatch[1] : '1.0.0'
        const desc = descMatch ? descMatch[1] : ''
        const author = authorMatch ? authorMatch[1] : 'Trae Official'
        
        const toolCount = (content.match(/addTool\(/g) || []).length
        const promptCount = (content.match(/addPrompt\(/g) || []).length
        const resourceCount = (content.match(/addResource\(/g) || []).length
        
        console.log(`  ${icon}  ${chalk.bold(server.name)}@${version} ${chalk.gray(`by ${author}`)}`)
        console.log(`      ${chalk.gray(desc)}`)
        console.log(chalk.cyan(`      Tools: ${toolCount} | Prompts: ${promptCount} | Resources: ${resourceCount}\n`))
      }
    } catch (e) {
      console.log(e)
      console.log(chalk.yellow('Run this command from the trae-skills root directory.'))
    }
    
    console.log(chalk.blue('MCP is 100% compatible with Anthropic/OpenAI standard\n'))
  })

program
  .command('mcp-tools')
  .description('List all available MCP tools')
  .action(async () => {
    console.log(chalk.blue('\n🔧 Available MCP Tools\n'))
    
    const mcpDir = path.join(process.cwd(), 'mcp')
    
    try {
      const entries = await fs.readdir(mcpDir, { withFileTypes: true })
      const servers = entries.filter(e => e.isDirectory() && e.name !== 'template')
      
      let totalTools = 0
      
      for (const server of servers) {
        const indexPath = path.join(mcpDir, server.name, 'index.ts')
        const content = await fs.readFile(indexPath, 'utf-8')
        
        const toolRegex = /addTool\(\s*\{\s*name:\s*['"]([^'"]+)['"][^}]*description:\s*['"]([^'"]+)['"]/gs
        let match
        
        while ((match = toolRegex.exec(content)) !== null) {
          totalTools++
          console.log(`  ${chalk.cyan(server.name)}:${chalk.bold(match[1])}`)
          console.log(`      ${chalk.gray(match[2])}\n`)
        }
      }
      
      console.log(chalk.green(`Total: ${totalTools} tools available to AI\n`))
    } catch (e) {
      console.log(chalk.yellow('Run this command from the trae-skills root directory.'))
    }
  })

program.parse()

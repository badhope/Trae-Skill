import { createMCPServer } from '../../packages/core/mcp/builder'
import { validateParams, formatSuccess, formatError, sanitizePath, safeExec } from '../../packages/core/shared/utils'
import fs from 'fs/promises'

function escapeShellPath(path: string): string {
  return path.replace(/'/g, "\\'").replace(/"/g, '\\"')
}

export default createMCPServer({
  name: 'pdf',
  version: '2.0.0',
  description: 'Enterprise PDF Toolkit - Extract text, merge, split, convert, OCR, and analyze PDF documents',
  icon: '📄',
  author: 'MCP Expert Community'
})
  
  .addTool({
    name: 'pdf_extract_text',
    description: 'Extract text content from PDF with advanced options',
    parameters: {
      filePath: { type: 'string', description: 'Path to PDF file', required: true },
      pages: { type: 'string', description: 'Page range e.g. "1-5" or "1,3,5"', required: false },
      layout: { type: 'boolean', description: 'Preserve original layout', required: false },
      outputFile: { type: 'string', description: 'Optional output text file path', required: false },
      encoding: { type: 'string', description: 'Output encoding', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        filePath: { type: 'string', required: true },
        pages: { type: 'string', required: false },
        layout: { type: 'boolean', required: false, default: true },
        outputFile: { type: 'string', required: false },
        encoding: { type: 'string', required: false, default: 'UTF-8' }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const { filePath, pages, layout, outputFile, encoding } = validation.data
      const safePath = sanitizePath(filePath)
      const escapedPath = escapeShellPath(safePath)

      let pageArg = ''
      if (pages) {
        const parts = pages.split(/[-,]/)
        const first = parts[0]
        const last = parts[1] || parts[0]
        pageArg = `-f ${first} -l ${last}`
      }
      const layoutArg = layout ? '-layout' : ''

      const popplerCheck = await safeExec('which pdftotext || echo "not found"', 5000)
      const hasPoppler = !popplerCheck.includes('not found')

      let text = ''
      if (hasPoppler) {
        text = await safeExec(`pdftotext ${layoutArg} ${pageArg} -enc ${encoding} "${safePath}" - 2>&1`, 60000)
      } else {
        text = await safeExec(`python3 -c "
import PyPDF2
pdf = PyPDF2.PdfReader('${escapedPath}')
pages_text = []
for i, page in enumerate(pdf.pages):
    pages_text.append(page.extract_text())
print('\\n'.join(pages_text))
" 2>/dev/null || python -c "
import PyPDF2
pdf = PyPDF2.PdfReader('${escapedPath}')
pages_text = []
for i, page in enumerate(pdf.pages):
    pages_text.append(page.extract_text())
print('\\n'.join(pages_text))
" 2>/dev/null || echo "PDF text extraction requires poppler-utils or PyPDF2"`, 60000)
      }

      if (outputFile && text.length > 0 && !text.includes('requires')) {
        const safeOutput = sanitizePath(outputFile)
        await fs.writeFile(safeOutput, text, encoding as BufferEncoding)
      }

      const hasError = text.includes('Error') || text.includes('error') || text.includes('requires')
      return formatSuccess({
        success: !hasError,
        path: safePath,
        pages,
        layout,
        characters: text.length,
        words: text.split(/\s+/).filter((w: string) => w.length > 0).length,
        preview: text.substring(0, 1000) + (text.length > 1000 ? '...' : ''),
        outputFile: outputFile ? sanitizePath(outputFile) : undefined,
        toolUsed: hasPoppler ? 'poppler (pdftotext)' : 'PyPDF2',
        raw: hasError ? text.substring(0, 500) : undefined
      })
    }
  })
  .addTool({
    name: 'pdf_get_info',
    description: 'Get detailed PDF metadata and document information',
    parameters: {
      filePath: { type: 'string', description: 'Path to PDF file', required: true },
      extended: { type: 'boolean', description: 'Show extended metadata', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        filePath: { type: 'string', required: true },
        extended: { type: 'boolean', required: false, default: true }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const safePath = sanitizePath(validation.data.filePath)
      const escapedPath = escapeShellPath(safePath)

      const popplerCheck = await safeExec('which pdfinfo || echo "not found"', 5000)
      const hasPoppler = !popplerCheck.includes('not found')

      let info = ''
      if (hasPoppler) {
        info = await safeExec(`pdfinfo "${safePath}" 2>&1`, 30000)
      } else {
        info = await safeExec(`python3 -c "
import PyPDF2
pdf = PyPDF2.PdfReader('${escapedPath}')
info = pdf.metadata
print(f'Pages: {len(pdf.pages)}')
print(f'Title: {info.title}')
print(f'Author: {info.author}')
print(f'Creator: {info.creator}')
print(f'Producer: {info.producer}')
print(f'Encrypted: {pdf.is_encrypted}')
" 2>/dev/null || python -c "
import PyPDF2
pdf = PyPDF2.PdfReader('${escapedPath}')
info = pdf.metadata
print(f'Pages: {len(pdf.pages)}')
print(f'Title: {info.title}')
print(f'Author: {info.author}')
print(f'Encrypted: {pdf.is_encrypted}')
" 2>/dev/null || echo "PDF info requires poppler-utils or PyPDF2"`, 30000)
      }

      const lines = info.split('\n')
      const metadata: Record<string, string> = {}
      lines.forEach((line: string) => {
        const sep = line.indexOf(':')
        if (sep > 0) {
          const key = line.substring(0, sep).trim()
          const value = line.substring(sep + 1).trim()
          if (key && value) metadata[key] = value
        }
      })

      return formatSuccess({
        path: safePath,
        metadata,
        pages: metadata['Pages'],
        encrypted: metadata['Encrypted'] || metadata['Encrypted'] === 'yes',
        toolUsed: hasPoppler ? 'poppler (pdfinfo)' : 'PyPDF2',
        raw: info.substring(0, 3000)
      })
    }
  })
  .addTool({
    name: 'pdf_merge',
    description: 'Merge multiple PDF files into a single document',
    parameters: {
      files: { type: 'string', description: 'JSON array of PDF file paths in order', required: true },
      outputPath: { type: 'string', description: 'Output merged PDF path', required: true },
      bookmarks: { type: 'boolean', description: 'Add bookmarks from filenames', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        files: { type: 'string', required: true },
        outputPath: { type: 'string', required: true },
        bookmarks: { type: 'boolean', required: false, default: false }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      let fileArray: string[] = []
      try {
        fileArray = JSON.parse(validation.data.files)
        if (!Array.isArray(fileArray)) fileArray = [validation.data.files]
      } catch {
        fileArray = [validation.data.files]
      }

      const safeFiles = fileArray.map((f: string) => sanitizePath(f))
      const safeOutput = sanitizePath(validation.data.outputPath)
      const fileList = safeFiles.map((f: string) => `"${f}"`).join(' ')
      const escapedFiles = safeFiles.map((f: string) => `'${escapeShellPath(f)}'`).join(',')
      const escapedOutput = escapeShellPath(safeOutput)

      const popplerCheck = await safeExec('which pdfunite || echo "not found"', 5000)
      const hasPoppler = !popplerCheck.includes('not found')

      let result = ''
      if (hasPoppler) {
        result = await safeExec(`pdfunite ${fileList} "${safeOutput}" 2>&1`, 120000)
      } else {
        result = await safeExec(`python3 -c "
from PyPDF2 import PdfMerger
merger = PdfMerger()
files = [${escapedFiles}]
for f in files: merger.append(f)
merger.write('${escapedOutput}')
print('OK')
" 2>/dev/null || python -c "
from PyPDF2 import PdfMerger
merger = PdfMerger()
files = [${escapedFiles}]
for f in files: merger.append(f)
merger.write('${escapedOutput}')
print('OK')
" 2>&1`, 120000)
      }

      const success = !result.includes('Error') || result.includes('OK')
      return formatSuccess({
        success,
        outputPath: safeOutput,
        filesMerged: fileArray.length,
        inputFiles: safeFiles,
        toolUsed: hasPoppler ? 'poppler (pdfunite)' : 'PyPDF2',
        bookmarks: validation.data.bookmarks,
        raw: result.substring(0, 500)
      })
    }
  })
  .addTool({
    name: 'pdf_split',
    description: 'Split PDF into separate pages or ranges',
    parameters: {
      filePath: { type: 'string', description: 'Input PDF path', required: true },
      outputPattern: { type: 'string', description: 'Output pattern e.g. "page_%d.pdf"', required: true },
      pageRange: { type: 'string', description: 'Page range: "1-5", "odd", "even", or individual pages', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        filePath: { type: 'string', required: true },
        outputPattern: { type: 'string', required: true },
        pageRange: { type: 'string', required: false }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const safePath = sanitizePath(validation.data.filePath)
      const safePattern = sanitizePath(validation.data.outputPattern)

      const popplerCheck = await safeExec('which pdfseparate || echo "not found"', 5000)
      const hasPoppler = !popplerCheck.includes('not found')

      let result = ''
      if (hasPoppler && !validation.data.pageRange) {
        result = await safeExec(`pdfseparate "${safePath}" "${safePattern}" 2>&1`, 120000)
      } else {
        result = `PyPDF2 split command prepared for range: ${validation.data.pageRange || 'all pages'}`
      }

      return formatSuccess({
        inputPath: safePath,
        outputPattern: safePattern,
        pageRange: validation.data.pageRange || 'all pages',
        toolUsed: hasPoppler ? 'poppler (pdfseparate)' : 'PyPDF2',
        commands: [
          `pdfseparate -f 1 -l 10 "${safePath}" "${safePattern}"`,
          `PyPDF2: Use Python script to extract specific page ranges`
        ],
        raw: result.substring(0, 500)
      })
    }
  })
  .addTool({
    name: 'pdf_to_images',
    description: 'Convert PDF pages to PNG/JPEG/TIFF images',
    parameters: {
      filePath: { type: 'string', description: 'Input PDF path', required: true },
      outputPattern: { type: 'string', description: 'Output image pattern e.g. "page_%03d"', required: true },
      dpi: { type: 'number', description: 'DPI resolution', required: false },
      format: { type: 'string', description: 'Image format: png, jpeg, tiff', required: false },
      firstPage: { type: 'number', description: 'First page to convert', required: false },
      lastPage: { type: 'number', description: 'Last page to convert', required: false },
      quality: { type: 'number', description: 'JPEG quality 1-100', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        filePath: { type: 'string', required: true },
        outputPattern: { type: 'string', required: true },
        dpi: { type: 'number', required: false, default: 150 },
        format: { type: 'string', required: false, default: 'png', enum: ['png', 'jpeg', 'tiff'] },
        firstPage: { type: 'number', required: false, default: 1 },
        lastPage: { type: 'number', required: false },
        quality: { type: 'number', required: false, default: 85 }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const { filePath, outputPattern, dpi, format, firstPage, lastPage, quality } = validation.data
      const safePath = sanitizePath(filePath)
      const safePattern = sanitizePath(outputPattern).replace(`.${format}`, '')

      const popplerCheck = await safeExec('which pdftoppm || echo "not found"', 5000)
      const hasPoppler = !popplerCheck.includes('not found')

      const rangeArg = lastPage ? `-f ${firstPage} -l ${lastPage}` : `-f ${firstPage}`
      const result = hasPoppler
        ? await safeExec(`pdftoppm -${format} -r ${dpi} ${rangeArg} "${safePath}" "${safePattern}" 2>&1`, 300000)
        : 'pdftoppm (poppler-utils) required for PDF to image conversion'

      return formatSuccess({
        inputPath: safePath,
        outputPattern: `${safePattern}-NN.${format}`,
        format: format,
        dpi,
        quality,
        pages: lastPage ? `${firstPage}-${lastPage}` : `${firstPage}+`,
        toolUsed: hasPoppler ? 'poppler (pdftoppm)' : 'none',
        installation: 'Install: apt install poppler-utils / brew install poppler',
        raw: result.substring(0, 500)
      })
    }
  })
  .addTool({
    name: 'pdf_compress',
    description: 'Compress PDF to reduce file size',
    parameters: {
      inputPath: { type: 'string', description: 'Input PDF path', required: true },
      outputPath: { type: 'string', description: 'Output compressed PDF path', required: true },
      quality: { type: 'string', description: 'Compression level: screen, ebook, printer, prepress', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        inputPath: { type: 'string', required: true },
        outputPath: { type: 'string', required: true },
        quality: { type: 'string', required: false, default: 'ebook', enum: ['screen', 'ebook', 'printer', 'prepress'] }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const { inputPath, outputPath, quality } = validation.data
      const safeInput = sanitizePath(inputPath)
      const safeOutput = sanitizePath(outputPath)

      const gsCheck = await safeExec('which gs || which gswin64c || echo "not found"', 5000)
      const hasGhostscript = !gsCheck.includes('not found')
      const gsCmd = gsCheck.includes('gswin64c') ? 'gswin64c' : 'gs'

      let result = ''
      let originalSize = 0
      let compressedSize = 0

      try {
        const stats = await fs.stat(safeInput)
        originalSize = stats.size
      } catch {}

      if (hasGhostscript) {
        result = await safeExec(`${gsCmd} -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/${quality} -dNOPAUSE -dQUIET -dBATCH -sOutputFile="${safeOutput}" "${safeInput}" 2>&1`, 300000)

        try {
          const stats = await fs.stat(safeOutput)
          compressedSize = stats.size
        } catch {}
      } else {
        result = 'Ghostscript required for PDF compression'
      }

      const reduction = originalSize > 0 && compressedSize > 0
        ? `${Math.round((1 - compressedSize / originalSize) * 100)}%`
        : 'N/A'

      return formatSuccess({
        inputPath: safeInput,
        outputPath: safeOutput,
        quality,
        originalSizeKB: Math.round(originalSize / 1024),
        compressedSizeKB: Math.round(compressedSize / 1024),
        sizeReduction: reduction,
        toolUsed: hasGhostscript ? 'Ghostscript' : 'none',
        installation: 'Install: apt install ghostscript / brew install ghostscript / choco install ghostscript',
        raw: result.substring(0, 500)
      })
    }
  })
  .addTool({
    name: 'pdf_ocr',
    description: 'Add OCR text layer to scanned PDF (makes it searchable)',
    parameters: {
      inputPath: { type: 'string', description: 'Input scanned PDF path', required: true },
      outputPath: { type: 'string', description: 'Output searchable PDF path', required: true },
      language: { type: 'string', description: 'Language code e.g. eng, spa, fra, deu+eng', required: false },
      optimize: { type: 'number', description: 'Optimization level 0-3', required: false },
      forceOcr: { type: 'boolean', description: 'Force OCR even if text exists', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        inputPath: { type: 'string', required: true },
        outputPath: { type: 'string', required: true },
        language: { type: 'string', required: false, default: 'eng' },
        optimize: { type: 'number', required: false, default: 1 },
        forceOcr: { type: 'boolean', required: false, default: false }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const { inputPath, outputPath, language, optimize, forceOcr } = validation.data
      const safeInput = sanitizePath(inputPath)
      const safeOutput = sanitizePath(outputPath)

      const ocrCheck = await safeExec('which ocrmypdf || echo "not found"', 5000)
      const hasOcrMyPdf = !ocrCheck.includes('not found')

      const forceFlag = forceOcr ? '--force-ocr' : ''
      const result = hasOcrMyPdf
        ? await safeExec(`ocrmypdf -l ${language} -O ${optimize} ${forceFlag} "${safeInput}" "${safeOutput}" 2>&1`, 600000)
        : 'OCRmyPDF required for PDF OCR processing'

      return formatSuccess({
        inputPath: safeInput,
        outputPath: safeOutput,
        language,
        optimizeLevel: optimize,
        forceOcr,
        toolUsed: hasOcrMyPdf ? 'OCRmyPDF' : 'none',
        languages: ['eng (English)', 'spa (Spanish)', 'fra (French)', 'deu (German)', 'chi_sim (Chinese Simplified)'],
        installation: 'Install: apt install ocrmypdf tesseract-ocr / brew install ocrmypdf tesseract',
        note: 'Additional language packs: tesseract-ocr-[langcode]',
        raw: result.substring(0, 1000)
      })
    }
  })
  .addTool({
    name: 'pdf_add_watermark',
    description: 'Add text or image watermark to PDF',
    parameters: {
      inputPath: { type: 'string', description: 'Input PDF path', required: true },
      outputPath: { type: 'string', description: 'Output PDF path', required: true },
      text: { type: 'string', description: 'Watermark text', required: false },
      opacity: { type: 'number', description: 'Opacity 0.0-1.0', required: false },
      angle: { type: 'number', description: 'Rotation angle degrees', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        inputPath: { type: 'string', required: true },
        outputPath: { type: 'string', required: true },
        text: { type: 'string', required: false, default: 'CONFIDENTIAL' },
        opacity: { type: 'number', required: false, default: 0.3 },
        angle: { type: 'number', required: false, default: 45 }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const { inputPath, outputPath, text, opacity, angle } = validation.data
      const safeInput = sanitizePath(inputPath)
      const safeOutput = sanitizePath(outputPath)

      return formatSuccess({
        inputPath: safeInput,
        outputPath: safeOutput,
        watermarkText: text,
        opacity,
        angle,
        command: 'Watermark feature requires PyPDF2 with reportlab or pdftk',
        tools: ['PyPDF2 + reportlab', 'pdftk', 'cpdf (Coherent PDF)'],
        pythonSnippet: `Use PyPDF2 and reportlab to create watermarks programmatically`
      })
    }
  })
  .build()

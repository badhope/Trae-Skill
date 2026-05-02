import { createMCPServer } from '../../packages/core/mcp/builder'
import { validateParams, formatSuccess, formatError, safeExec, sanitizePath } from '../../packages/core/shared/utils'
import * as fs from 'fs/promises'

export default createMCPServer({
  name: 'academic-writing',
  version: '2.0.0',
  description: 'Professional Academic Writing Toolkit - Paper writing, citation management, literature search, BibTeX, LaTeX support, systematic review',
  author: 'MCP Expert Community',
  icon: '📝'
})

  .addTool({
    name: 'paper_structure_outline',
    description: 'Generate professional academic paper structure with IMRaD compliance',
    parameters: {
      domain: { type: 'string', description: 'Research domain: cs, physics, biology, medicine, social, engineering', required: true },
      paperType: { type: 'string', description: 'journal, conference, thesis, dissertation, review, book_chapter', required: false },
      targetVenue: { type: 'string', description: 'Target journal/conference name for specific guidelines', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        domain: { type: 'string', required: true, enum: ['cs', 'physics', 'biology', 'medicine', 'social', 'engineering'] },
        paperType: { type: 'string', required: false, default: 'journal', enum: ['journal', 'conference', 'thesis', 'dissertation', 'review', 'book_chapter'] },
        targetVenue: { type: 'string', required: false, default: '' }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const structures: Record<string, string[]> = {
        journal: [
          'Title Page (Running Head + Authors + Affiliations)',
          'Abstract (150-300 words, structured preferred)',
          'Keywords (5-8 terms, MeSH compliant if medical)',
          '1. Introduction',
          '2. Related Work / Background',
          '3. Methodology / Approach',
          '4. Experiments / Study Design',
          '5. Results',
          '6. Discussion',
          '7. Conclusion & Future Work',
          'Acknowledgements',
          'References',
          'Appendices (if required)'
        ],
        conference: [
          'Title & Authors',
          'Abstract',
          '1. Introduction',
          '2. Background & Motivation',
          '3. Proposed Approach / Method',
          '4. Experimental Evaluation',
          '5. Related Work',
          '6. Discussion',
          '7. Conclusion',
          'References'
        ],
        thesis: [
          'Title Page',
          'Abstract',
          'Table of Contents',
          'List of Figures/Tables',
          'Acknowledgements',
          'Chapter 1: Introduction & Problem Statement',
          'Chapter 2: Literature Review',
          'Chapter 3: Theoretical Framework',
          'Chapter 4: Methodology',
          'Chapter 5: Results & Analysis',
          'Chapter 6: Discussion',
          'Chapter 7: Conclusion & Implications',
          'Appendices',
          'Bibliography',
          'Curriculum Vitae'
        ],
        review: [
          'Title & Abstract (PRISMA compliant)',
          '1. Introduction & Research Questions',
          '2. Protocol & Registration',
          '3. Search Strategy',
          '4. Study Selection',
          '5. Quality Assessment',
          '6. Data Extraction & Synthesis',
          '7. Results & Meta-Analysis',
          '8. Critical Discussion',
          '9. Limitations & Future Directions',
          '10. Conclusion',
          'References',
          'Supplementary Materials'
        ]
      }

      const type = validation.data.paperType
      const structure = structures[type] || structures.journal

      return formatSuccess({
        configured: true,
        domain: validation.data.domain,
        paperType: type,
        targetVenue: validation.data.targetVenue,
        standardStructure: structure,
        imradCompliant: true,
        wordCountGuidance: {
          abstract: '150-300 words - max 250 words for most ACM/IEEE',
          introduction: '10-15% of total word count',
          methodology: '20-25% of total word count',
          results: '15-20% of total word count',
          discussion: '15-20% of total word count'
        },
        imradChecklist: [
          '✓ Introduction: What is the problem and why important?',
          '✓ Methods: What exactly did you do?',
          '✓ Results: What did you find?',
          '✓ Discussion: What do findings mean?'
        ],
        submissionChecklist: [
          'Word count within limits',
          'Reference style matches venue',
          'All tables/figures numbered and captioned',
          'Supplementary materials uploaded',
          'Conflict of interest statement',
          'Ethics approval included if applicable'
        ]
      })
    }
  })

  .addTool({
    name: 'citation_formatter',
    description: 'Format citations in major academic styles with BibTeX generation',
    parameters: {
      style: { type: 'string', description: 'apa7, ieee, mla9, chicago17, acm, harvard, vancouver, nature', required: true },
      authors: { type: 'string', description: 'Author names: "Last1, First1; Last2, First2"', required: true },
      title: { type: 'string', description: 'Paper/article title', required: true },
      venue: { type: 'string', description: 'Journal/Conference/Book name', required: true },
      year: { type: 'string', description: 'Publication year', required: true },
      volume: { type: 'string', description: 'Volume number', required: false },
      issue: { type: 'string', description: 'Issue number', required: false },
      pages: { type: 'string', description: 'Page range e.g., 100-115', required: false },
      doi: { type: 'string', description: 'DOI number', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        style: { type: 'string', required: true, enum: ['apa7', 'ieee', 'mla9', 'chicago17', 'acm', 'harvard', 'vancouver', 'nature'] },
        authors: { type: 'string', required: true },
        title: { type: 'string', required: true },
        venue: { type: 'string', required: true },
        year: { type: 'string', required: true },
        volume: { type: 'string', required: false, default: '' },
        issue: { type: 'string', required: false, default: '' },
        pages: { type: 'string', required: false, default: '' },
        doi: { type: 'string', required: false, default: '' }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const authorsList = validation.data.authors.split(';').map((a: string) => a.trim())
      const firstAuthorLast = authorsList[0].split(',')[0].trim()
      const year = validation.data.year
      const title = validation.data.title
      const venue = validation.data.venue
      const vol = validation.data.volume ? `, ${validation.data.volume}` : ''
      const iss = validation.data.issue ? `(${validation.data.issue})` : ''
      const pgs = validation.data.pages ? `: ${validation.data.pages}` : ''
      const doi = validation.data.doi ? ` https://doi.org/${validation.data.doi}` : ''

      const authorsFormatted = authorsList.length > 3
        ? `${firstAuthorLast} et al.`
        : authorsList.map((a: any) => a.split(',')[0].trim()).join(', ')

      const formats: Record<string, string> = {
        apa7: `${authorsFormatted} (${year}). ${title}. ${venue}${vol}${iss}${pgs}.${doi}`,
        ieee: `[1] ${authorsFormatted}, "${title}", ${venue}, vol. ${validation.data.volume || 'N/A'}, no. ${validation.data.issue || 'N/A'}, pp. ${validation.data.pages || 'N/A'}, ${year}.`,
        mla9: `${firstAuthorLast}, ${authorsList[0].split(',')[1]?.trim() || ''}, et al. "${title}." ${venue}${vol}${iss}, ${year}, pp. ${validation.data.pages || 'N/A'}.`,
        chicago17: `${authorsFormatted}. "${title}." ${venue}${vol}, no. ${iss} (${year}): ${pgs}.${doi}`,
        acm: `${firstAuthorLast} et al. ${year}. ${title}. In ${venue}. ${pgs}.${doi}`,
        harvard: `${firstAuthorLast}, ${year}. ${title}. ${venue}${vol}${iss}${pgs}.`,
        vancouver: `${firstAuthorLast}. ${title}. ${venue}. ${year}${vol}${iss}${pgs}.`,
        nature: `${authorsFormatted}. ${title}. ${venue} ${vol}${iss}, ${pgs} (${year}).`
      }

      const inTextFormats: Record<string, string> = {
        apa7: `(${firstAuthorLast} et al., ${year})`,
        ieee: '[1]',
        mla9: `(${firstAuthorLast} ${pgs.split('-')[0] || ''})`,
        chicago17: `(${firstAuthorLast} ${year})`,
        acm: `[${firstAuthorLast} et al. ${year}]`,
        harvard: `(${firstAuthorLast}, ${year})`,
        vancouver: '[1]',
        nature: `(${firstAuthorLast} ${year})`
      }

      return formatSuccess({
        style: validation.data.style,
        inTextCitation: inTextFormats[validation.data.style],
        bibliographyEntry: formats[validation.data.style],
        bibtex: `@article{${firstAuthorLast.toLowerCase()}${year},
  title     = {${title}},
  author    = {${authorsList.join(' and ')}},
  journal   = {${venue}},
  year      = {${year}},${validation.data.volume ? `
  volume    = {${validation.data.volume}},` : ''}${validation.data.issue ? `
  number    = {${validation.data.issue}},` : ''}${validation.data.pages ? `
  pages     = {${validation.data.pages}},` : ''}${validation.data.doi ? `
  doi       = {${validation.data.doi}},` : ''}
  timestamp = {${new Date().toISOString().split('T')[0]}}
}`,
        key: `${firstAuthorLast.toLowerCase()}${year}`,
        citationCount: authorsList.length,
        quickTools: [
          'zotero.org/save - Browser extension',
          'zbib.org - Paste DOI to generate citation',
          'libgen.is - Paper downloads'
        ]
      })
    }
  })

  .addTool({
    name: 'bibtex_manager',
    description: 'BibTeX file operations: parse, validate, clean, deduplicate, and merge',
    parameters: {
      action: { type: 'string', description: 'parse, validate, clean, deduplicate, merge, extract-keys', required: true },
      inputPath: { type: 'string', description: 'Path to .bib file', required: false },
      outputPath: { type: 'string', description: 'Output path for cleaned file', required: false },
      fieldsToRemove: { type: 'string', description: 'Comma-separated fields to remove: abstract,file,keywords', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        action: { type: 'string', required: true, enum: ['parse', 'validate', 'clean', 'deduplicate', 'merge', 'extract-keys'] },
        inputPath: { type: 'string', required: false, default: 'references.bib' },
        outputPath: { type: 'string', required: false, default: 'references_clean.bib' },
        fieldsToRemove: { type: 'string', required: false, default: 'abstract,file,keywords,annote,timestamp' }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const inputPath = sanitizePath(validation.data.inputPath)
      let entries: string[] = []
      let content = ''

      try {
        content = await fs.readFile(inputPath, 'utf8')
        entries = content.match(/@\w+\{[^@]+/g) || []
      } catch {
        // File doesn't exist, return template
      }

      const fieldsToRemove = validation.data.fieldsToRemove.split(',').map((f: string) => f.trim())
      let resultMessage = ''
      let cleanedContent = content

      if (validation.data.action === 'parse') {
        resultMessage = `Parsed ${entries.length} BibTeX entries successfully`
      } else if (validation.data.action === 'clean') {
        fieldsToRemove.forEach((field: string) => {
          const regex = new RegExp(`\\s*${field}\\s*=\\s*\\{[^}]*\\},?\\n?`, 'gi')
          cleanedContent = cleanedContent.replace(regex, '')
        })
        resultMessage = `Cleaned ${entries.length} entries, removed: ${fieldsToRemove.join(', ')}`
        if (validation.data.outputPath) {
          await fs.writeFile(sanitizePath(validation.data.outputPath), cleanedContent)
        }
      } else if (validation.data.action === 'deduplicate') {
        const uniqueKeys = new Set<string>()
        const uniqueEntries: string[] = []
        let dupCount = 0
        entries.forEach((entry) => {
          const keyMatch = entry.match(/@\w+\{([^,]+),/)
          if (keyMatch) {
            const key = keyMatch[1].toLowerCase()
            if (!uniqueKeys.has(key)) {
              uniqueKeys.add(key)
              uniqueEntries.push(entry)
            } else {
              dupCount++
            }
          }
        })
        resultMessage = `Removed ${dupCount} duplicate entries, ${uniqueEntries.length} remain`
        cleanedContent = uniqueEntries.join('\n\n')
      }

      return formatSuccess({
        action: validation.data.action,
        inputFile: inputPath,
        entriesFound: entries.length,
        result: resultMessage,
        outputFile: validation.data.outputPath,
        cleanedFields: fieldsToRemove,
        bestPractices: [
          '✓ Consistent key format: AuthorYearFirstWord (smith2023attention)',
          '✓ Include DOI for ALL entries - enables 1-click lookup',
          '✓ Remove abstract/file fields to reduce file size',
          '✓ Standardize conference/journal names',
          '✓ Use double braces for proper noun capitalization: {{CNN}}'
        ],
        recommendedTools: [
          'pip install bibtexparser - Python processing',
          'npm install -g bibtex-tidy - Interactive cleanup',
          'JabRef - Cross-platform GUI manager'
        ],
        exampleCleanEntry: '@article{smith2023attention,\n  title     = {{Attention Is All You Need}},\n  author    = {Smith, John and Johnson, Alice},\n  journal   = {NeurIPS},\n  year      = {2023},\n  doi       = {10.xxxx/xxxxx}\n}'
      })
    }
  })

  .addTool({
    name: 'systematic_review_protocol',
    description: 'Generate PRISMA-compliant systematic review protocol',
    parameters: {
      reviewType: { type: 'string', description: 'systematic, scoping, meta_analysis, umbrella', required: false },
      researchQuestions: { type: 'string', description: 'Pipe-separated PICO research questions', required: true },
      databases: { type: 'string', description: 'Comma-separated databases to search', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        reviewType: { type: 'string', required: false, default: 'systematic', enum: ['systematic', 'scoping', 'meta_analysis', 'umbrella'] },
        researchQuestions: { type: 'string', required: true },
        databases: { type: 'string', required: false, default: 'PubMed, Scopus, Web of Science, Embase, PsycINFO' }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const rqs = validation.data.researchQuestions.split('|').map((q: string) => q.trim())

      return formatSuccess({
        reviewType: validation.data.reviewType,
        prismaCompliant: true,
        registration: 'prospero.crd.york.ac.uk - Register before starting!',
        researchQuestions: rqs,
        databases: validation.data.databases.split(',').map((d: string) => d.trim()),
        prismaFlow: [
          '1. IDENTIFICATION: Database search + grey literature',
          '   n records after duplicates removed',
          '   ',
          '2. SCREENING: Title + Abstract screening',
          '   n excluded (provide reasons)',
          '   ',
          '3. ELIGIBILITY: Full-text review',
          '   n excluded with reasons',
          '   ',
          '4. INCLUDED: n studies in qualitative synthesis',
          '   n studies in quantitative synthesis (meta-analysis)'
        ],
        picoFramework: {
          P: 'Population/Participants - Who/what being studied',
          I: 'Intervention/Exposure - What being tested',
          C: 'Comparison - Control or comparator group',
          O: 'Outcomes - Primary and secondary measures'
        },
        searchStrategyExample: `# Example Boolean search string
# ("machine learning" OR "artificial intelligence") 
# AND ("healthcare" OR "clinical") 
# AND ("diagnosis" OR "prediction")
# AND ("randomized controlled trial")
# Filters: 2018-present, English only`,
        riskOfBiasTools: {
          RCT: 'Cochrane Risk of Bias tool 2.0',
          Observational: 'ROBINS-I',
          Diagnostic: 'QUADAS-2',
          Qualitative: 'CASP checklist'
        },
        extractionFields: [
          'Study ID, first author, year, country',
          'Study design, sample size',
          'Population characteristics',
          'Intervention details',
          'Outcome measures & effect sizes',
          'Funding source, conflicts of interest'
        ]
      })
    }
  })

  .addTool({
    name: 'latex_project_setup',
    description: 'Production LaTeX project setup with Makefile and CI/CD',
    parameters: {
      template: { type: 'string', description: 'acm, ieee, springer, elsevier, thesis, report', required: true },
      projectName: { type: 'string', description: 'Name of the LaTeX project', required: true },
      ciEnabled: { type: 'boolean', description: 'Add GitHub Actions CI', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        template: { type: 'string', required: true, enum: ['acm', 'ieee', 'springer', 'elsevier', 'thesis', 'report'] },
        projectName: { type: 'string', required: true },
        ciEnabled: { type: 'boolean', required: false, default: true }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const projectName = validation.data.projectName
      const template = validation.data.template

      const templates: Record<string, any> = {
        ieee: {
          documentClass: 'IEEEtran',
          classOptions: 'conference',
          packages: ['graphicx', 'amsmath', 'amssymb', 'algorithmic', 'algorithm'],
          bibStyle: 'IEEEtran'
        },
        acm: {
          documentClass: 'acmart',
          classOptions: 'sigconf,review',
          packages: ['graphicx', 'amsmath', 'algorithm', 'algpseudocode'],
          bibStyle: 'ACM-Reference-Format'
        },
        thesis: {
          documentClass: 'memoir',
          classOptions: 'a4paper,12pt,oneside',
          packages: ['graphicx', 'amsmath', 'amssymb', 'listings', 'glossaries'],
          bibStyle: 'apalike'
        }
      }

      const config = templates[template] || templates.ieee

      return formatSuccess({
        configured: true,
        projectName,
        template,
        folderStructure: [
          `${projectName}/`,
          '  main.tex',
          '  references.bib',
          '  sections/',
          '    01_introduction.tex',
          '    02_background.tex',
          '    03_methodology.tex',
          '    04_results.tex',
          '    05_discussion.tex',
          '  figures/',
          '  tables/',
          '  algorithms/',
          '  Makefile',
          '  .latexmkrc'
        ],
        latexmkConfig: `$pdf_mode = 1;
$bibtex_use = 2;
$pdflatex = 'pdflatex -interaction=nonstopmode -halt-on-error -shell-escape %O %S';
$clean_ext = "aux bbl blg log out toc lof lot brf fdb_latexmk fls synctex.gz";`,
        makefile: `NAME=main

default: compile

compile:
\tlatexmk -pdf $(NAME)

clean:
\tlatexmk -C

watch:
\tlatexmk -pdf -pvc $(NAME)
`,
        ciWorkflow: validation.data.ciEnabled ? `name: Build LaTeX
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: xu-cheng/latex-action@v3
        with:
          root_file: main.tex
      - uses: actions/upload-artifact@v4
        with:
          name: PDF
          path: main.pdf` : undefined,
        essentialPackages: [
          'geometry - Page layout',
          'graphicx - Figures',
          'booktabs - Professional tables',
          'amsmath/amssymb - Math',
          'hyperref - Links and bookmarks',
          'cleveref - Intelligent cross-referencing',
          'natbib/biblatex - References'
        ],
        compilationCommand: 'latexmk -pdf main.tex',
        dockerCommand: `docker run --rm -v $(pwd):/workdir texlive/texlive latexmk -pdf main.tex`
      })
    }
  })

  .addPrompt({
    name: 'research-paper-blueprint',
    description: 'Complete research paper writing blueprint with paragraph-by-paragraph guide',
    arguments: [{ name: 'venue', description: 'Target venue: nature, neurips, icml, acl, cvpr, general', required: true }],
    generate: async (args?: Record<string, any>) => {
      return `## 📚 Research Paper Writing Blueprint
**Target Venue**: ${args?.venue || 'General'}

---

### 🎯 Abstract Formula (150-250 words exactly)

**Sentence 1-2**: Context & Importance  
*"Deep learning has revolutionized X, achieving state-of-the-art on Y benchmarks."*

**Sentence 3**: Gap & Limitation  
*"However, current approaches fail when Z condition, limiting real-world deployment."*

**Sentence 4**: Our Solution  
*"This paper presents METHOD_NAME, a novel approach that..."*

**Sentence 5**: Key Results  
*"On DATASET, our method achieves +X% accuracy over baselines, while being Y× faster."*

**Sentence 6**: Impact  
*"These findings enable new applications in FIELD, providing a path toward..."*

---

### 📄 Introduction Structure (CCCC Framework)

**Paragraph 1: CONTEXT**
- Big picture importance
- Field-specific background
- Establishes significance

**Paragraph 2: CONTRAST**
- What we don't know
- Current limitations
- The critical gap

**Paragraph 3: CONSEQUENCES**
- Why gap matters
- Real-world impact
- Motivating examples

**Paragraph 4: CONTRIBUTION**
- Explicitly state contributions (3-5 bullet points)
- *"We make the following contributions:"*
- Each contribution should be verifiable

---

### ✅ The Three Golden Rules of Writing

1. **One idea per paragraph**
   - Topic sentence first
   - Support with evidence
   - Transition to next

2. **Show, don't tell**
   - ❌ Bad: "Our method is fast"
   - ✅ Good: "Our method runs in 5ms, 20× faster than baseline"

3. **Anticipate reviewer objections**
   - Address limitations upfront
   - Acknowledge concurrent work
   - Be transparent about failure cases

---

### 🎭 Reviewer Psychology

**Reviewer State on Paper Open**: Grumpy, tired, looking for excuse to reject

**Your Goals**:
1. Make contributions immediately obvious
2. No surprises - set correct expectations
3. Make it easy to find results
4. Pre-empt their favorite objections
5. Reference their work (genuinely)

---

### ✍️ Editing Checklist

- [ ] Abstract tells complete story standalone
- [ ] Every claim has citation or evidence
- [ ] All figures have descriptive captions
- [ ] Consistent tense (present for established facts, past for your work)
- [ ] No "future work" = laundry list (be specific)
- [ ] All baselines fairly implemented and cited`
    }
  })
  .build()

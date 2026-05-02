import { createMCPServer } from '../../packages/core/mcp/builder'
import { validateParams, formatSuccess, formatError, safeExecRaw, sanitizePath } from '../../packages/core/shared/utils'

export default createMCPServer({
  name: 'spreadsheet',
  version: '2.0.0',
  description: 'Professional Spreadsheet & Data Analysis Toolkit - CSV/Excel query, filter, transform, pivot, statistics, and format conversion',
  author: 'MCP Expert Community',
  icon: '📊'
})

  .addTool({
    name: 'csv_read_query',
    description: 'Read, filter, and query CSV files with SQL-like operations',
    parameters: {
      filePath: { type: 'string', description: 'Path to CSV file', required: true },
      delimiter: { type: 'string', description: 'Column delimiter: comma, tab, semicolon, pipe', required: false },
      limit: { type: 'number', description: 'Max rows to preview (default: 50)', required: false },
      selectColumns: { type: 'string', description: 'Comma-separated columns to SELECT', required: false },
      filterColumn: { type: 'string', description: 'Column name for WHERE filter', required: false },
      filterValue: { type: 'string', description: 'Filter value', required: false },
      filterOperator: { type: 'string', description: 'Operator: eq, neq, gt, lt, contains', required: false },
      sortBy: { type: 'string', description: 'Column to sort by', required: false },
      sortAscending: { type: 'boolean', description: 'Sort direction', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        filePath: { type: 'string', required: true },
        delimiter: { type: 'string', required: false, default: ',', enum: [',', ';', '\t', '|'] },
        limit: { type: 'number', required: false, default: 50 },
        selectColumns: { type: 'string', required: false, default: '' },
        filterColumn: { type: 'string', required: false, default: '' },
        filterValue: { type: 'string', required: false, default: '' },
        filterOperator: { type: 'string', required: false, default: 'eq', enum: ['eq', 'neq', 'gt', 'lt', 'gte', 'lte', 'contains'] },
        sortBy: { type: 'string', required: false, default: '' },
        sortAscending: { type: 'boolean', required: false, default: true }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const filePath = sanitizePath(validation.data.filePath)
      const delimiter = validation.data.delimiter
      const limit = validation.data.limit
      const selectCols = validation.data.selectColumns ? validation.data.selectColumns.split(',').map((c: string) => c.trim()).filter(Boolean) : []
      const filterCol = validation.data.filterColumn
      const filterVal = validation.data.filterValue
      const filterOp = validation.data.filterOperator
      const sortCol = validation.data.sortBy

      const pythonScript = `
import csv
import sys
from operator import itemgetter

csv.field_size_limit(sys.maxsize)

with open('${filePath.replace(/'/g, "\\'")}', 'r', encoding='utf-8-sig', errors='replace') as f:
    reader = csv.DictReader(f, delimiter='${delimiter}')
    fieldnames = reader.fieldnames or []
    rows = list(reader)

print(f"Total rows: {len(rows)}")
print(f"Columns ({len(fieldnames)}): {', '.join(fieldnames)}")
print()

filtered = rows
${filterCol && filterVal ? `
filtered = []
for r in rows:
    val = r.get('${filterCol}', '')
    filter_val = '${filterVal}'
    op_result = False
    if '${filterOp}' == 'eq':
        op_result = val == filter_val
    elif '${filterOp}' == 'neq':
        op_result = val != filter_val
    elif '${filterOp}' == 'gt':
        op_result = float(val) > float(filter_val) if val and filter_val else False
    elif '${filterOp}' == 'lt':
        op_result = float(val) < float(filter_val) if val and filter_val else False
    elif '${filterOp}' == 'contains':
        op_result = filter_val.lower() in val.lower()
    if op_result:
        filtered.append(r)
print(f"After filter: {len(filtered)} rows")
` : ''}

${sortCol ? `
filtered = [r for r in filtered if r.get('${sortCol}')]
filtered.sort(key=lambda x: x['${sortCol}'], reverse=${!validation.data.sortAscending})
print(f"Sorted by: ${sortCol} (${validation.data.sortAscending ? 'ASC' : 'DESC'})")
` : ''}

${selectCols.length > 0 ? `
cols = [c for c in ${JSON.stringify(selectCols)} if c in fieldnames]
result = []
for r in filtered[:${limit}]:
    result.append({c: r.get(c, '') for c in cols})
print(f"Selected columns: {cols}")
` : `
result = filtered[:${limit}]
`}

print()
print(f"Preview ({len(result)} rows):")
print("-" * 80)
for i, row in enumerate(result):
    print(f"{i+1:3d}: { {k: v[:50] + '...' if len(str(v)) > 50 else v for k, v in row.items()} }")
`
      const execResult = await safeExecRaw(`python -c "${pythonScript.replace(/"/g, '\\"')}"`, 30000)

      return formatSuccess({
        queried: true,
        filePath,
        delimiter,
        totalRows: execResult.stdout.match(/Total rows: (\d+)/)?.[1] || 'N/A',
        filteredRows: execResult.stdout.match(/After filter: (\d+) rows/)?.[1] || 'N/A',
        previewRows: limit,
        output: execResult.stdout,
        stderr: execResult.stderr,
        exitCode: execResult.exitCode,
        pythonCommand: 'pip install pandas openpyxl xlrd',
        tips: [
          'Use filterColumn + filterValue for SQL-like WHERE',
          'Use selectColumns to project specific fields',
          'Large files? Use qsv or duckdb CLI tools'
        ]
      })
    }
  })

  .addTool({
    name: 'csv_schema_analyzer',
    description: 'Analyze CSV schema, data types, null rates, and value distributions',
    parameters: {
      filePath: { type: 'string', description: 'Path to CSV file', required: true },
      sampleSize: { type: 'number', description: 'Rows to sample for type detection', required: false },
      detectNulls: { type: 'boolean', description: 'Calculate null rates', required: false },
      cardinality: { type: 'boolean', description: 'Calculate column cardinality', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        filePath: { type: 'string', required: true },
        sampleSize: { type: 'number', required: false, default: 10000 },
        detectNulls: { type: 'boolean', required: false, default: true },
        cardinality: { type: 'boolean', required: false, default: true }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const filePath = sanitizePath(validation.data.filePath)
      const sampleSize = validation.data.sampleSize

      const pythonScript = `
import csv
from collections import Counter

csv.field_size_limit(1000000000)

with open('${filePath.replace(/'/g, "\\'")}', 'r', encoding='utf-8-sig', errors='replace') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames or []
    rows = list(reader)[:${sampleSize}]

print("=" * 80)
print(f"CSV SCHEMA ANALYSIS - {len(rows)} rows sampled")
print("=" * 80)
print()

for col in fieldnames:
    values = [r.get(col, '') for r in rows]
    non_empty = [v for v in values if v and v.strip()]
    
    detected_type = 'string'
    try:
        floats = [float(v) for v in non_empty if v]
        all_int = all(f == int(f) for f in floats)
        detected_type = 'integer' if all_int else 'float'
    except:
        if set(''.join(non_empty)).issubset(set('01')) and len(non_empty) > 5:
            detected_type = 'boolean'
    
    null_rate = (len(values) - len(non_empty)) / len(values) * 100 if values else 0
    
    uniques = len(set(non_empty))
    card_pct = uniques / len(non_empty) * 100 if non_empty else 0
    
    top5 = Counter(v.strip() for v in non_empty if v.strip()).most_common(5)
    
    print(f"🔍 {col}")
    print(f"   Type:     {detected_type}")
    print(f"   Nulls:    {null_rate:.1f}%")
    print(f"   Cardinality: {uniques} unique ({card_pct:.1f}%)")
    print(f"   Top values: {dict(top5)}")
    print()

print("=" * 80)
print(f"Total columns: {len(fieldnames)}")
print(f"Estimated types: {sum(1 for c in Counter([detected_type]) for detected_type in ['string', 'integer', 'float'])}")
print("=" * 80)
`
      const execResult = await safeExecRaw(`python -c "${pythonScript.replace(/"/g, '\\"')}"`, 30000)

      return formatSuccess({
        analyzed: true,
        filePath,
        sampleRows: sampleSize,
        schemaOutput: execResult.stdout,
        warnings: execResult.stderr,
        recommendedTools: [
          'pandas-profiling / ydata-profiling - Full HTML report',
          'DuckDB - Fast SQL queries on CSV',
          'q - Text as Data (https://harelba.github.io/q/)'
        ],
        cleaningChecklist: [
          'Trim whitespace from all string fields',
          'Standardize date formats',
          'Handle sentinel values (NA, NULL, -1)',
          'Normalize categorical values'
        ]
      })
    }
  })

  .addTool({
    name: 'excel_workbook_explorer',
    description: 'Explore Excel workbook structure, sheets, and get detailed metadata',
    parameters: {
      filePath: { type: 'string', description: 'Path to XLSX/XLS file', required: true },
      listSheets: { type: 'boolean', description: 'List all worksheets', required: false },
      sheetInfo: { type: 'boolean', description: 'Get dimensions for each sheet', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        filePath: { type: 'string', required: true },
        listSheets: { type: 'boolean', required: false, default: true },
        sheetInfo: { type: 'boolean', required: false, default: true }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const filePath = sanitizePath(validation.data.filePath)

      const pythonScript = `
import pandas as pd
from openpyxl import load_workbook
from collections import OrderedDict

try:
    wb = load_workbook(filename='${filePath.replace(/'/g, "\\'")}', read_only=True, data_only=True)
    sheets = wb.sheetnames
    
    print("📊 EXCEL WORKBOOK ANALYSIS")
    print("=" * 60)
    print(f"File:          '${filePath}'")
    print(f"Sheets:        {len(sheets)}")
    print(f"Excel version: {wb.excel_base_date}")
    print()
    
    print("WORKSHEETS:")
    print("-" * 60)
    
    for i, sheet_name in enumerate(sheets, 1):
        ws = wb[sheet_name]
        dims = ws.dimensions if ws.dimensions else 'Empty'
        max_row = ws.max_row
        max_col = ws.max_column
        cell_count = max_row * max_col if max_row and max_col else 0
        
        hidden = " (HIDDEN)" if ws.sheet_state == 'hidden' else ""
        print(f"{i:2d}. 📄 {sheet_name}{hidden}")
        print(f"    Range:  {dims}")
        print(f"    Size:   {max_row:,d} rows × {max_col:,d} columns = {cell_count:,d} cells")
        print()
        
    wb.close()
        
except Exception as e:
    print(f"Using pandas fallback... (error: {e})")
    xl = pd.ExcelFile('${filePath.replace(/'/g, "\\'")}')
    for i, name in enumerate(xl.sheet_names, 1):
        df = xl.parse(name)
        print(f"{i:2d}. {name}: {len(df):,d} rows × {len(df.columns)} cols")
`
      const execResult = await safeExecRaw(`python -c "${pythonScript.replace(/"/g, '\\"')}"`, 60000)

      return formatSuccess({
        explored: true,
        filePath,
        workbookOutput: execResult.stdout,
        errors: execResult.stderr,
        requiredPackages: 'pip install openpyxl pandas xlrd',
        proTips: [
          'openpyxl for .xlsx, xlrd==1.2.0 for old .xls',
          'Use read_only=True for large files',
          'data_only=True gets calculated cell values'
        ]
      })
    }
  })

  .addTool({
    name: 'excel_sheet_reader',
    description: 'Read specific Excel sheet with filtering and preview',
    parameters: {
      filePath: { type: 'string', description: 'Path to XLSX file', required: true },
      sheetName: { type: 'string', description: 'Sheet name or 0-based index', required: false },
      headerRow: { type: 'number', description: 'Row index for column headers (0-based)', required: false },
      skipRows: { type: 'number', description: 'Rows to skip at start', required: false },
      limit: { type: 'number', description: 'Preview rows limit', required: false },
      outputFormat: { type: 'string', description: 'Output format: table, json, csv, markdown', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        filePath: { type: 'string', required: true },
        sheetName: { type: 'string', required: false, default: '0' },
        headerRow: { type: 'number', required: false, default: 0 },
        skipRows: { type: 'number', required: false, default: 0 },
        limit: { type: 'number', required: false, default: 30 },
        outputFormat: { type: 'string', required: false, default: 'table', enum: ['table', 'json', 'csv', 'markdown'] }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const filePath = sanitizePath(validation.data.filePath)
      const sheetArg = /^\d+$/.test(validation.data.sheetName) ? parseInt(validation.data.sheetName) : validation.data.sheetName
      const limit = validation.data.limit

      const pythonScript = `
import pandas as pd
import json
pd.options.display.width = 200
pd.options.display.max_columns = 20
pd.options.display.max_rows = ${limit}
pd.options.display.float_format = '{:.2f}'.format

df = pd.read_excel(
    '${filePath.replace(/'/g, "\\'")}',
    sheet_name=${typeof sheetArg === 'number' ? sheetArg : `'${sheetArg}'`},
    header=${validation.data.headerRow},
    skiprows=${validation.data.skipRows},
    dtype=str
)

print(f"Sheet shape: {len(df)} rows × {len(df.columns)} columns")
print(f"Columns: {list(df.columns)}")
print()
print("-" * 80)

${validation.data.outputFormat === 'json' ? `
result = df.head(${limit}).to_dict('records')
print(json.dumps(result, indent=2, ensure_ascii=False))
` : validation.data.outputFormat === 'markdown' ? `
print(df.head(${limit}).to_markdown(index=False))
` : validation.data.outputFormat === 'csv' ? `
print(df.head(${limit}).to_csv(index=False))
` : `
print(df.head(${limit}).to_string(index=False))
`}
`
      const execResult = await safeExecRaw(`python -c "${pythonScript.replace(/"/g, '\\"')}"`, 60000)

      return formatSuccess({
        readSuccess: true,
        filePath,
        sheetName: validation.data.sheetName,
        previewLimit: limit,
        dimensions: execResult.stdout.match(/Sheet shape: (\d+ rows × \d+ columns)/)?.[1] || 'N/A',
        output: execResult.stdout,
        stderr: execResult.stderr,
        conversionTip: 'Use df.to_csv("output.csv", index=False) to export to CSV'
      })
    }
  })

  .addTool({
    name: 'spreadsheet_converter',
    description: 'Convert between Excel, CSV, JSON, Parquet formats',
    parameters: {
      inputPath: { type: 'string', description: 'Input file path', required: true },
      outputPath: { type: 'string', description: 'Output file path', required: true },
      sheetName: { type: 'string', description: 'Sheet name for Excel input', required: false },
      overwrite: { type: 'boolean', description: 'Overwrite existing file', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        inputPath: { type: 'string', required: true },
        outputPath: { type: 'string', required: true },
        sheetName: { type: 'string', required: false, default: '0' },
        overwrite: { type: 'boolean', required: false, default: false }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const inputPath = sanitizePath(validation.data.inputPath)
      const outputPath = sanitizePath(validation.data.outputPath)
      const sheetArg = /^\d+$/.test(validation.data.sheetName) ? parseInt(validation.data.sheetName) : validation.data.sheetName

      const pythonScript = `
import pandas as pd
import os

input_ext = '${inputPath.split('.').pop()?.toLowerCase()}'
output_ext = '${outputPath.split('.').pop()?.toLowerCase()}'

print(f"Converting: {input_ext} -> {output_ext}")

if input_ext in ['xlsx', 'xls', 'xlsm']:
    df = pd.read_excel('${inputPath.replace(/'/g, "\\'")}', sheet_name=${typeof sheetArg === 'number' ? sheetArg : `'${sheetArg}'`})
elif input_ext == 'csv':
    df = pd.read_csv('${inputPath.replace(/'/g, "\\'")}', low_memory=False)
elif input_ext == 'json':
    df = pd.read_json('${inputPath.replace(/'/g, "\\'")}')
elif input_ext == 'parquet':
    df = pd.read_parquet('${inputPath.replace(/'/g, "\\'")}')
else:
    raise ValueError(f"Unsupported input: {input_ext}")

print(f"Loaded: {len(df)} rows × {len(df.columns)} columns")

if output_ext == 'csv':
    df.to_csv('${outputPath.replace(/'/g, "\\'")}', index=False, encoding='utf-8-sig')
elif output_ext in ['xlsx', 'xls']:
    df.to_excel('${outputPath.replace(/'/g, "\\'")}', index=False, engine='openpyxl')
elif output_ext == 'json':
    df.to_json('${outputPath.replace(/'/g, "\\'")}', orient='records', indent=2)
elif output_ext == 'parquet':
    df.to_parquet('${outputPath.replace(/'/g, "\\'")}', index=False)
else:
    raise ValueError(f"Unsupported output: {output_ext}")

print(f"✅ Saved: '${outputPath}'")
print(f"File size: {os.path.getsize('${outputPath.replace(/'/g, "\\'")}'):,} bytes")
`
      const execResult = await safeExecRaw(`python -c "${pythonScript.replace(/"/g, '\\"')}"`, 120000)

      return formatSuccess({
        converted: execResult.exitCode === 0,
        inputPath,
        outputPath,
        exitCode: execResult.exitCode,
        output: execResult.stdout,
        error: execResult.stderr,
        formatNotes: {
          '✅ CSV': 'Universal, compact',
          '✅ Parquet': 'Compressed, typed, fast',
          '✅ JSON': 'Hierarchical, web-friendly',
          '⚠️ XLSX': 'Excel compatibility only'
        },
        largeFiles: 'For 100MB+ files: use parquet + duckdb for analytics'
      })
    }
  })

  .addTool({
    name: 'data_pivot_summary',
    description: 'Create pivot table and summary statistics from CSV/Excel',
    parameters: {
      filePath: { type: 'string', description: 'Path to data file', required: true },
      indexCol: { type: 'string', description: 'Rows for pivot table', required: true },
      valueCol: { type: 'string', description: 'Value column to aggregate', required: true },
      columns: { type: 'string', description: 'Columns for pivot (optional)', required: false },
      aggFunc: { type: 'string', description: 'Aggregation: sum, mean, count, min, max', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        filePath: { type: 'string', required: true },
        indexCol: { type: 'string', required: true },
        valueCol: { type: 'string', required: true },
        columns: { type: 'string', required: false, default: '' },
        aggFunc: { type: 'string', required: false, default: 'sum', enum: ['sum', 'mean', 'count', 'min', 'max', 'median'] }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const filePath = sanitizePath(validation.data.filePath)
      const isExcel = /\.xlsx?$/i.test(filePath)

      const pythonScript = `
import pandas as pd
pd.options.display.width = 150
pd.options.display.float_format = '{:,.2f}'.format

${isExcel ? `df = pd.read_excel('${filePath.replace(/'/g, "\\'")}')` : `df = pd.read_csv('${filePath.replace(/'/g, "\\'")}', low_memory=False)`}

print(f"Dataset: {len(df)} rows")
print()

pivot = pd.pivot_table(
    df,
    index='${validation.data.indexCol}',
    ${validation.data.columns ? `columns='${validation.data.columns}',` : ''}
    values='${validation.data.valueCol}',
    aggfunc='${validation.data.aggFunc}',
    fill_value=0,
    margins=True,
    margins_name='TOTAL'
)

print("📊 PIVOT TABLE")
print("=" * 80)
print(pivot.to_string())
print()
print("=" * 80)
print(f"Index:     {validation.data.indexCol}")
print(f"Values:    {validation.data.valueCol} ({validation.data.aggFunc})")
${validation.data.columns ? `print(f"Columns:   {validation.data.columns}")` : ''}
`
      const execResult = await safeExecRaw(`python -c "${pythonScript.replace(/"/g, '\\"')}"`, 60000)

      return formatSuccess({
        pivotCreated: true,
        filePath,
        index: validation.data.indexCol,
        values: validation.data.valueCol,
        aggregation: validation.data.aggFunc,
        pivotOutput: execResult.stdout,
        stderr: execResult.stderr,
        tools: ['DuckDB CLI for SQL on files', 'qsv for fast CSV operations', 'VisiData for interactive terminal analysis']
      })
    }
  })

  .build()

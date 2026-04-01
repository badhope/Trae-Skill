---
name: data-visualizer
description: "Tier 2: Data visualization and dashboard creation. Charts, graphs, interactive dashboards from raw data. Keywords: data visualization, charts, dashboards, 数据可视化, 仪表盘"
layer: workflow
role: data-scientist
tier: 2
version: 5.0.0
architecture: handoff-chain
invokes:
  - etl
  - data-validation
  - documentation
tags:
  - data
  - visualization
  - charts
  - dashboards
  - analytics
---

# Data Visualizer

## Overview

Data visualization and interactive dashboard creation.

## Key Capabilities

- Data import and cleaning
- Automatic chart type selection
- Interactive visualization generation
- Dashboard layout design
- Real-time data streaming
- Export to multiple formats
- Storytelling with data

## Chart Types

- **Basic**: Bar, line, pie, scatter
- **Statistical**: Histogram, box plot, heatmap
- **Advanced**: Network, tree, sankey, chord
- **Geospatial**: Maps, choropleth, bubble maps
- **3D**: 3D scatter, surface, volume
- **Interactive**: Zoom, pan, filter, tooltip

## Tools & Libraries

- **Python**: Matplotlib, Seaborn, Plotly, Bokeh, Altair
- **JavaScript**: D3.js, Chart.js, ECharts, Recharts
- **BI Tools**: Tableau, Power BI, Looker
- **Web**: React + D3, Vue + ECharts

## Process Flow

1. **Import** - Load and parse data
2. **Clean** - Data cleaning and validation
3. **Analyze** - Understand data patterns
4. **Visualize** - Choose chart types and generate
5. **Design** - Layout and styling
6. **Interactive** - Add interactivity
7. **Export** - Save and share

## Example Usage

```
"Create a dashboard for my sales data"
"Visualize this CSV with interactive charts"
"Make a geospatial map of customer locations"
"Create an animated time-series visualization"
"Build a story with these data points"
```

## Features

- Auto-insight generation
- Anomaly detection highlighting
- Comparison views
- Drill-down capability
- Export to PNG, PDF, HTML
- Embeddable widgets
- Real-time updates

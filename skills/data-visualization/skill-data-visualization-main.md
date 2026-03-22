---
id: skill-data-visualization-main-v1
name: Data Visualization
summary: 数据可视化与图表生成指南
type: skill
category: data-visualization
tags: [visualization, charts, graphs, data, dashboard, reporting]
keywords: [可视化, 图表, 数据, 仪表盘, 报表]
intent: 提供数据可视化设计与实现指导，支持多种图表类型和交互功能
use_cases:
  - 需要创建数据仪表盘时
  - 需要生成报告图表时
  - 需要展示数据分析结果时
inputs:
  - name: chart_type
    type: string
    required: true
    description: 图表类型
  - name: data
    type: array
    required: true
    description: 数据集
  - name: options
    type: object
    required: false
    description: 图表配置选项
outputs:
  - name: chart_spec
    type: object
    description: 图表规格
  - name: code
    type: code
    description: 实现代码
prerequisites:
  - 了解目标可视化库
  - 准备好数据集
steps:
  - step: 1
    action: 选择合适的图表类型
  - step: 2
    action: 准备和清洗数据
  - step: 3
    action: 设计图表布局
  - step: 4
    action: 实现可视化代码
  - step: 5
    action: 添加交互功能
examples:
  - input: "chart_type: line, data: time_series_data, options: {title: Sales Trend}"
    output: "line chart implementation with proper axes and legend"
    notes: 展示折线图实现
related_skills:
  - skill-research-v1
  - skill-documentation-main-v1
related_prompts:
  - prompt-task-visualization-design-dashboard
  - prompt-task-visualization-create-real-time-chart
notes: |
  关键原则：
  - 选择正确的图表类型展示数据
  - 保持图表简洁清晰
  - 使用合适的颜色和标签
  - 确保可访问性
created: 2026-03-22
updated: 2026-03-22
version: 1.0.0
deprecated: false
---

# Data Visualization Skill

数据可视化与图表生成的完整指南。

## 图表类型选择

### 选择指南

| 数据关系 | 推荐图表 | 示例 |
|----------|----------|------|
| 趋势 | 折线图 | 股票价格、气温变化 |
| 比较 | 柱状图 | 月度销售额对比 |
| 比例 | 饼图/环形图 | 市场占有率 |
| 分布 | 直方图/箱线图 | 用户年龄分布 |
| 相关性 | 散点图 | 身高体重关系 |
| 地理 | 地图可视化 | 各省销售额 |
| 多维度 | 雷达图 | 产品特性对比 |

### 决策树

```markdown
## 图表选择决策树

开始
  │
  ├─► 数据是时间序列?
  │     └─ YES → 折线图 / 面积图
  │
  ├─► 需要比较分类?
  │     ├─ 比较大小 → 柱状图
  │     └─ 比较比例 → 堆叠柱状图
  │
  ├─► 需要显示部分与整体?
  │     └─ YES → 饼图 / 环形图
  │
  ├─► 需要显示分布?
  │     ├─ 单变量 → 直方图
  │     └─ 多变量 → 箱线图 / 散点图
  │
  └─► 需要地理信息?
        └─ YES → 地图可视化 / 热力图
```

## 常用图表实现

### 折线图

```python
import matplotlib.pyplot as plt
import pandas as pd

# 数据准备
data = {
    'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    'sales': [120, 145, 132, 178, 189, 210],
    'target': [130, 130, 130, 150, 150, 170]
}
df = pd.DataFrame(data)

# 创建图表
plt.figure(figsize=(10, 6))
plt.plot(df['month'], df['sales'], marker='o', linewidth=2, label='实际销售额')
plt.plot(df['month'], df['target'], linestyle='--', linewidth=2, label='目标额')

# 添加标签和样式
plt.title('月度销售趋势', fontsize=16, fontweight='bold')
plt.xlabel('月份', fontsize=12)
plt.ylabel('销售额 (万元)', fontsize=12)
plt.legend(loc='upper left')
plt.grid(True, alpha=0.3)

# 添加数据标签
for i, (x, y) in enumerate(zip(df['month'], df['sales'])):
    plt.annotate(f'{y}', (x, y), textcoords="offset points", 
                 xytext=(0,10), ha='center')

plt.tight_layout()
plt.show()
```

### 柱状图

```python
import matplotlib.pyplot as plt
import numpy as np

categories = ['Python', 'JavaScript', 'Java', 'C++', 'Go']
popularity = [28.5, 24.8, 21.2, 10.3, 9.2]

plt.figure(figsize=(10, 6))
colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))

bars = plt.bar(categories, popularity, color=colors, edgecolor='black')

# 添加数值标签
for bar, val in zip(bars, popularity):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f'{val}%', ha='center', va='bottom', fontsize=11)

plt.title('编程语言受欢迎程度', fontsize=16, fontweight='bold')
plt.xlabel('语言', fontsize=12)
plt.ylabel('使用率 (%)', fontsize=12)
plt.ylim(0, 35)
plt.tight_layout()
plt.show()
```

### 饼图

```python
import matplotlib.pyplot as plt

sizes = [35, 25, 20, 12, 8]
labels = ['电子', '服装', '食品', '家居', '其他']
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
explode = (0.05, 0, 0, 0, 0)

plt.figure(figsize=(10, 8))
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)

plt.title('商品类别销售占比', fontsize=16, fontweight='bold')
plt.axis('equal')
plt.tight_layout()
plt.show()
```

### 散点图

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
x = np.random.randn(100)
y = x * 0.8 + np.random.randn(100) * 0.3

plt.figure(figsize=(10, 8))
plt.scatter(x, y, alpha=0.6, s=50, c='steelblue', edgecolors='black')

# 添加趋势线
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
plt.plot(np.sort(x), p(np.sort(x)), "r--", linewidth=2, label='趋势线')

plt.title('X与Y的相关性分析', fontsize=16, fontweight='bold')
plt.xlabel('X', fontsize=12)
plt.ylabel('Y', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

## Web可视化 (ECharts)

```javascript
// ECharts 基础配置
const chart = echarts.init(document.getElementById('chart'));

// 折线图配置
const option = {
    title: {
        text: '用户增长趋势',
        left: 'center'
    },
    tooltip: {
        trigger: 'axis',
        formatter: '{b}: {c} 人'
    },
    legend: {
        data: ['新增用户', '活跃用户'],
        bottom: 0
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '10%',
        containLabel: true
    },
    xAxis: {
        type: 'category',
        data: ['1月', '2月', '3月', '4月', '5月', '6月']
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name: '新增用户',
            type: 'line',
            data: [120, 132, 101, 134, 90, 230],
            smooth: true,
            areaStyle: {
                color: 'rgba(58, 147, 221, 0.3)'
            }
        },
        {
            name: '活跃用户',
            type: 'line',
            data: [450, 432, 501, 534, 590, 630],
            smooth: true
        }
    ]
};

chart.setOption(option);

// 响应式
window.addEventListener('resize', () => chart.resize());
```

## 仪表盘设计

### 布局原则

```markdown
## 仪表盘布局模板

┌─────────────────────────────────────────────────────────┐
│  标题栏                                                   │
├─────────────────────────────────────────────────────────┤
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │
│ │   KPI卡片    │ │   KPI卡片    │ │   KPI卡片    │     │
│ │   销售额    │ │   订单数    │ │   转化率    │     │
│ └──────────────┘ └──────────────┘ └──────────────┘     │
├─────────────────────────────────────────────────────────┤
│ ┌────────────────────────────┐ ┌────────────────────┐ │
│ │                            │ │                    │ │
│ │        主图表              │ │      次要图表      │ │
│ │      (折线/柱状)          │ │      (饼图/雷达)   │ │
│ │                            │ │                    │ │
│ └────────────────────────────┘ └────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────┐ │
│ │                   详细数据表格                       │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘

## KPI卡片设计
- 大字号显示核心数值
- 使用对比色显示趋势
- 箭头指示增减
- 简短说明文字
```

### 颜色系统

```python
# 专业配色方案
COLOR_PALETTES = {
    'corporate': {
        'primary': '#1f77b4',    # 蓝色
        'secondary': '#ff7f0e',  # 橙色
        'success': '#2ca02c',    # 绿色
        'danger': '#d62728',     # 红色
        'neutral': '#7f7f7f'      # 灰色
    },
    'modern': {
        'primary': '#6366f1',    # 靛蓝
        'secondary': '#8b5cf6',  # 紫色
        'accent': '#06b6d4',     # 青色
        'success': '#10b981',    # 翠绿
        'warning': '#f59e0b',    # 琥珀
        'danger': '#ef4444'      # 红宝石
    },
    'dark': {
        'background': '#1a1a2e',
        'surface': '#16213e',
        'primary': '#0f3460',
        'accent': '#e94560',
        'text': '#eaeaea'
    }
}

# 渐变色方案
GRADIENTS = {
    'blue_cyan': ['#0066ff', '#00d4ff'],
    'purple_pink': ['#8b5cf6', '#ec4899'],
    'green_teal': ['#10b981', '#06b6d4']
}
```

## 数据清洗

```python
import pandas as pd
import numpy as np

def clean_chart_data(df, column_config):
    """清洗数据用于可视化"""
    df_clean = df.copy()
    
    for col, config in column_config.items():
        # 处理缺失值
        if config.get('fill_missing'):
            if config['fill_missing'] == 'mean':
                df_clean[col].fillna(df_clean[col].mean(), inplace=True)
            elif config['fill_missing'] == 'median':
                df_clean[col].fillna(df_clean[col].median(), inplace=True)
            elif config['fill_missing'] == 'zero':
                df_clean[col].fillna(0, inplace=True)
        
        # 处理异常值
        if config.get('remove_outliers'):
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            df_clean = df_clean[(df_clean[col] >= lower) & (df_clean[col] <= upper)]
        
        # 格式化
        if config.get('format'):
            df_clean[col] = df_clean[col].apply(config['format'])
    
    return df_clean

# 使用示例
column_config = {
    'sales': {
        'fill_missing': 'mean',
        'remove_outliers': True,
        'format': lambda x: f'{x:,.0f}'
    },
    'date': {
        'format': lambda x: pd.to_datetime(x).strftime('%Y-%m')
    }
}
```

## 交互功能

```javascript
// ECharts 交互功能

// 1. 数据区域缩放
dataZoom: [
    { type: 'slider', start: 0, end: 100 },
    { type: 'inside', start: 0, end: 100 }
]

// 2. 工具栏
toolbox: {
    feature: {
        dataZoom: { title: { zoom: '区域缩放', back: '还原' } },
        magicType: { type: ['line', 'bar', 'stack'] },
        restore: { title: '还原' },
        saveAsImage: { title: '保存图片' }
    }
}

// 3. 点击事件
chart.on('click', function(params) {
    console.log(params);
    // 根据点击的数据更新其他图表
    updateDetailChart(params.name);
});

// 4. 提示框
tooltip: {
    trigger: 'item',
    formatter: function(params) {
        return `${params.name}<br/>
                ${params.marker} ${params.seriesName}: ${params.value}`;
    }
}

// 5. 图例选择
legend: {
    selected: {
        '新增用户': true,
        '活跃用户': false
    }
}
```

## 可访问性

```markdown
## 数据可视化可访问性检查

### 颜色使用
- [ ] 不能仅依赖颜色传达信息
- [ ] 使用足够的颜色对比度 (WCAG AA)
- [ ] 提供文字标签
- [ ] 使用图案/纹理辅助

### 图表元素
- [ ] 图表有清晰的标题
- [ ] 轴标签清晰可读
- [ ] 图例易于理解
- [ ] 数据点有tooltip说明

### 响应式设计
- [ ] 在移动设备上正常显示
- [ ] 支持键盘导航
- [ ] 支持屏幕阅读器

### 性能优化
- [ ] 大数据集使用采样
- [ ] 使用canvas替代svg处理大数据
- [ ] 实现懒加载
```

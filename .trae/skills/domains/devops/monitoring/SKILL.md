---
name: monitoring
description: "System monitoring and alerting for application performance, errors, and metrics. Keywords: monitoring, alerting, observability, prometheus, grafana, 监控, 告警"
layer: domain
role: specialist
version: 2.0.0
domain: devops
languages:
  - yaml
  - promql
frameworks:
  - prometheus
  - grafana
  - alertmanager
invoked_by:
  - devops
  - kubernetes
  - performance-optimizer
capabilities:
  - metrics_collection
  - alert_configuration
  - dashboard_creation
  - incident_response
triggers:
  keywords:
    - monitoring
    - alerting
    - observability
    - prometheus
    - grafana
    - metrics
    - 监控
    - 告警
    - 可观测性
metrics:
  avg_execution_time: 5s
  success_rate: 0.95
  alert_accuracy: 0.90
---

# Monitoring

系统监控和告警，用于应用性能、错误和指标监控。

## 目的

提供全面的监控解决方案：
- 指标收集和存储
- 告警配置和管理
- 仪表板创建
- 事件响应

## 能力

- **指标收集**: 收集系统和应用指标
- **告警配置**: 配置告警规则和通知
- **仪表板创建**: 创建监控仪表板
- **事件响应**: 处理监控事件

## 监控架构

```
┌─────────────────────────────────────────┐
│            Monitoring Stack             │
├─────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │ Grafana │  │  Alert  │  │   Log   │ │
│  │Dashboard│  │ Manager │  │Aggr.    │ │
│  └─────────┘  └─────────┘  └─────────┘ │
├─────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │Prometheus│ │  Trace  │  │  Event  │ │
│  │  Store  │  │  Store  │  │  Store  │ │
│  └─────────┘  └─────────┘  └─────────┘ │
├─────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │ Agents  │  │ Exporter│  │  SDK    │ │
│  └─────────┘  └─────────┘  └─────────┘ │
└─────────────────────────────────────────┘
```

## 监控工具

### Prometheus

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - "alerts/*.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
  
  - job_name: 'application'
    static_configs:
      - targets: ['app:8080']
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Application Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{path}}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
            "legendFormat": "{{status}}"
          }
        ]
      },
      {
        "title": "Latency P99",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "p99"
          }
        ]
      }
    ]
  }
}
```

## 指标类型

### 1. 系统指标

| 指标 | 描述 | 告警阈值 |
|------|------|----------|
| CPU使用率 | CPU占用百分比 | > 80% |
| 内存使用率 | 内存占用百分比 | > 85% |
| 磁盘使用率 | 磁盘占用百分比 | > 90% |
| 网络IO | 网络吞吐量 | 根据基线 |

### 2. 应用指标

| 指标 | 描述 | 告警阈值 |
|------|------|----------|
| 请求率 | 每秒请求数 | 根据基线 |
| 错误率 | 错误请求比例 | > 1% |
| 延迟 | 响应时间 | P99 > 1s |
| 并发数 | 并发连接数 | 根据容量 |

### 3. 业务指标

| 指标 | 描述 | 告警阈值 |
|------|------|----------|
| 活跃用户 | 在线用户数 | 根据基线 |
| 订单量 | 订单数量 | 根据预期 |
| 转化率 | 转化百分比 | 根据目标 |

## 告警配置

### Prometheus告警规则

```yaml
# alerts/application.yml
groups:
  - name: application
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) 
          / sum(rate(http_requests_total[5m])) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }}"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "P99 latency is {{ $value }}s"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} is down"
```

### AlertManager配置

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/xxx'

route:
  group_by: ['alertname', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'team-notifications'
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty'
    - match:
        severity: warning
      receiver: 'slack'

receivers:
  - name: 'team-notifications'
    slack_configs:
      - channel: '#alerts'
        send_resolved: true

  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: 'xxx'
        severity: critical
```

## 应用集成

### Python (Prometheus Client)

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
from flask import Flask, request

app = Flask(__name__)

# 定义指标
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'path', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP Request Latency',
    ['method', 'path']
)

ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Active HTTP Requests',
    ['method', 'path']
)

@app.before_request
def before_request():
    ACTIVE_REQUESTS.labels(method=request.method, path=request.path).inc()

@app.after_request
def after_request(response):
    REQUEST_COUNT.labels(
        method=request.method,
        path=request.path,
        status=response.status_code
    ).inc()
    ACTIVE_REQUESTS.labels(method=request.method, path=request.path).dec()
    return response

@app.route('/api/users')
def get_users():
    with REQUEST_LATENCY.labels(method='GET', path='/api/users').time():
        # 处理请求
        return {'users': []}

if __name__ == '__main__':
    start_http_server(9090)  # 指标端点
    app.run()
```

### Node.js (Prom-client)

```javascript
const promClient = require('prom-client');
const express = require('express');

const app = express();

// 默认指标
promClient.collectDefaultMetrics();

// 自定义指标
const httpRequestDuration = new promClient.Histogram({
    name: 'http_request_duration_seconds',
    help: 'HTTP Request Duration',
    labelNames: ['method', 'path', 'status']
});

const httpRequestsTotal = new promClient.Counter({
    name: 'http_requests_total',
    help: 'Total HTTP Requests',
    labelNames: ['method', 'path', 'status']
});

// 中间件
app.use((req, res, next) => {
    const end = httpRequestDuration.startTimer();
    res.on('finish', () => {
        end({ method: req.method, path: req.path, status: res.statusCode });
        httpRequestsTotal.inc({ method: req.method, path: req.path, status: res.statusCode });
    });
    next();
});

// 指标端点
app.get('/metrics', async (req, res) => {
    res.set('Content-Type', promClient.register.contentType);
    res.send(await promClient.register.metrics());
});
```

## 事件响应

### 响应流程

```
告警触发 → 确认 → 调查 → 修复 → 复盘
```

### Runbook模板

```markdown
# Runbook: High Error Rate

## 告警信息
- 告警名称: HighErrorRate
- 严重程度: Critical
- 触发条件: 错误率 > 1% 持续5分钟

## 影响
- 用户请求失败
- 可能的数据不一致

## 调查步骤
1. 检查应用日志
   ```bash
   kubectl logs -l app=api --tail=100
   ```

2. 检查错误类型分布
   ```bash
   curl http://prometheus:9090/api/v1/query?query=rate(http_requests_total{status=~"5.."}[5m])
   ```

3. 检查依赖服务状态
   ```bash
   kubectl get pods -l app=database
   ```

## 缓解措施
1. 如果是数据库问题，考虑重启或扩容
2. 如果是代码问题，回滚到上一版本
3. 如果是流量问题，启用限流

## 升级联系人
- 一线: @oncall
- 二线: @team-lead
- 三线: @engineering-manager
```

## 最佳实践

1. **四黄金信号**: 延迟、流量、错误、饱和度
2. **告警分级**: Critical/Warning/Info
3. **避免告警疲劳**: 合理设置阈值
4. **文档化**: 为每个告警提供Runbook
5. **持续优化**: 定期审查告警规则

## 相关技能

- [kubernetes](../devops/kubernetes) - K8s编排
- [docker](../devops/docker) - Docker容器
- [ci-cd-pipeline](../devops/ci-cd-pipeline) - CI/CD流水线
- [performance-optimizer](../performance/performance-optimizer) - 性能优化

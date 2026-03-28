---
name: kubernetes
description: "Kubernetes orchestration for container deployment and scaling. Keywords: kubernetes, k8s, deployment, service, pod, 编排"
layer: domain
role: specialist
version: 2.0.0
domain: devops
languages:
  - yaml
frameworks:
  - kubernetes
  - helm
invoked_by:
  - coding-workflow
  - ci-cd-pipeline
capabilities:
  - deployment_management
  - service_configuration
  - scaling_strategies
  - resource_management
  - monitoring_setup
---

# Kubernetes

Kubernetes容器编排专家，专注于部署管理、服务配置和弹性伸缩。

## 适用场景

- 容器编排
- 微服务部署
- 自动扩缩容
- 滚动更新
- 服务发现

## 核心架构

### 1. Deployment配置

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
  labels:
    app: myapp
    version: v1
spec:
  replicas: 3
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app: myapp
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: myapp
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "3000"
    spec:
      serviceAccountName: myapp
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
        - name: app
          image: myapp:v1.0.0
          imagePullPolicy: Always
          ports:
            - name: http
              containerPort: 3000
              protocol: TCP
          env:
            - name: NODE_ENV
              value: "production"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: myapp-secrets
                  key: database-url
            - name: REDIS_URL
              valueFrom:
                configMapKeyRef:
                  name: myapp-config
                  key: redis-url
          envFrom:
            - configMapRef:
                name: myapp-config
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          livenessProbe:
            httpGet:
              path: /health/live
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /health/ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
          startupProbe:
            httpGet:
              path: /health/startup
              port: http
            initialDelaySeconds: 10
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 30
          volumeMounts:
            - name: config
              mountPath: /app/config
              readOnly: true
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: config
          configMap:
            name: myapp-config
        - name: tmp
          emptyDir: {}
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: myapp
                topologyKey: kubernetes.io/hostname
      tolerations:
        - key: "node-role.kubernetes.io/master"
          operator: "Exists"
          effect: "NoSchedule"
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
  namespace: production
data:
  redis-url: "redis://redis:6379"
  log-level: "info"
  max-connections: "100"
---
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
  namespace: production
type: Opaque
stringData:
  database-url: "postgresql://user:password@postgres:5432/mydb"
  jwt-secret: "your-jwt-secret"
```

### 2. Service配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
  namespace: production
  labels:
    app: myapp
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
    - name: http
      port: 80
      targetPort: http
      protocol: TCP
---
apiVersion: v1
kind: Service
metadata:
  name: myapp-headless
  namespace: production
spec:
  type: ClusterIP
  clusterIP: None
  selector:
    app: myapp
  ports:
    - port: 3000
      targetPort: http
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  namespace: production
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  tls:
    - hosts:
        - api.example.com
      secretName: myapp-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp
                port:
                  number: 80
```

### 3. 自动扩缩容

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "1000"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
        - type: Pods
          value: 2
          periodSeconds: 60
      selectPolicy: Min
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
        - type: Pods
          value: 4
          periodSeconds: 15
      selectPolicy: Max
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp
  namespace: production
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: myapp
```

### 4. Helm Chart

```yaml
# Chart.yaml
apiVersion: v2
name: myapp
description: A Helm chart for myapp
type: application
version: 1.0.0
appVersion: "1.0.0"

# values.yaml
replicaCount: 3

image:
  repository: myapp
  pullPolicy: Always
  tag: "latest"

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  create: true
  annotations: {}
  name: ""

podAnnotations: {}

podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000

securityContext:
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: api.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-tls
      hosts:
        - api.example.com

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

nodeSelector: {}
tolerations: []
affinity: {}

# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - containerPort: 3000
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
```

### 5. 常用命令

```bash
# 部署管理
kubectl apply -f deployment.yaml
kubectl rollout status deployment/myapp
kubectl rollout history deployment/myapp
kubectl rollout undo deployment/myapp
kubectl rollout undo deployment/myapp --to-revision=2

# 扩缩容
kubectl scale deployment myapp --replicas=5
kubectl autoscale deployment myapp --min=3 --max=10 --cpu-percent=70

# 调试
kubectl logs -f deployment/myapp
kubectl exec -it pod/myapp-xxx -- /bin/sh
kubectl describe pod myapp-xxx
kubectl get events --sort-by='.lastTimestamp'

# 资源查看
kubectl get all -n production
kubectl top pods
kubectl top nodes

# 配置管理
kubectl create configmap my-config --from-file=config.yaml
kubectl create secret generic my-secret --from-literal=key=value

# Helm操作
helm install myapp ./chart
helm upgrade myapp ./chart
helm rollback myapp 1
helm uninstall myapp
```

## 最佳实践

1. **资源限制**: 设置requests和limits
2. **健康检查**: 配置liveness/readiness探针
3. **安全配置**: 使用非root用户
4. **滚动更新**: 配置合理的更新策略
5. **监控告警**: 集成Prometheus
6. **日志收集**: 使用EFK/Loki

## 相关技能

- [docker](../docker) - Docker容器
- [ci-cd-pipeline](../ci-cd-pipeline) - CI/CD流水线
- [monitoring](../monitoring) - 监控告警

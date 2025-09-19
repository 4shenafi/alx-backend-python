# Django Messaging App - Kubernetes Deployment

This document provides comprehensive instructions for deploying the Django messaging application on Kubernetes with advanced deployment strategies.

## 📁 Project Structure

```
messaging_app/
├── kurbeScript              # Kubernetes cluster setup script
├── deployment.yaml          # Initial Django app deployment
├── blue_deployment.yaml     # Blue deployment (v2.0)
├── green_deployment.yaml    # Green deployment (v2.0)
├── kubeservice.yaml         # Blue-green service configuration
├── ingress.yaml             # Nginx ingress configuration
├── commands.txt             # Ingress setup commands
├── kubctl-0x01             # Scaling and load testing script
├── kubctl-0x02             # Blue-green deployment script
├── kubctl-0x03             # Rolling update script
└── KUBERNETES_README.md     # This documentation
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl installed and configured
- wrk (for load testing)

### 1. Setup Kubernetes Cluster

```bash
# Make script executable and run
chmod +x kurbeScript
./kurbeScript
```

This script will:
- Install minikube and kubectl if not present
- Start a local Kubernetes cluster
- Verify cluster status
- Show available pods

### 2. Deploy Django App

```bash
# Deploy the initial application
kubectl apply -f deployment.yaml

# Verify deployment
kubectl get pods
kubectl get services
```

### 3. Scale the Application

```bash
# Run scaling and load testing
chmod +x kubctl-0x01
./kubctl-0x01
```

This script will:
- Scale deployment to 3 replicas
- Verify multiple pods are running
- Perform load testing with wrk
- Monitor resource usage

### 4. Setup Ingress

```bash
# Install Nginx Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml

# Apply ingress configuration
kubectl apply -f ingress.yaml

# Follow commands in commands.txt for detailed setup
```

### 5. Blue-Green Deployment

```bash
# Deploy blue and green versions
chmod +x kubctl-0x02
./kubctl-0x02
```

This script will:
- Deploy blue version (current)
- Deploy green version (new)
- Apply blue-green services
- Check logs for errors
- Demonstrate traffic switching

### 6. Rolling Updates

```bash
# Apply rolling update to version 2.0
chmod +x kubctl-0x03
./kubctl-0x03
```

This script will:
- Apply updated deployment (v2.0)
- Monitor rollout progress
- Test app availability during update
- Verify no downtime

## 📋 Detailed Instructions

### Task 0: Kubernetes Cluster Setup

**File**: `kurbeScript`

**Features**:
- Automatic minikube and kubectl installation
- Cluster startup with optimal resources
- Cluster verification and status reporting
- Pod listing and system information

**Usage**:
```bash
./kurbeScript
```

### Task 1: Django App Deployment

**File**: `deployment.yaml`

**Components**:
- Django app deployment (2 replicas)
- MySQL database deployment
- ClusterIP services for internal communication
- Health checks and resource limits

**Features**:
- Environment variable configuration
- Liveness and readiness probes
- Resource requests and limits
- Automatic database migrations

### Task 2: Application Scaling

**File**: `kubctl-0x01`

**Features**:
- Scale deployment to 3 replicas
- Pod verification across nodes
- Load testing with wrk
- Resource monitoring
- Port forwarding for testing

**Load Testing**:
- 10s test: 2 threads, 10 connections
- 30s test: 4 threads, 20 connections
- 60s test: 8 threads, 50 connections

### Task 3: Ingress Configuration

**Files**: `ingress.yaml`, `commands.txt`

**Features**:
- Nginx Ingress Controller setup
- Multiple host routing
- Path-based routing (/api/, /admin/)
- SSL configuration
- Proxy settings optimization

**Hosts**:
- `messaging-app.local` - Main application
- `api.messaging-app.local` - API endpoints
- `blue.messaging-app.local` - Blue environment
- `green.messaging-app.local` - Green environment

### Task 4: Blue-Green Deployment

**Files**: `blue_deployment.yaml`, `green_deployment.yaml`, `kubeservice.yaml`, `kubctl-0x02`

**Strategy**:
- Blue deployment: Current version (v1.0)
- Green deployment: New version (v2.0)
- Traffic switching via service selectors
- Zero-downtime deployments

**Traffic Switching**:
```bash
# Switch to green
kubectl patch service messaging-app-blue-green-service -p '{"spec":{"selector":{"environment":"green"}}}'

# Switch to blue
kubectl patch service messaging-app-blue-green-service -p '{"spec":{"selector":{"environment":"blue"}}}'
```

### Task 5: Rolling Updates

**Files**: `blue_deployment.yaml` (updated), `kubctl-0x03`

**Features**:
- Rolling update to version 2.0
- Continuous availability testing
- Rollout status monitoring
- Downtime detection
- Automatic rollback on failure

**Update Strategy**:
- Max Unavailable: 25%
- Max Surge: 25%
- Rolling update with health checks

## 🔧 Configuration Details

### Environment Variables

```yaml
env:
- name: DEBUG
  value: "1"
- name: DJANGO_SETTINGS_MODULE
  value: "messaging_app.settings"
- name: SECRET_KEY
  value: "django-insecure-..."
- name: MYSQL_DATABASE
  value: "messaging_db"
- name: MYSQL_USER
  value: "messaging_user"
- name: MYSQL_PASSWORD
  value: "messaging_password"
- name: DB_HOST
  value: "mysql-service"
- name: DB_PORT
  value: "3306"
```

### Resource Limits

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Health Checks

```yaml
livenessProbe:
  httpGet:
    path: /
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

## 🧪 Testing and Monitoring

### Load Testing

The `kubctl-0x01` script includes comprehensive load testing:

```bash
# Basic connectivity test
curl -s --max-time 10 "http://localhost:8080"

# Load tests with different parameters
wrk -t2 -c10 -d10s --latency http://localhost:8080
wrk -t4 -c20 -d30s --latency http://localhost:8080
wrk -t8 -c50 -d60s --latency http://localhost:8080
```

### Availability Testing

The `kubctl-0x03` script monitors availability during rolling updates:

- Continuous HTTP requests during update
- Success/failure rate calculation
- Downtime detection and reporting
- Real-time availability percentage

### Resource Monitoring

```bash
# Node resource usage
kubectl top nodes

# Pod resource usage
kubectl top pods

# Detailed resource information
kubectl describe pods
```

## 🚨 Troubleshooting

### Common Issues

1. **Pods not starting**:
   ```bash
   kubectl describe pod <pod-name>
   kubectl logs <pod-name>
   ```

2. **Service not accessible**:
   ```bash
   kubectl get svc
   kubectl get endpoints
   ```

3. **Ingress not working**:
   ```bash
   kubectl get ingress
   kubectl describe ingress <ingress-name>
   kubectl logs -n ingress-nginx
   ```

4. **Database connection issues**:
   ```bash
   kubectl logs -l app=mysql
   kubectl exec -it <mysql-pod> -- mysql -u root -p
   ```

### Debug Commands

```bash
# Check cluster status
kubectl cluster-info
kubectl get nodes

# Check deployments
kubectl get deployments
kubectl describe deployment <deployment-name>

# Check services
kubectl get services
kubectl describe service <service-name>

# Check pods
kubectl get pods -o wide
kubectl describe pod <pod-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Check logs
kubectl logs <pod-name>
kubectl logs -f <pod-name>  # Follow logs
```

## 🔄 Deployment Strategies

### 1. Rolling Update (Default)
- Gradual replacement of pods
- Zero-downtime deployment
- Automatic rollback on failure
- Configurable update parameters

### 2. Blue-Green Deployment
- Two identical environments
- Instant traffic switching
- Easy rollback capability
- Full environment testing

### 3. Canary Deployment
- Gradual traffic shifting
- Risk mitigation
- A/B testing capability
- Performance monitoring

## 📊 Performance Optimization

### Resource Optimization
- CPU and memory requests/limits
- Horizontal Pod Autoscaling (HPA)
- Vertical Pod Autoscaling (VPA)
- Cluster autoscaling

### Network Optimization
- Service mesh (Istio)
- Load balancing strategies
- Connection pooling
- CDN integration

### Storage Optimization
- Persistent volumes
- Storage classes
- Backup strategies
- Data replication

## 🔐 Security Considerations

### Network Security
- Network policies
- Service mesh security
- TLS/SSL termination
- Firewall rules

### Application Security
- Secrets management
- RBAC configuration
- Pod security policies
- Image scanning

### Data Security
- Encryption at rest
- Encryption in transit
- Backup encryption
- Access controls

## 📈 Monitoring and Observability

### Metrics
- Prometheus integration
- Custom metrics
- Resource utilization
- Application metrics

### Logging
- Centralized logging
- Log aggregation
- Log analysis
- Alerting

### Tracing
- Distributed tracing
- Request tracking
- Performance analysis
- Error tracking

## 🎯 Best Practices

1. **Resource Management**
   - Set appropriate requests and limits
   - Monitor resource usage
   - Use horizontal pod autoscaling

2. **Health Checks**
   - Implement liveness and readiness probes
   - Use appropriate timeouts
   - Monitor probe success rates

3. **Deployment Strategy**
   - Choose appropriate deployment strategy
   - Test deployments in staging
   - Implement rollback procedures

4. **Security**
   - Use secrets for sensitive data
   - Implement network policies
   - Regular security updates

5. **Monitoring**
   - Implement comprehensive monitoring
   - Set up alerting
   - Regular performance reviews

## 🚀 Production Deployment

For production deployment, consider:

1. **High Availability**
   - Multi-zone deployment
   - Load balancer configuration
   - Database clustering

2. **Scalability**
   - Auto-scaling configuration
   - Resource optimization
   - Performance tuning

3. **Security**
   - Production secrets management
   - Network security policies
   - Regular security audits

4. **Monitoring**
   - Production monitoring setup
   - Alerting configuration
   - Log management

5. **Backup and Recovery**
   - Data backup strategies
   - Disaster recovery plans
   - Testing procedures

## 📚 Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Django on Kubernetes](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [Nginx Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)

---

**Note**: This setup is designed for learning and development purposes. For production use, additional security, monitoring, and operational considerations should be implemented.

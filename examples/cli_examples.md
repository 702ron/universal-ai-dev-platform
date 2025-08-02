# Universal AI Development Platform - CLI Examples

This document provides practical examples of using the Universal AI Development Platform CLI (`uai`) for common development tasks.

## 📋 Table of Contents

- [Basic Analysis](#basic-analysis)
- [Project Creation](#project-creation)
- [Enhancement Workflows](#enhancement-workflows)
- [Agent Orchestration](#agent-orchestration)
- [Industry Adaptation](#industry-adaptation)
- [Intelligence Insights](#intelligence-insights)
- [Advanced Usage](#advanced-usage)

## 🔍 Basic Analysis

### Analyze Any Project

```bash
# Quick analysis of current directory
uai analyze .

# Analyze specific project with comprehensive depth
uai analyze ./my-project --depth comprehensive

# Focus on specific areas
uai analyze ./my-project --focus security,performance

# Export results to file
uai analyze ./my-project --output analysis.json --format json
```

### Real-World Analysis Examples

```bash
# Analyze a React application
uai analyze ./my-react-app --focus performance,maintainability
# Output: Detects React patterns, suggests optimizations

# Analyze a Python API
uai analyze ./my-fastapi --focus security,architecture
# Output: Identifies API patterns, security recommendations

# Analyze a mobile app
uai analyze ./my-flutter-app --depth comprehensive
# Output: Mobile-specific insights, platform optimizations
```

## 🚀 Project Creation

### Web Applications

```bash
# Modern React application
uai create web-app my-saas \
  --tech-stack "react,typescript,node,postgresql" \
  --features "auth,payments,real-time" \
  --deployment "vercel"

# Vue.js application with authentication
uai create web-app my-vue-app \
  --tech-stack "vue,typescript,express,mongodb" \
  --features "auth,routing,testing"

# Next.js full-stack application
uai create web-app my-nextjs-app \
  --tech-stack "nextjs,prisma,postgresql" \
  --features "auth,api-routes,ssg,ssr"
```

### API Services

```bash
# FastAPI service with PostgreSQL
uai create api-service my-api \
  --tech-stack "fastapi,postgresql" \
  --features "auth,validation,documentation,monitoring"

# GraphQL API with Apollo
uai create api-service my-graphql-api \
  --tech-stack "nodejs,graphql,mongodb" \
  --features "graphql-playground,subscriptions,auth"

# Go microservice
uai create api-service my-go-service \
  --tech-stack "go,postgresql" \
  --features "auth,middleware,validation,testing"
```

### Mobile Applications

```bash
# React Native with Expo
uai create mobile-app my-mobile-app \
  --tech-stack "react-native,expo" \
  --features "navigation,auth,push-notifications,offline-support"

# Flutter cross-platform app
uai create mobile-app my-flutter-app \
  --tech-stack "flutter" \
  --features "navigation,auth,state-management,testing"

# Native iOS app
uai create mobile-app my-ios-app \
  --tech-stack "ios-native,swift" \
  --features "auth,coredata,push-notifications"
```

### AI/ML Projects

```bash
# PyTorch machine learning project
uai create ai-project ml-model \
  --tech-stack "pytorch,fastapi" \
  --features "data-processing,model-training,api-endpoints,monitoring"

# TensorFlow research project
uai create ai-project research-project \
  --tech-stack "tensorflow,jupyter" \
  --features "data-analysis,model-training,visualization"

# MLOps pipeline
uai create ai-project ml-pipeline \
  --tech-stack "pytorch,mlflow,docker" \
  --features "mlops,model-versioning,a-b-testing,monitoring"
```

## 🔧 Enhancement Workflows

### Add Capabilities to Existing Projects

```bash
# Add testing infrastructure
uai enhance ./my-project --add-capabilities "testing,ci-cd,coverage"

# Add monitoring and analytics
uai enhance ./my-project --add-capabilities "monitoring,analytics,logging"

# Migrate to TypeScript
uai enhance ./my-project --migrate-to "typescript"

# Add AI capabilities
uai enhance ./my-project --ai-enhance

# Comprehensive upgrade
uai enhance ./my-project --upgrade --add-capabilities "security,performance"
```

### Real-World Enhancement Examples

```bash
# Legacy JavaScript project
uai enhance ./legacy-app \
  --migrate-to "typescript" \
  --add-capabilities "testing,eslint,prettier" \
  --upgrade

# Add authentication to existing app
uai enhance ./my-app \
  --add-capabilities "auth,user-management,security"

# Modernize React app
uai enhance ./old-react-app \
  --upgrade \
  --add-capabilities "hooks,context,testing,performance"
```

## 🎭 Agent Orchestration

### Predefined Workflows

```bash
# Complete full-stack setup
uai orchestrate full-stack-setup --project ./my-app --agents 15

# Comprehensive security hardening
uai orchestrate security-hardening --project ./my-app --priority high

# Performance optimization workflow
uai orchestrate performance-optimization \
  --project ./my-app \
  --agents 10 \
  --monitoring

# Bug investigation with multiple agents
uai orchestrate bug-investigation \
  --project ./my-app \
  --priority critical \
  --dry-run
```

### Custom Workflows

```bash
# Custom development workflow
uai orchestrate custom \
  --project ./my-app \
  --workflow "api-development,testing,deployment" \
  --agents 8

# Parallel development tasks
uai orchestrate parallel \
  --project ./my-app \
  --tasks "backend,frontend,database" \
  --agents 12 \
  --monitoring
```

### Workflow Examples by Project Type

```bash
# E-commerce platform setup
uai orchestrate full-stack-setup \
  --project ./ecommerce \
  --agents 20 \
  --priority high

# Microservices migration
uai orchestrate microservices-migration \
  --project ./monolith \
  --agents 15 \
  --dry-run

# ML model deployment
uai orchestrate ml-deployment \
  --project ./ml-model \
  --agents 8 \
  --monitoring
```

## 🔄 Industry Adaptation

### Monitor AI Evolution

```bash
# Check adaptation status
uai adapt --status

# Check for new AI features
uai adapt --check-updates

# Force update to latest capabilities (use with caution)
uai adapt --force-update
```

### Adaptation Workflow

```bash
# Daily adaptation check
uai adapt --check-updates > daily-updates.log

# Weekly comprehensive update
uai adapt --status && uai adapt --check-updates

# Emergency feature integration
uai adapt --force-update --backup
```

## 🧠 Intelligence Insights

### Predictive Analysis

```bash
# Predict issues for next month
uai intelligence predict --focus performance --timeline 1month

# Learn from project patterns
uai intelligence learn --pattern-recognition

# Get optimization recommendations
uai intelligence optimize --focus "scalability,security"

# ML-powered insights
uai intelligence predict --ml-insights --timeline 3months
```

### Intelligence Examples

```bash
# Performance prediction
uai intelligence predict \
  --focus performance \
  --timeline 1week \
  --ml-insights

# Security analysis
uai intelligence analyze \
  --focus security \
  --depth comprehensive

# Architecture optimization
uai intelligence optimize \
  --focus architecture \
  --timeline current
```

## 🚀 Advanced Usage

### Chaining Commands

```bash
# Analyze, enhance, and orchestrate
uai analyze ./project --format json > analysis.json && \
uai enhance ./project --add-capabilities "testing,security" && \
uai orchestrate feature-development --project ./project

# Daily workflow
uai adapt --check-updates && \
uai intelligence predict --timeline 1week && \
uai analyze ./current-project --depth standard
```

### Batch Operations

```bash
# Analyze multiple projects
for project in ./projects/*/; do
  uai analyze "$project" --output "${project}/analysis.json"
done

# Enhance all JavaScript projects
find . -name "package.json" -exec dirname {} \; | \
while read project; do
  uai enhance "$project" --migrate-to "typescript"
done
```

### Configuration and Automation

```bash
# Set up environment
export UAI_MAX_AGENTS=20
export UAI_AUTO_ADAPTATION=false
export UAI_ANALYSIS_DEPTH=comprehensive

# Automated daily checks
echo "0 9 * * * uai adapt --check-updates" | crontab -

# CI/CD integration
uai analyze . --format json --output ci-analysis.json
uai orchestrate health-check --project . --priority normal
```

### Real-World Scenarios

#### Scenario 1: Legacy Modernization

```bash
# 1. Analyze legacy application
uai analyze ./legacy-app --depth comprehensive --output legacy-analysis.json

# 2. Create modernization plan
uai intelligence optimize --focus "architecture,maintainability"

# 3. Gradual migration
uai enhance ./legacy-app --migrate-to "typescript" --add-capabilities "testing"

# 4. Monitor progress
uai orchestrate modernization-tracking --project ./legacy-app
```

#### Scenario 2: Startup MVP Development

```bash
# 1. Create MVP quickly
uai create web-app startup-mvp \
  --tech-stack "nextjs,supabase" \
  --features "auth,database,api" \
  --deployment "vercel"

# 2. Rapid development cycle
uai orchestrate feature-development --project ./startup-mvp --agents 10

# 3. Monitor and optimize
uai intelligence predict --focus performance --timeline 1month
```

#### Scenario 3: Enterprise Platform

```bash
# 1. Comprehensive analysis
uai analyze ./enterprise-platform --depth comprehensive --focus "security,scalability"

# 2. Security hardening
uai orchestrate security-hardening --project ./enterprise-platform --priority critical

# 3. Performance optimization
uai orchestrate performance-optimization --project ./enterprise-platform --agents 15

# 4. Continuous monitoring
uai adapt --status && uai intelligence monitor --focus "security,performance"
```

## 📚 Additional Resources

- **Getting Started**: See `docs/GETTING_STARTED.md`
- **Development Guide**: See `docs/DEVELOPMENT.md`
- **API Reference**: See `docs/api-reference.md`
- **Examples**: See `examples/` directory
- **Templates**: See `templates/` directory

## 🆘 Help and Support

```bash
# General help
uai --help

# Command-specific help
uai analyze --help
uai create --help
uai orchestrate --help

# List available options
uai create --list-types
uai orchestrate --list-workflows
```

---

**Happy coding with the Universal AI Development Platform! 🎉**
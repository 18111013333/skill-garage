/**
 * 控制层性能升级
 * 
 * 优化监控告警和自动降级
 */

// ==================== 性能监控器 ====================
class PerformanceMonitor {
  constructor(options = {}) {
    this.metrics = new Map();
    this.thresholds = {
      responseTime: options.responseTimeThreshold || 10000, // 10秒
      memoryUsage: options.memoryThreshold || 0.8, // 80%
      cpuUsage: options.cpuThreshold || 0.8, // 80%
      errorRate: options.errorRateThreshold || 0.1 // 10%
    };
    this.alerts = [];
    this.maxAlerts = options.maxAlerts || 100;
    this.monitoringInterval = null;
  }

  /**
   * 记录指标
   */
  recordMetric(name, value) {
    if (!this.metrics.has(name)) {
      this.metrics.set(name, {
        values: [],
        total: 0,
        count: 0,
        min: Infinity,
        max: -Infinity
      });
    }

    const metric = this.metrics.get(name);
    metric.values.push({ value, timestamp: Date.now() });
    metric.total += value;
    metric.count++;
    metric.min = Math.min(metric.min, value);
    metric.max = Math.max(metric.max, value);

    // 只保留最近 100 个值
    if (metric.values.length > 100) {
      metric.values.shift();
    }

    // 检查阈值
    this.checkThreshold(name, value);
  }

  /**
   * 检查阈值
   */
  checkThreshold(name, value) {
    const threshold = this.thresholds[name];
    if (!threshold) return;

    if (value > threshold) {
      this.addAlert(name, value, threshold);
    }
  }

  /**
   * 添加告警
   */
  addAlert(name, value, threshold) {
    const alert = {
      name,
      value,
      threshold,
      timestamp: Date.now(),
      message: `${name} 超过阈值: ${value} > ${threshold}`
    };

    this.alerts.push(alert);

    // 只保留最近的告警
    if (this.alerts.length > this.maxAlerts) {
      this.alerts.shift();
    }

    console.warn(`[PerformanceMonitor] ${alert.message}`);
  }

  /**
   * 获取指标统计
   */
  getMetricStats(name) {
    const metric = this.metrics.get(name);
    if (!metric) return null;

    return {
      name,
      avg: metric.total / metric.count,
      min: metric.min,
      max: metric.max,
      count: metric.count,
      latest: metric.values[metric.values.length - 1]?.value
    };
  }

  /**
   * 获取所有指标
   */
  getAllMetrics() {
    const stats = {};
    for (const name of this.metrics.keys()) {
      stats[name] = this.getMetricStats(name);
    }
    return stats;
  }

  /**
   * 获取告警
   */
  getAlerts(limit = 10) {
    return this.alerts.slice(-limit);
  }

  /**
   * 清除告警
   */
  clearAlerts() {
    this.alerts = [];
  }

  /**
   * 启动监控
   */
  startMonitoring(interval = 60000) {
    this.monitoringInterval = setInterval(() => {
      // 记录系统指标
      const memUsage = process.memoryUsage();
      this.recordMetric('memoryUsage', memUsage.heapUsed / memUsage.heapTotal);
      this.recordMetric('heapUsed', memUsage.heapUsed);
    }, interval);
  }

  /**
   * 停止监控
   */
  stopMonitoring() {
    if (this.monitoringInterval) {
      clearInterval(this.monitoringInterval);
      this.monitoringInterval = null;
    }
  }

  /**
   * 获取状态
   */
  getStatus() {
    return {
      metrics: this.getAllMetrics(),
      alerts: this.alerts.length,
      thresholds: this.thresholds
    };
  }
}

// ==================== 自动降级管理器 ====================
class AutoDegradationManager {
  constructor(options = {}) {
    this.levels = {
      normal: { concurrent: 3, timeout: 120000, cacheTTL: 60000 },
      degraded: { concurrent: 2, timeout: 60000, cacheTTL: 30000 },
      critical: { concurrent: 1, timeout: 30000, cacheTTL: 10000 }
    };
    this.currentLevel = 'normal';
    this.degradationHistory = [];
    this.monitor = null;
  }

  /**
   * 设置监控器
   */
  setMonitor(monitor) {
    this.monitor = monitor;
  }

  /**
   * 检查并降级
   */
  checkAndDegrade() {
    if (!this.monitor) return;

    const alerts = this.monitor.getAlerts(5);
    const recentAlerts = alerts.filter(a => Date.now() - a.timestamp < 60000);

    if (recentAlerts.length >= 3) {
      this.degrade('critical');
    } else if (recentAlerts.length >= 1) {
      this.degrade('degraded');
    } else {
      this.upgrade();
    }
  }

  /**
   * 降级
   */
  degrade(level) {
    if (this.currentLevel === level) return;

    const previousLevel = this.currentLevel;
    this.currentLevel = level;

    this.degradationHistory.push({
      from: previousLevel,
      to: level,
      timestamp: Date.now()
    });

    console.warn(`[AutoDegradation] 降级: ${previousLevel} -> ${level}`);

    return this.levels[level];
  }

  /**
   * 升级
   */
  upgrade() {
    if (this.currentLevel === 'normal') return;

    const levelOrder = ['critical', 'degraded', 'normal'];
    const currentIndex = levelOrder.indexOf(this.currentLevel);
    const nextLevel = levelOrder[currentIndex + 1];

    if (nextLevel) {
      const previousLevel = this.currentLevel;
      this.currentLevel = nextLevel;

      this.degradationHistory.push({
        from: previousLevel,
        to: nextLevel,
        timestamp: Date.now()
      });

      console.log(`[AutoDegradation] 升级: ${previousLevel} -> ${nextLevel}`);
    }

    return this.levels[this.currentLevel];
  }

  /**
   * 获取当前配置
   */
  getCurrentConfig() {
    return {
      level: this.currentLevel,
      config: this.levels[this.currentLevel]
    };
  }

  /**
   * 获取历史
   */
  getHistory(limit = 10) {
    return this.degradationHistory.slice(-limit);
  }

  /**
   * 获取状态
   */
  getStatus() {
    return {
      currentLevel: this.currentLevel,
      currentConfig: this.levels[this.currentLevel],
      historyCount: this.degradationHistory.length
    };
  }
}

// ==================== 资源泄漏检测器 ====================
class ResourceLeakDetector {
  constructor(options = {}) {
    this.resources = new Map();
    this.leakThreshold = options.leakThreshold || 300000; // 5分钟
    this.checkInterval = null;
    this.leaks = [];
  }

  /**
   * 注册资源
   */
  register(id, type, metadata = {}) {
    this.resources.set(id, {
      type,
      metadata,
      createdAt: Date.now(),
      lastAccessed: Date.now()
    });
  }

  /**
   * 访问资源
   */
  access(id) {
    const resource = this.resources.get(id);
    if (resource) {
      resource.lastAccessed = Date.now();
    }
  }

  /**
   * 释放资源
   */
  release(id) {
    return this.resources.delete(id);
  }

  /**
   * 检测泄漏
   */
  detectLeaks() {
    const now = Date.now();
    const leaks = [];

    for (const [id, resource] of this.resources) {
      const idleTime = now - resource.lastAccessed;
      if (idleTime > this.leakThreshold) {
        leaks.push({
          id,
          type: resource.type,
          idleTime,
          createdAt: resource.createdAt
        });
      }
    }

    this.leaks = leaks;
    return leaks;
  }

  /**
   * 清理泄漏资源
   */
  cleanupLeaks() {
    const leaks = this.detectLeaks();
    let cleaned = 0;

    for (const leak of leaks) {
      if (this.resources.delete(leak.id)) {
        cleaned++;
      }
    }

    return cleaned;
  }

  /**
   * 启动定期检测
   */
  startDetection(interval = 300000) {
    this.checkInterval = setInterval(() => {
      const cleaned = this.cleanupLeaks();
      if (cleaned > 0) {
        console.log(`[ResourceLeakDetector] 清理了 ${cleaned} 个泄漏资源`);
      }
    }, interval);
  }

  /**
   * 停止检测
   */
  stopDetection() {
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
      this.checkInterval = null;
    }
  }

  /**
   * 获取状态
   */
  getStatus() {
    return {
      totalResources: this.resources.size,
      leaks: this.leaks.length,
      leakTypes: this.leaks.reduce((acc, l) => {
        acc[l.type] = (acc[l.type] || 0) + 1;
        return acc;
      }, {})
    };
  }
}

// 导出
module.exports = {
  PerformanceMonitor,
  AutoDegradationManager,
  ResourceLeakDetector
};

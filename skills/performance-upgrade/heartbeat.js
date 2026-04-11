/**
 * HeartBeat 优化器
 * 
 * 优化 HeartBeat 机制，减少 AI 点数消耗
 */

// ==================== HeartBeat 优化器 ====================
class HeartbeatOptimizer {
  constructor(options = {}) {
    this.interval = options.interval || 60000; // 默认 1 分钟
    this.maxRetries = options.maxRetries || 3;
    this.timeout = options.timeout || 5000;
    
    this.callbacks = new Map();
    this.timer = null;
    this.stats = {
      totalBeats: 0,
      successfulBeats: 0,
      failedBeats: 0,
      skippedBeats: 0,
      savedTokens: 0
    };

    // 优化配置
    this.optimization = {
      skipIfIdle: true,        // 空闲时跳过
      batchCallbacks: true,    // 批量执行回调
      adaptiveInterval: true,  // 自适应间隔
      minInterval: 30000,      // 最小间隔 30 秒
      maxInterval: 300000      // 最大间隔 5 分钟
    };

    this.lastActivity = Date.now();
    this.isIdle = false;
  }

  /**
   * 注册回调
   */
  register(id, callback, options = {}) {
    this.callbacks.set(id, {
      callback,
      priority: options.priority || 0,
      lastRun: 0,
      runCount: 0,
      errorCount: 0
    });
  }

  /**
   * 注销回调
   */
  unregister(id) {
    this.callbacks.delete(id);
  }

  /**
   * 启动心跳
   */
  start() {
    if (this.timer) return;

    this.timer = setInterval(() => {
      this.beat();
    }, this.interval);

    console.log('[HeartbeatOptimizer] Started with interval:', this.interval);
  }

  /**
   * 停止心跳
   */
  stop() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }

  /**
   * 执行心跳
   */
  async beat() {
    this.stats.totalBeats++;

    // 检查是否空闲
    const idleTime = Date.now() - this.lastActivity;
    this.isIdle = idleTime > 60000; // 1 分钟无活动视为空闲

    // 空闲时跳过（优化点数消耗）
    if (this.optimization.skipIfIdle && this.isIdle) {
      this.stats.skippedBeats++;
      this.stats.savedTokens += this.estimateTokensPerBeat();
      
      // 自适应：延长间隔
      if (this.optimization.adaptiveInterval) {
        this.adjustInterval(true);
      }
      
      return;
    }

    // 执行回调
    try {
      await this.executeCallbacks();
      this.stats.successfulBeats++;
      
      // 自适应：恢复正常间隔
      if (this.optimization.adaptiveInterval) {
        this.adjustInterval(false);
      }
    } catch (error) {
      this.stats.failedBeats++;
      console.error('[HeartbeatOptimizer] Beat failed:', error.message);
    }
  }

  /**
   * 执行回调
   */
  async executeCallbacks() {
    // 按优先级排序
    const sorted = Array.from(this.callbacks.entries())
      .sort((a, b) => b[1].priority - a[1].priority);

    // 批量执行
    if (this.optimization.batchCallbacks) {
      const results = await Promise.allSettled(
        sorted.map(([id, item]) => this.executeOne(id, item))
      );

      for (const result of results) {
        if (result.status === 'rejected') {
          console.error('[HeartbeatOptimizer] Callback error:', result.reason);
        }
      }
    } else {
      // 顺序执行
      for (const [id, item] of sorted) {
        await this.executeOne(id, item);
      }
    }
  }

  /**
   * 执行单个回调
   */
  async executeOne(id, item) {
    const startTime = Date.now();

    try {
      await item.callback();
      item.lastRun = Date.now();
      item.runCount++;
      item.errorCount = 0;
    } catch (error) {
      item.errorCount++;
      throw error;
    }
  }

  /**
   * 调整间隔
   */
  adjustInterval(isIdle) {
    if (isIdle) {
      // 空闲时延长间隔
      this.interval = Math.min(
        this.interval * 1.5,
        this.optimization.maxInterval
      );
    } else {
      // 活跃时恢复正常间隔
      this.interval = Math.max(
        this.interval / 1.5,
        this.optimization.minInterval
      );
    }

    // 重启定时器
    this.stop();
    this.start();
  }

  /**
   * 记录活动
   */
  recordActivity() {
    this.lastActivity = Date.now();
    this.isIdle = false;
  }

  /**
   * 估算每次心跳消耗的 Token
   */
  estimateTokensPerBeat() {
    // 假设每次心跳消耗约 100 tokens
    return 100;
  }

  /**
   * 获取统计
   */
  getStats() {
    return {
      ...this.stats,
      currentInterval: this.interval,
      isIdle: this.isIdle,
      idleTime: Date.now() - this.lastActivity,
      registeredCallbacks: this.callbacks.size,
      savingsRate: this.stats.totalBeats > 0
        ? (this.stats.skippedBeats / this.stats.totalBeats * 100).toFixed(1) + '%'
        : '0%'
    };
  }

  /**
   * 重置统计
   */
  resetStats() {
    this.stats = {
      totalBeats: 0,
      successfulBeats: 0,
      failedBeats: 0,
      skippedBeats: 0,
      savedTokens: 0
    };
  }
}

// ==================== 轻量级心跳 ====================
class LightweightHeartbeat {
  constructor(options = {}) {
    this.interval = options.interval || 60000;
    this.callback = null;
    this.timer = null;
    this.lastBeat = 0;
    this.beatCount = 0;
  }

  /**
   * 设置回调
   */
  setCallback(callback) {
    this.callback = callback;
  }

  /**
   * 启动
   */
  start() {
    if (this.timer) return;

    this.timer = setInterval(() => {
      this.beat();
    }, this.interval);
  }

  /**
   * 停止
   */
  stop() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }

  /**
   * 执行心跳
   */
  async beat() {
    if (!this.callback) return;

    this.lastBeat = Date.now();
    this.beatCount++;

    try {
      await this.callback();
    } catch (error) {
      console.error('[LightweightHeartbeat] Error:', error.message);
    }
  }

  /**
   * 获取状态
   */
  getStatus() {
    return {
      running: this.timer !== null,
      interval: this.interval,
      lastBeat: this.lastBeat,
      beatCount: this.beatCount
    };
  }
}

// 导出
module.exports = {
  HeartbeatOptimizer,
  LightweightHeartbeat
};

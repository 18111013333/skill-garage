/**
 * 能力层性能升级
 * 
 * 优化并发控制和资源池
 */

// ==================== 信号量并发控制 ====================
class Semaphore {
  constructor(maxConcurrent = 3) {
    this.maxConcurrent = maxConcurrent;
    this.current = 0;
    this.queue = [];
    this.totalAcquired = 0;
    this.totalReleased = 0;
  }

  /**
   * 获取许可
   */
  async acquire() {
    if (this.current < this.maxConcurrent) {
      this.current++;
      this.totalAcquired++;
      return true;
    }

    // 等待释放
    return new Promise((resolve) => {
      this.queue.push(resolve);
    });
  }

  /**
   * 释放许可
   */
  release() {
    this.totalReleased++;
    
    if (this.queue.length > 0) {
      const next = this.queue.shift();
      next(true);
    } else {
      this.current--;
    }
  }

  /**
   * 使用许可执行任务
   */
  async withPermit(task) {
    await this.acquire();
    try {
      return await task();
    } finally {
      this.release();
    }
  }

  /**
   * 获取状态
   */
  getStatus() {
    return {
      current: this.current,
      maxConcurrent: this.maxConcurrent,
      waiting: this.queue.length,
      totalAcquired: this.totalAcquired,
      totalReleased: this.totalReleased
    };
  }
}

// ==================== 技能实例池 ====================
class SkillInstancePool {
  constructor(options = {}) {
    this.maxSize = options.maxSize || 10;
    this.pools = new Map();
    this.factoryRegistry = new Map();
  }

  /**
   * 注册技能工厂
   */
  register(skillName, factory) {
    this.factoryRegistry.set(skillName, factory);
    this.pools.set(skillName, {
      available: [],
      inUse: new Set(),
      maxSize: this.maxSize
    });
  }

  /**
   * 获取技能实例
   */
  acquire(skillName) {
    const pool = this.pools.get(skillName);
    if (!pool) return null;

    if (pool.available.length > 0) {
      const instance = pool.available.pop();
      pool.inUse.add(instance);
      return instance;
    }

    const factory = this.factoryRegistry.get(skillName);
    if (!factory) return null;

    const instance = factory();
    pool.inUse.add(instance);
    return instance;
  }

  /**
   * 释放技能实例
   */
  release(skillName, instance) {
    const pool = this.pools.get(skillName);
    if (!pool || !pool.inUse.has(instance)) return false;

    pool.inUse.delete(instance);
    pool.available.push(instance);
    return true;
  }

  /**
   * 获取状态
   */
  getStatus() {
    const status = {};
    for (const [name, pool] of this.pools) {
      status[name] = {
        available: pool.available.length,
        inUse: pool.inUse.size
      };
    }
    return status;
  }
}

// ==================== 上下文缓存池 ====================
class ContextCachePool {
  constructor(maxSize = 50) {
    this.maxSize = maxSize;
    this.contexts = new Map();
    this.lru = [];
  }

  /**
   * 获取上下文
   */
  get(sessionId) {
    const context = this.contexts.get(sessionId);
    if (!context) return null;

    // 更新 LRU
    this.lru = this.lru.filter(id => id !== sessionId);
    this.lru.push(sessionId);

    return context;
  }

  /**
   * 设置上下文
   */
  set(sessionId, context) {
    // 如果已存在，更新
    if (this.contexts.has(sessionId)) {
      this.contexts.set(sessionId, context);
      this.lru = this.lru.filter(id => id !== sessionId);
      this.lru.push(sessionId);
      return true;
    }

    // 如果超过最大大小，删除最久未使用的
    if (this.contexts.size >= this.maxSize) {
      const oldest = this.lru.shift();
      if (oldest) {
        this.contexts.delete(oldest);
      }
    }

    this.contexts.set(sessionId, context);
    this.lru.push(sessionId);
    return true;
  }

  /**
   * 删除上下文
   */
  delete(sessionId) {
    if (this.contexts.has(sessionId)) {
      this.contexts.delete(sessionId);
      this.lru = this.lru.filter(id => id !== sessionId);
      return true;
    }
    return false;
  }

  /**
   * 清空
   */
  clear() {
    this.contexts.clear();
    this.lru = [];
    return true;
  }

  /**
   * 获取状态
   */
  getStatus() {
    return {
      size: this.contexts.size,
      maxSize: this.maxSize
    };
  }
}

// ==================== 并发管理器 ====================
class ConcurrencyManager {
  constructor(maxConcurrent = 3) {
    this.semaphore = new Semaphore(maxConcurrent);
    this.skillPool = new SkillInstancePool();
    this.contextPool = new ContextCachePool();
    this.taskStats = {
      total: 0,
      completed: 0,
      failed: 0,
      timeout: 0
    };
  }

  /**
   * 执行任务（带并发控制）
   */
  async execute(task, options = {}) {
    const timeout = options.timeout || 120000; // 2分钟

    this.taskStats.total++;

    return this.semaphore.withPermit(async () => {
      const startTime = Date.now();

      try {
        // 设置超时
        const result = await Promise.race([
          task(),
          new Promise((_, reject) => {
            setTimeout(() => reject(new Error('Task timeout')), timeout);
          })
        ]);

        this.taskStats.completed++;
        return {
          success: true,
          result,
          duration: Date.now() - startTime
        };
      } catch (error) {
        if (error.message === 'Task timeout') {
          this.taskStats.timeout++;
        } else {
          this.taskStats.failed++;
        }

        return {
          success: false,
          error: error.message,
          duration: Date.now() - startTime
        };
      }
    });
  }

  /**
   * 获取完整状态
   */
  getFullStatus() {
    return {
      semaphore: this.semaphore.getStatus(),
      skillPool: this.skillPool.getStatus(),
      contextPool: this.contextPool.getStatus(),
      taskStats: this.taskStats
    };
  }
}

// 导出
module.exports = {
  Semaphore,
  SkillInstancePool,
  ContextCachePool,
  ConcurrencyManager
};

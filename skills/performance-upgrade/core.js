/**
 * 核心层性能升级
 * 
 * 优化启动速度和内存管理
 */

// ==================== 启动优化 ====================
class StartupOptimizer {
  constructor() {
    this.modules = new Map();
    this.loadedModules = new Set();
    this.initQueue = [];
  }

  /**
   * 注册模块（延迟加载）
   */
  register(name, loader, dependencies = []) {
    this.modules.set(name, {
      loader,
      dependencies,
      loaded: false,
      instance: null
    });
  }

  /**
   * 初始化核心模块（立即加载）
   */
  async initCore() {
    const startTime = Date.now();
    
    // 并行初始化无依赖的核心模块
    const coreModules = ['memory', 'config', 'logger'];
    await Promise.all(coreModules.map(name => this.load(name)));
    
    return {
      duration: Date.now() - startTime,
      loaded: this.loadedModules.size
    };
  }

  /**
   * 延迟初始化非核心模块
   */
  async initDeferred() {
    // 延迟 1 秒后初始化
    setTimeout(async () => {
      const deferredModules = ['skills', 'plugins', 'extensions'];
      await Promise.all(deferredModules.map(name => this.load(name)));
    }, 1000);
  }

  /**
   * 加载模块
   */
  async load(name) {
    const module = this.modules.get(name);
    if (!module || module.loaded) return module?.instance;

    // 先加载依赖
    for (const dep of module.dependencies) {
      await this.load(dep);
    }

    // 加载模块
    module.instance = await module.loader();
    module.loaded = true;
    this.loadedModules.add(name);

    return module.instance;
  }

  /**
   * 获取模块
   */
  get(name) {
    const module = this.modules.get(name);
    return module?.instance;
  }

  /**
   * 获取状态
   */
  getStatus() {
    return {
      total: this.modules.size,
      loaded: this.loadedModules.size,
      pending: this.modules.size - this.loadedModules.size
    };
  }
}

// ==================== 内存管理 ====================
class MemoryManager {
  constructor(options = {}) {
    this.maxHeapSize = options.maxHeapSize || 512 * 1024 * 1024; // 512MB
    this.gcThreshold = options.gcThreshold || 0.8; // 80%
    this.objectPools = new Map();
    this.weakRefs = new WeakMap();
    this.cleanupInterval = null;
  }

  /**
   * 创建对象池
   */
  createPool(name, factory, maxSize = 100) {
    const pool = {
      available: [],
      inUse: new Set(),
      factory,
      maxSize,
      created: 0,
      reused: 0
    };
    this.objectPools.set(name, pool);
    return pool;
  }

  /**
   * 获取对象
   */
  acquire(poolName) {
    const pool = this.objectPools.get(poolName);
    if (!pool) return null;

    if (pool.available.length > 0) {
      const obj = pool.available.pop();
      pool.inUse.add(obj);
      pool.reused++;
      return obj;
    }

    if (pool.created < pool.maxSize) {
      const obj = pool.factory();
      pool.inUse.add(obj);
      pool.created++;
      return obj;
    }

    return null;
  }

  /**
   * 释放对象
   */
  release(poolName, obj) {
    const pool = this.objectPools.get(poolName);
    if (!pool || !pool.inUse.has(obj)) return false;

    pool.inUse.delete(obj);
    
    // 重置对象状态
    if (typeof obj.reset === 'function') {
      obj.reset();
    }
    
    pool.available.push(obj);
    return true;
  }

  /**
   * 获取内存使用情况
   */
  getMemoryUsage() {
    const usage = process.memoryUsage();
    return {
      heapUsed: usage.heapUsed,
      heapTotal: usage.heapTotal,
      external: usage.external,
      rss: usage.rss,
      heapUsedPercent: (usage.heapUsed / usage.heapTotal * 100).toFixed(1) + '%'
    };
  }

  /**
   * 检查是否需要 GC
   */
  needGC() {
    const usage = this.getMemoryUsage();
    return usage.heapUsed / usage.heapTotal > this.gcThreshold;
  }

  /**
   * 触发 GC（如果可用）
   */
  triggerGC() {
    if (global.gc) {
      global.gc();
      return true;
    }
    return false;
  }

  /**
   * 启动定期清理
   */
  startCleanup(interval = 60000) {
    this.cleanupInterval = setInterval(() => {
      // 清理对象池
      for (const [name, pool] of this.objectPools) {
        // 保留一半的可用对象
        const keep = Math.floor(pool.available.length / 2);
        pool.available = pool.available.slice(0, keep);
      }

      // 检查是否需要 GC
      if (this.needGC()) {
        this.triggerGC();
      }
    }, interval);
  }

  /**
   * 停止定期清理
   */
  stopCleanup() {
    if (this.cleanupInterval) {
      clearInterval(this.cleanupInterval);
      this.cleanupInterval = null;
    }
  }

  /**
   * 获取状态
   */
  getStatus() {
    const pools = {};
    for (const [name, pool] of this.objectPools) {
      pools[name] = {
        available: pool.available.length,
        inUse: pool.inUse.size,
        created: pool.created,
        reused: pool.reused
      };
    }

    return {
      memory: this.getMemoryUsage(),
      pools
    };
  }
}

// 导出
module.exports = {
  StartupOptimizer,
  MemoryManager
};

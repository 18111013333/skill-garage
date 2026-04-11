/**
 * 智能层性能升级
 * 
 * 优化响应速度和缓存系统
 */

// ==================== 响应速度优化 ====================
class ResponseOptimizer {
  constructor(options = {}) {
    this.responseTimeout = options.responseTimeout || 3000; // 3秒
    this.partialResults = new Map();
    this.pendingRequests = new Map();
  }

  /**
   * 快速响应包装器
   */
  async quickResponse(requestId, task, options = {}) {
    const startTime = Date.now();
    const timeout = options.timeout || this.responseTimeout;

    // 如果任务可以快速完成，直接返回
    if (options.fast) {
      const result = await task();
      return {
        status: 'complete',
        result,
        duration: Date.now() - startTime
      };
    }

    // 对于长任务，先返回部分结果
    return new Promise((resolve) => {
      let completed = false;
      const partialResults = [];

      // 设置超时，超时后返回部分结果
      const timer = setTimeout(() => {
        if (!completed) {
          completed = true;
          resolve({
            status: 'partial',
            results: partialResults,
            message: '正在处理中，稍后返回完整结果...',
            duration: Date.now() - startTime
          });
        }
      }, timeout);

      // 执行任务
      task((result) => {
        if (completed) return;
        partialResults.push(result);
      }).then((finalResult) => {
        if (!completed) {
          completed = true;
          clearTimeout(timer);
          resolve({
            status: 'complete',
            result: finalResult,
            duration: Date.now() - startTime
          });
        }
      }).catch((error) => {
        if (!completed) {
          completed = true;
          clearTimeout(timer);
          resolve({
            status: 'error',
            error: error.message,
            results: partialResults,
            duration: Date.now() - startTime
          });
        }
      });
    });
  }

  /**
   * 分批返回结果
   */
  async *batchResults(requestId, items, processor, batchSize = 3) {
    for (let i = 0; i < items.length; i += batchSize) {
      const batch = items.slice(i, i + batchSize);
      const results = await Promise.all(batch.map(processor));
      yield {
        batch: Math.floor(i / batchSize) + 1,
        total: Math.ceil(items.length / batchSize),
        results,
        progress: Math.min(100, ((i + batchSize) / items.length * 100)).toFixed(0)
      };
    }
  }

  /**
   * 获取状态
   */
  getStatus() {
    return {
      pendingRequests: this.pendingRequests.size,
      partialResults: this.partialResults.size
    };
  }
}

// ==================== LRU 缓存 ====================
class LRUCache {
  constructor(options = {}) {
    this.maxSize = options.maxSize || 100;
    this.ttl = options.ttl || 60000; // 60秒
    this.cache = new Map();
    this.accessOrder = [];
    this.hits = 0;
    this.misses = 0;
    this.evictions = 0;
  }

  /**
   * 获取缓存
   */
  get(key) {
    const item = this.cache.get(key);

    if (!item) {
      this.misses++;
      return null;
    }

    // 检查是否过期
    if (Date.now() > item.expiry) {
      this.cache.delete(key);
      this.accessOrder = this.accessOrder.filter(k => k !== key);
      this.misses++;
      return null;
    }

    // 更新访问顺序
    this.accessOrder = this.accessOrder.filter(k => k !== key);
    this.accessOrder.push(key);

    this.hits++;
    return item.value;
  }

  /**
   * 设置缓存
   */
  set(key, value, customTtl) {
    // 如果已存在，先删除
    if (this.cache.has(key)) {
      this.cache.delete(key);
      this.accessOrder = this.accessOrder.filter(k => k !== key);
    }

    // 如果超过最大大小，删除最久未使用的
    if (this.cache.size >= this.maxSize) {
      const oldestKey = this.accessOrder.shift();
      if (oldestKey) {
        this.cache.delete(oldestKey);
        this.evictions++;
      }
    }

    this.cache.set(key, {
      value,
      expiry: Date.now() + (customTtl || this.ttl),
      createdAt: Date.now()
    });
    this.accessOrder.push(key);

    return true;
  }

  /**
   * 删除缓存
   */
  delete(key) {
    if (this.cache.has(key)) {
      this.cache.delete(key);
      this.accessOrder = this.accessOrder.filter(k => k !== key);
      return true;
    }
    return false;
  }

  /**
   * 清理过期缓存
   */
  cleanup() {
    const now = Date.now();
    let cleaned = 0;

    for (const [key, item] of this.cache) {
      if (now > item.expiry) {
        this.cache.delete(key);
        this.accessOrder = this.accessOrder.filter(k => k !== key);
        cleaned++;
      }
    }

    return cleaned;
  }

  /**
   * 清空缓存
   */
  clear() {
    this.cache.clear();
    this.accessOrder = [];
    return true;
  }

  /**
   * 获取状态
   */
  getStatus() {
    return {
      size: this.cache.size,
      maxSize: this.maxSize,
      hits: this.hits,
      misses: this.misses,
      evictions: this.evictions,
      hitRate: this.hits + this.misses > 0
        ? (this.hits / (this.hits + this.misses) * 100).toFixed(1) + '%'
        : '0%'
    };
  }

  /**
   * 获取热点数据
   */
  getHotKeys(limit = 10) {
    // 返回最近访问的 key
    return this.accessOrder.slice(-limit).reverse();
  }
}

// ==================== 智能缓存管理器 ====================
class SmartCacheManager {
  constructor() {
    this.caches = new Map();
    this.defaultConfig = {
      maxSize: 100,
      ttl: 60000
    };
  }

  /**
   * 创建命名缓存
   */
  createCache(name, config = {}) {
    const cache = new LRUCache({
      ...this.defaultConfig,
      ...config
    });
    this.caches.set(name, cache);
    return cache;
  }

  /**
   * 获取缓存
   */
  getCache(name) {
    return this.caches.get(name);
  }

  /**
   * 清理所有缓存
   */
  cleanupAll() {
    let total = 0;
    for (const cache of this.caches.values()) {
      total += cache.cleanup();
    }
    return total;
  }

  /**
   * 获取所有缓存状态
   */
  getAllStatus() {
    const status = {};
    for (const [name, cache] of this.caches) {
      status[name] = cache.getStatus();
    }
    return status;
  }
}

// 导出
module.exports = {
  ResponseOptimizer,
  LRUCache,
  SmartCacheManager
};

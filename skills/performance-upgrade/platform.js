/**
 * 平台层性能升级
 * 
 * 优化网络和连接管理
 */

// ==================== HTTP 连接池 ====================
class HTTPConnectionPool {
  constructor(options = {}) {
    this.maxConnections = options.maxConnections || 10;
    this.maxIdleTime = options.maxIdleTime || 30000; // 30秒
    this.connections = new Map();
    this.idleConnections = [];
    this.stats = {
      total: 0,
      active: 0,
      idle: 0,
      requests: 0
    };
  }

  /**
   * 获取连接
   */
  async acquire(host) {
    // 尝试从空闲连接中获取
    const idleIndex = this.idleConnections.findIndex(c => c.host === host);
    if (idleIndex !== -1) {
      const connection = this.idleConnections.splice(idleIndex, 1)[0];
      connection.lastUsed = Date.now();
      this.connections.set(connection.id, connection);
      this.stats.idle--;
      this.stats.active++;
      return connection;
    }

    // 创建新连接
    if (this.stats.total < this.maxConnections) {
      const connection = {
        id: `${host}-${Date.now()}`,
        host,
        createdAt: Date.now(),
        lastUsed: Date.now()
      };
      this.connections.set(connection.id, connection);
      this.stats.total++;
      this.stats.active++;
      return connection;
    }

    // 等待连接可用
    return new Promise((resolve) => {
      setTimeout(() => {
        this.acquire(host).then(resolve);
      }, 100);
    });
  }

  /**
   * 释放连接
   */
  release(connection) {
    if (!connection) return;

    this.connections.delete(connection.id);
    this.stats.active--;

    // 放入空闲池
    connection.lastUsed = Date.now();
    this.idleConnections.push(connection);
    this.stats.idle++;

    // 清理过期的空闲连接
    this.cleanupIdle();
  }

  /**
   * 清理过期空闲连接
   */
  cleanupIdle() {
    const now = Date.now();
    const expired = this.idleConnections.filter(
      c => now - c.lastUsed > this.maxIdleTime
    );

    for (const conn of expired) {
      const index = this.idleConnections.indexOf(conn);
      if (index !== -1) {
        this.idleConnections.splice(index, 1);
        this.stats.idle--;
        this.stats.total--;
      }
    }
  }

  /**
   * 获取状态
   */
  getStatus() {
    return {
      ...this.stats,
      connections: this.connections.size,
      idleConnections: this.idleConnections.length
    };
  }
}

// ==================== 请求合并器 ====================
class RequestCoalescer {
  constructor(options = {}) {
    this.windowMs = options.windowMs || 100; // 100ms 合并窗口
    this.maxBatchSize = options.maxBatchSize || 10;
    this.pendingRequests = new Map();
    this.batches = new Map();
    this.stats = {
      total: 0,
      coalesced: 0,
      batches: 0
    };
  }

  /**
   * 发送请求（自动合并）
   */
  async request(key, fetcher) {
    this.stats.total++;

    // 如果有相同的请求正在进行，复用
    if (this.pendingRequests.has(key)) {
      this.stats.coalesced++;
      return this.pendingRequests.get(key);
    }

    // 创建新请求
    const promise = fetcher();
    this.pendingRequests.set(key, promise);

    try {
      const result = await promise;
      return result;
    } finally {
      // 延迟删除，允许短时间内的重复请求复用
      setTimeout(() => {
        this.pendingRequests.delete(key);
      }, this.windowMs);
    }
  }

  /**
   * 批量请求
   */
  async batchRequest(keys, batchFetcher) {
    this.stats.batches++;

    const batchKey = keys.sort().join(',');
    if (this.pendingRequests.has(batchKey)) {
      return this.pendingRequests.get(batchKey);
    }

    const promise = batchFetcher(keys);
    this.pendingRequests.set(batchKey, promise);

    try {
      const result = await promise;
      return result;
    } finally {
      setTimeout(() => {
        this.pendingRequests.delete(batchKey);
      }, this.windowMs);
    }
  }

  /**
   * 获取状态
   */
  getStatus() {
    return {
      ...this.stats,
      pendingRequests: this.pendingRequests.size,
      coalesceRate: this.stats.total > 0
        ? (this.stats.coalesced / this.stats.total * 100).toFixed(1) + '%'
        : '0%'
    };
  }
}

// ==================== 响应压缩器 ====================
class ResponseCompressor {
  constructor(options = {}) {
    this.minSize = options.minSize || 1024; // 最小 1KB 才压缩
    this.level = options.level || 6; // 压缩级别 1-9
    this.stats = {
      total: 0,
      compressed: 0,
      savedBytes: 0
    };
  }

  /**
   * 压缩响应
   */
  async compress(data) {
    this.stats.total++;

    const jsonStr = JSON.stringify(data);
    const originalSize = Buffer.byteLength(jsonStr, 'utf8');

    if (originalSize < this.minSize) {
      return { compressed: false, data, originalSize };
    }

    // 使用 gzip 压缩（如果可用）
    try {
      const zlib = require('zlib');
      const compressed = await new Promise((resolve, reject) => {
        zlib.gzip(jsonStr, { level: this.level }, (err, result) => {
          if (err) reject(err);
          else resolve(result);
        });
      });

      const compressedSize = compressed.length;
      const savedBytes = originalSize - compressedSize;

      this.stats.compressed++;
      this.stats.savedBytes += savedBytes;

      return {
        compressed: true,
        data: compressed,
        originalSize,
        compressedSize,
        savedBytes,
        ratio: (savedBytes / originalSize * 100).toFixed(1) + '%'
      };
    } catch (error) {
      return { compressed: false, data, originalSize };
    }
  }

  /**
   * 解压响应
   */
  async decompress(compressed) {
    try {
      const zlib = require('zlib');
      const jsonStr = await new Promise((resolve, reject) => {
        zlib.gunzip(compressed, (err, result) => {
          if (err) reject(err);
          else resolve(result.toString());
        });
      });
      return JSON.parse(jsonStr);
    } catch (error) {
      return null;
    }
  }

  /**
   * 获取状态
   */
  getStatus() {
    return {
      ...this.stats,
      avgSavedBytes: this.stats.compressed > 0
        ? Math.round(this.stats.savedBytes / this.stats.compressed)
        : 0
    };
  }
}

// ==================== 连接管理器 ====================
class ConnectionManager {
  constructor(options = {}) {
    this.httpPool = new HTTPConnectionPool(options.httpPool);
    this.coalescer = new RequestCoalescer(options.coalescer);
    this.compressor = new ResponseCompressor(options.compressor);
    this.heartbeatInterval = options.heartbeatInterval || 30000;
    this.heartbeats = new Map();
  }

  /**
   * 发送请求
   */
  async request(url, options = {}) {
    const host = new URL(url).host;
    const connection = await this.httpPool.acquire(host);

    try {
      const result = await this.coalescer.request(url, async () => {
        // 实际发送请求
        const response = await fetch(url, options);
        return response.json();
      });

      return result;
    } finally {
      this.httpPool.release(connection);
    }
  }

  /**
   * 启动心跳
   */
  startHeartbeat(id, callback) {
    const timer = setInterval(callback, this.heartbeatInterval);
    this.heartbeats.set(id, timer);
  }

  /**
   * 停止心跳
   */
  stopHeartbeat(id) {
    const timer = this.heartbeats.get(id);
    if (timer) {
      clearInterval(timer);
      this.heartbeats.delete(id);
    }
  }

  /**
   * 获取完整状态
   */
  getFullStatus() {
    return {
      httpPool: this.httpPool.getStatus(),
      coalescer: this.coalescer.getStatus(),
      compressor: this.compressor.getStatus(),
      heartbeats: this.heartbeats.size
    };
  }
}

// 导出
module.exports = {
  HTTPConnectionPool,
  RequestCoalescer,
  ResponseCompressor,
  ConnectionManager
};

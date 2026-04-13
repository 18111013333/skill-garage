/**
 * Token 优化器
 * 
 * 优化 Token 消耗，降低 API 调用成本
 */

// ==================== Token 计数器 ====================
class TokenCounter {
  constructor() {
    this.stats = {
      total: 0,
      input: 0,
      output: 0,
      cached: 0,
      saved: 0
    };
    this.history = [];
    this.maxHistory = 1000;
  }

  /**
   * 记录 Token 使用
   */
  record(input, output, cached = 0) {
    const usage = {
      input,
      output,
      cached,
      total: input + output,
      saved: cached,
      timestamp: Date.now()
    };

    this.stats.total += usage.total;
    this.stats.input += input;
    this.stats.output += output;
    this.stats.cached += cached;
    this.stats.saved += cached;

    this.history.push(usage);
    if (this.history.length > this.maxHistory) {
      this.history.shift();
    }

    return usage;
  }

  /**
   * 获取统计
   */
  getStats() {
    return {
      ...this.stats,
      avgInput: this.history.length > 0
        ? Math.round(this.stats.input / this.history.length)
        : 0,
      avgOutput: this.history.length > 0
        ? Math.round(this.stats.output / this.history.length)
        : 0,
      savingsRate: this.stats.total > 0
        ? (this.stats.saved / (this.stats.total + this.stats.saved) * 100).toFixed(1) + '%'
        : '0%'
    };
  }

  /**
   * 获取最近使用
   */
  getRecent(limit = 10) {
    return this.history.slice(-limit);
  }

  /**
   * 重置统计
   */
  reset() {
    this.stats = {
      total: 0,
      input: 0,
      output: 0,
      cached: 0,
      saved: 0
    };
    this.history = [];
  }
}

// ==================== 上下文压缩器 ====================
class ContextCompressor {
  constructor(options = {}) {
    this.maxTokens = options.maxTokens || 4000;
    this.compressionRatio = options.compressionRatio || 0.5;
    this.strategies = {
      removeRedundancy: true,
      summarizeHistory: true,
      keepRecent: true,
      compressCode: true
    };
  }

  /**
   * 压缩上下文
   */
  compress(context) {
    const originalTokens = this.estimateTokens(context);
    
    if (originalTokens <= this.maxTokens) {
      return { compressed: context, originalTokens, compressedTokens: originalTokens };
    }

    let compressed = context;

    // 策略1: 移除冗余
    if (this.strategies.removeRedundancy) {
      compressed = this.removeRedundancy(compressed);
    }

    // 策略2: 压缩历史
    if (this.strategies.summarizeHistory && this.estimateTokens(compressed) > this.maxTokens) {
      compressed = this.summarizeHistory(compressed);
    }

    // 策略3: 保留最近
    if (this.strategies.keepRecent && this.estimateTokens(compressed) > this.maxTokens) {
      compressed = this.keepRecent(compressed);
    }

    // 策略4: 压缩代码
    if (this.strategies.compressCode && this.estimateTokens(compressed) > this.maxTokens) {
      compressed = this.compressCode(compressed);
    }

    const compressedTokens = this.estimateTokens(compressed);

    return {
      compressed,
      originalTokens,
      compressedTokens,
      savedTokens: originalTokens - compressedTokens,
      compressionRate: ((1 - compressedTokens / originalTokens) * 100).toFixed(1) + '%'
    };
  }

  /**
   * 移除冗余
   */
  removeRedundancy(text) {
    // 移除多余空行
    text = text.replace(/\n{3,}/g, '\n\n');
    // 移除行尾空格
    text = text.replace(/[ \t]+$/gm, '');
    // 移除重复空格
    text = text.replace(/ {2,}/g, ' ');
    return text;
  }

  /**
   * 压缩历史
   */
  summarizeHistory(text) {
    // 找到历史部分
    const historyMatch = text.match(/## 历史记录[\s\S]*?(?=##|$)/);
    if (historyMatch) {
      const history = historyMatch[0];
      const lines = history.split('\n');
      
      // 只保留标题和最近 5 条
      const headers = lines.filter(l => l.startsWith('#'));
      const recent = lines.slice(-5);
      const summarized = [...headers, ...recent].join('\n');
      
      text = text.replace(history, summarized);
    }
    return text;
  }

  /**
   * 保留最近
   */
  keepRecent(text) {
    const lines = text.split('\n');
    const targetLines = Math.floor(this.maxTokens / 4); // 大约每行 4 tokens
    
    if (lines.length > targetLines) {
      // 保留开头（标题和重要信息）和结尾（最近内容）
      const head = lines.slice(0, Math.floor(targetLines * 0.3));
      const tail = lines.slice(-Math.floor(targetLines * 0.7));
      text = [...head, '\n... (省略中间内容) ...\n', ...tail].join('\n');
    }
    
    return text;
  }

  /**
   * 压缩代码
   */
  compressCode(text) {
    // 移除代码注释
    text = text.replace(/\/\/.*$/gm, '');
    text = text.replace(/\/\*[\s\S]*?\*\//g, '');
    // 移除空行
    text = text.replace(/\n{2,}/g, '\n');
    return text;
  }

  /**
   * 估算 Token 数量
   */
  estimateTokens(text) {
    // 简单估算：英文约 4 字符 = 1 token，中文约 1.5 字符 = 1 token
    const chineseChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
    const otherChars = text.length - chineseChars;
    return Math.ceil(chineseChars / 1.5 + otherChars / 4);
  }
}

// ==================== 提示词优化器 ====================
class PromptOptimizer {
  constructor() {
    this.templates = new Map();
    this.shortcuts = new Map();
    this.stats = {
      optimized: 0,
      savedTokens: 0
    };
  }

  /**
   * 注册模板
   */
  registerTemplate(name, template, variables = []) {
    this.templates.set(name, { template, variables });
  }

  /**
   * 注册快捷方式
   */
  registerShortcut(shortcut, expansion) {
    this.shortcuts.set(shortcut, expansion);
  }

  /**
   * 优化提示词
   */
  optimize(prompt) {
    let optimized = prompt;
    let savedTokens = 0;

    // 应用快捷方式
    for (const [shortcut, expansion] of this.shortcuts) {
      if (optimized.includes(shortcut)) {
        const before = this.estimateTokens(optimized);
        optimized = optimized.replace(new RegExp(shortcut, 'g'), expansion);
        const after = this.estimateTokens(optimized);
        savedTokens += before - after;
      }
    }

    // 移除冗余
    optimized = this.removeRedundancy(optimized);

    // 压缩空格
    optimized = optimized.replace(/ {2,}/g, ' ');

    this.stats.optimized++;
    this.stats.savedTokens += savedTokens;

    return {
      optimized,
      originalTokens: this.estimateTokens(prompt),
      optimizedTokens: this.estimateTokens(optimized),
      savedTokens
    };
  }

  /**
   * 使用模板
   */
  useTemplate(name, values = {}) {
    const template = this.templates.get(name);
    if (!template) return null;

    let result = template.template;
    for (const [key, value] of Object.entries(values)) {
      result = result.replace(new RegExp(`\\{${key}\\}`, 'g'), value);
    }

    return result;
  }

  /**
   * 移除冗余
   */
  removeRedundancy(text) {
    return text
      .replace(/\n{3,}/g, '\n\n')
      .replace(/[ \t]+$/gm, '')
      .replace(/ {2,}/g, ' ');
  }

  /**
   * 估算 Token
   */
  estimateTokens(text) {
    const chineseChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
    const otherChars = text.length - chineseChars;
    return Math.ceil(chineseChars / 1.5 + otherChars / 4);
  }

  /**
   * 获取统计
   */
  getStats() {
    return {
      ...this.stats,
      templates: this.templates.size,
      shortcuts: this.shortcuts.size
    };
  }
}

// ==================== 响应缓存 ====================
class ResponseCache {
  constructor(options = {}) {
    this.maxSize = options.maxSize || 100;
    this.ttl = options.ttl || 3600000; // 1小时
    this.cache = new Map();
    this.lru = [];
    this.stats = {
      hits: 0,
      misses: 0,
      savedTokens: 0
    };
  }

  /**
   * 生成缓存键
   */
  generateKey(prompt, context = '') {
    const crypto = require('crypto');
    const content = prompt + context;
    return crypto.createHash('md5').update(content).digest('hex');
  }

  /**
   * 获取缓存
   */
  get(prompt, context = '') {
    const key = this.generateKey(prompt, context);
    const item = this.cache.get(key);

    if (!item) {
      this.stats.misses++;
      return null;
    }

    if (Date.now() > item.expiry) {
      this.cache.delete(key);
      this.lru = this.lru.filter(k => k !== key);
      this.stats.misses++;
      return null;
    }

    // 更新 LRU
    this.lru = this.lru.filter(k => k !== key);
    this.lru.push(key);

    this.stats.hits++;
    this.stats.savedTokens += item.tokens;

    return item.response;
  }

  /**
   * 设置缓存
   */
  set(prompt, response, tokens, context = '') {
    const key = this.generateKey(prompt, context);

    // 如果超过最大大小，删除最久未使用的
    if (this.cache.size >= this.maxSize) {
      const oldest = this.lru.shift();
      if (oldest) {
        this.cache.delete(oldest);
      }
    }

    this.cache.set(key, {
      response,
      tokens,
      expiry: Date.now() + this.ttl,
      createdAt: Date.now()
    });
    this.lru.push(key);

    return true;
  }

  /**
   * 清理过期
   */
  cleanup() {
    const now = Date.now();
    let cleaned = 0;

    for (const [key, item] of this.cache) {
      if (now > item.expiry) {
        this.cache.delete(key);
        this.lru = this.lru.filter(k => k !== key);
        cleaned++;
      }
    }

    return cleaned;
  }

  /**
   * 获取统计
   */
  getStats() {
    return {
      size: this.cache.size,
      maxSize: this.maxSize,
      ...this.stats,
      hitRate: this.stats.hits + this.stats.misses > 0
        ? (this.stats.hits / (this.stats.hits + this.stats.misses) * 100).toFixed(1) + '%'
        : '0%'
    };
  }
}

// ==================== Token 优化管理器 ====================
class TokenOptimizer {
  constructor(options = {}) {
    this.counter = new TokenCounter();
    this.contextCompressor = new ContextCompressor(options.compression);
    this.promptOptimizer = new PromptOptimizer();
    this.responseCache = new ResponseCache(options.cache);

    // 注册常用快捷方式
    this.initShortcuts();
  }

  /**
   * 初始化快捷方式
   */
  initShortcuts() {
    this.promptOptimizer.registerShortcut(
      '请帮我',
      ''
    );
    this.promptOptimizer.registerShortcut(
      '能不能',
      ''
    );
    this.promptOptimizer.registerShortcut(
      '我想知道',
      ''
    );
  }

  /**
   * 优化请求
   */
  optimizeRequest(prompt, context = '') {
    // 1. 检查缓存
    const cached = this.responseCache.get(prompt, context);
    if (cached) {
      return {
        cached: true,
        prompt: null,
        context: null,
        savedTokens: this.estimateTokens(prompt) + this.estimateTokens(context)
      };
    }

    // 2. 优化提示词
    const optimizedPrompt = this.promptOptimizer.optimize(prompt);

    // 3. 压缩上下文
    const compressedContext = context
      ? this.contextCompressor.compress(context)
      : { compressed: '', originalTokens: 0, compressedTokens: 0 };

    return {
      cached: false,
      prompt: optimizedPrompt.optimized,
      context: compressedContext.compressed,
      originalTokens: optimizedPrompt.originalTokens + compressedContext.originalTokens,
      optimizedTokens: optimizedPrompt.optimizedTokens + compressedContext.compressedTokens,
      savedTokens: optimizedPrompt.savedTokens + (compressedContext.originalTokens - compressedContext.compressedTokens)
    };
  }

  /**
   * 记录响应
   */
  recordResponse(prompt, response, context = '') {
    const inputTokens = this.estimateTokens(prompt + context);
    const outputTokens = this.estimateTokens(response);

    // 缓存响应
    this.responseCache.set(prompt, response, inputTokens + outputTokens, context);

    // 记录统计
    return this.counter.record(inputTokens, outputTokens);
  }

  /**
   * 估算 Token
   */
  estimateTokens(text) {
    const chineseChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
    const otherChars = text.length - chineseChars;
    return Math.ceil(chineseChars / 1.5 + otherChars / 4);
  }

  /**
   * 获取完整统计
   */
  getFullStats() {
    return {
      counter: this.counter.getStats(),
      promptOptimizer: this.promptOptimizer.getStats(),
      responseCache: this.responseCache.getStats(),
      totalSaved: this.counter.stats.saved + this.promptOptimizer.stats.savedTokens + this.responseCache.stats.savedTokens
    };
  }

  /**
   * 清理
   */
  cleanup() {
    return this.responseCache.cleanup();
  }
}

// 导出
module.exports = {
  TokenCounter,
  ContextCompressor,
  PromptOptimizer,
  ResponseCache,
  TokenOptimizer
};

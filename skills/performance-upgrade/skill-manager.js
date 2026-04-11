/**
 * 批量技能安装器
 * 
 * 支持同时安装多个技能，不阻塞
 */

// ==================== 批量安装器 ====================
class BatchSkillInstaller {
  constructor(options = {}) {
    this.maxConcurrent = options.maxConcurrent || 3;
    this.queue = [];
    this.running = new Map();
    this.completed = [];
    this.failed = [];
    this.stats = {
      total: 0,
      installed: 0,
      failed: 0,
      skipped: 0
    };
  }

  /**
   * 批量安装技能
   */
  async installBatch(skills, options = {}) {
    const results = [];
    const startTime = Date.now();

    // 分批执行
    for (let i = 0; i < skills.length; i += this.maxConcurrent) {
      const batch = skills.slice(i, i + this.maxConcurrent);
      const batchResults = await Promise.allSettled(
        batch.map(skill => this.installOne(skill, options))
      );

      for (let j = 0; j < batchResults.length; j++) {
        const result = batchResults[j];
        const skill = batch[j];

        if (result.status === 'fulfilled') {
          results.push({
            skill,
            success: true,
            ...result.value
          });
          this.completed.push(skill);
          this.stats.installed++;
        } else {
          results.push({
            skill,
            success: false,
            error: result.reason?.message || 'Unknown error'
          });
          this.failed.push(skill);
          this.stats.failed++;
        }
      }

      // 汇报进度
      if (options.onProgress) {
        options.onProgress({
          completed: this.completed.length,
          failed: this.failed.length,
          total: skills.length,
          progress: Math.round((i + batch.length) / skills.length * 100)
        });
      }
    }

    this.stats.total = skills.length;

    return {
      results,
      stats: this.stats,
      duration: Date.now() - startTime
    };
  }

  /**
   * 安装单个技能
   */
  async installOne(skill, options = {}) {
    const { name, source = 'clawhub' } = skill;

    // 检查是否已安装
    if (await this.isInstalled(name)) {
      this.stats.skipped++;
      return {
        name,
        status: 'skipped',
        message: 'Already installed'
      };
    }

    // 执行安装
    const startTime = Date.now();
    
    try {
      // 模拟安装过程（实际需要调用 ClawHub API）
      await this.executeInstall(name, source, options);
      
      return {
        name,
        status: 'installed',
        duration: Date.now() - startTime
      };
    } catch (error) {
      throw new Error(`Failed to install ${name}: ${error.message}`);
    }
  }

  /**
   * 检查是否已安装
   */
  async isInstalled(skillName) {
    // 检查本地技能列表
    const { exec } = require('child_process');
    const { promisify } = require('util');
    const execAsync = promisify(exec);

    try {
      const { stdout } = await execAsync('openclaw skills list --json 2>/dev/null || echo "[]"');
      const skills = JSON.parse(stdout || '[]');
      return skills.some(s => s.name === skillName);
    } catch {
      return false;
    }
  }

  /**
   * 执行安装
   */
  async executeInstall(name, source, options = {}) {
    const { exec } = require('child_process');
    const { promisify } = require('util');
    const execAsync = promisify(exec);

    const timeout = options.timeout || 60000;
    const mirror = options.mirror || 'china'; // 使用中国区镜像

    let command;
    if (source === 'clawhub') {
      command = `npx clawhub@latest install ${name} --mirror ${mirror}`;
    } else if (source === 'npm') {
      command = `npm install ${name}`;
    } else {
      command = `openclaw skills install ${name}`;
    }

    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        reject(new Error('Installation timeout'));
      }, timeout);

      execAsync(command)
        .then(({ stdout }) => {
          clearTimeout(timer);
          resolve({ output: stdout });
        })
        .catch((error) => {
          clearTimeout(timer);
          reject(error);
        });
    });
  }

  /**
   * 获取状态
   */
  getStatus() {
    return {
      queue: this.queue.length,
      running: this.running.size,
      completed: this.completed.length,
      failed: this.failed.length,
      stats: this.stats
    };
  }

  /**
   * 重置
   */
  reset() {
    this.queue = [];
    this.running.clear();
    this.completed = [];
    this.failed = [];
    this.stats = {
      total: 0,
      installed: 0,
      failed: 0,
      skipped: 0
    };
  }
}

// ==================== 技能搜索器 ====================
class SkillSearcher {
  constructor(options = {}) {
    this.mirrors = {
      global: 'https://clawhub.ai',
      china: 'https://clawhub.cn'
    };
    this.defaultMirror = options.mirror || 'china';
    this.cache = new Map();
    this.cacheTimeout = options.cacheTimeout || 300000; // 5分钟
  }

  /**
   * 搜索技能
   */
  async search(query, options = {}) {
    const mirror = options.mirror || this.defaultMirror;
    const cacheKey = `${mirror}:${query}`;

    // 检查缓存
    if (this.cache.has(cacheKey)) {
      const cached = this.cache.get(cacheKey);
      if (Date.now() - cached.timestamp < this.cacheTimeout) {
        return cached.results;
      }
    }

    // 执行搜索
    const results = await this.executeSearch(query, mirror, options);

    // 缓存结果
    this.cache.set(cacheKey, {
      results,
      timestamp: Date.now()
    });

    return results;
  }

  /**
   * 执行搜索
   */
  async executeSearch(query, mirror, options = {}) {
    const { exec } = require('child_process');
    const { promisify } = require('util');
    const execAsync = promisify(exec);

    const mirrorUrl = this.mirrors[mirror] || this.mirrors.global;
    const limit = options.limit || 10;

    try {
      const { stdout } = await execAsync(
        `npx clawhub@latest search "${query}" --mirror ${mirror} --json --limit ${limit} 2>/dev/null || echo "[]"`,
        { timeout: 30000 }
      );

      const results = JSON.parse(stdout || '[]');
      return results;
    } catch (error) {
      console.error('Search failed:', error.message);
      return [];
    }
  }

  /**
   * 获取技能详情
   */
  async getSkillInfo(skillId, options = {}) {
    const mirror = options.mirror || this.defaultMirror;
    const cacheKey = `info:${mirror}:${skillId}`;

    // 检查缓存
    if (this.cache.has(cacheKey)) {
      const cached = this.cache.get(cacheKey);
      if (Date.now() - cached.timestamp < this.cacheTimeout) {
        return cached.results;
      }
    }

    // 获取详情
    const { exec } = require('child_process');
    const { promisify } = require('util');
    const execAsync = promisify(exec);

    try {
      const { stdout } = await execAsync(
        `npx clawhub@latest info ${skillId} --mirror ${mirror} --json 2>/dev/null || echo "{}"`,
        { timeout: 30000 }
      );

      const info = JSON.parse(stdout || '{}');
      
      // 缓存结果
      this.cache.set(cacheKey, {
        results: info,
        timestamp: Date.now()
      });

      return info;
    } catch (error) {
      console.error('Get skill info failed:', error.message);
      return null;
    }
  }

  /**
   * 清理缓存
   */
  clearCache() {
    this.cache.clear();
  }

  /**
   * 获取状态
   */
  getStatus() {
    return {
      cacheSize: this.cache.size,
      defaultMirror: this.defaultMirror,
      mirrors: Object.keys(this.mirrors)
    };
  }
}

// 导出
module.exports = {
  BatchSkillInstaller,
  SkillSearcher
};

/**
 * 通用 API 集成框架
 * 
 * 快速集成任何第三方 API，如企查查、天眼查等
 */

// ==================== API 配置管理器 ====================
class APIConfigManager {
  constructor() {
    this.apis = new Map();
    this.presets = new Map();
    
    // 预设常用 API
    this.initPresets();
  }

  /**
   * 初始化预设 API
   */
  initPresets() {
    // 企查查
    this.presets.set('qichacha', {
      name: '企查查',
      baseUrl: 'https://api.qichacha.com',
      authType: 'apikey',
      authHeader: 'Authorization',
      endpoints: {
        searchCompany: {
          path: '/api/company/search',
          method: 'GET',
          params: ['keyword', 'pageIndex', 'pageSize']
        },
        getCompanyDetail: {
          path: '/api/company/detail',
          method: 'GET',
          params: ['companyId']
        },
        getShareholders: {
          path: '/api/company/shareholders',
          method: 'GET',
          params: ['companyId']
        }
      }
    });

    // 天眼查
    this.presets.set('tianyancha', {
      name: '天眼查',
      baseUrl: 'https://api.tianyancha.com',
      authType: 'apikey',
      authHeader: 'Authorization',
      endpoints: {
        searchCompany: {
          path: '/services/open/search',
          method: 'GET',
          params: ['keyword', 'pageSize']
        },
        getCompanyDetail: {
          path: '/services/open/company',
          method: 'GET',
          params: ['id']
        }
      }
    });

    // 爱企查
    this.presets.set('aiqicha', {
      name: '爱企查',
      baseUrl: 'https://aiqicha.baidu.com',
      authType: 'cookie',
      endpoints: {
        searchCompany: {
          path: '/q',
          method: 'GET',
          params: ['query']
        }
      }
    });
  }

  /**
   * 注册 API
   */
  register(apiId, config) {
    this.apis.set(apiId, {
      ...config,
      id: apiId,
      createdAt: Date.now()
    });
    return this.apis.get(apiId);
  }

  /**
   * 使用预设
   */
  usePreset(presetId, credentials) {
    const preset = this.presets.get(presetId);
    if (!preset) {
      throw new Error(`Preset not found: ${presetId}`);
    }

    return this.register(presetId, {
      ...preset,
      credentials
    });
  }

  /**
   * 获取 API 配置
   */
  get(apiId) {
    return this.apis.get(apiId) || this.presets.get(apiId);
  }

  /**
   * 列出所有可用 API
   */
  list() {
    const presets = Array.from(this.presets.keys()).map(id => ({
      id,
      name: this.presets.get(id).name,
      type: 'preset'
    }));

    const custom = Array.from(this.apis.keys()).map(id => ({
      id,
      name: this.apis.get(id).name,
      type: 'custom'
    }));

    return [...presets, ...custom];
  }
}

// ==================== API 调用器 ====================
class APICaller {
  constructor(config) {
    this.config = config;
    this.stats = {
      total: 0,
      success: 0,
      failed: 0,
      totalTokens: 0
    };
  }

  /**
   * 调用 API
   */
  async call(endpoint, params = {}, options = {}) {
    const endpointConfig = this.config.endpoints?.[endpoint];
    if (!endpointConfig) {
      throw new Error(`Endpoint not found: ${endpoint}`);
    }

    const startTime = Date.now();
    this.stats.total++;

    try {
      const url = this.buildUrl(endpointConfig, params);
      const headers = this.buildHeaders();
      const body = endpointConfig.method === 'POST' 
        ? JSON.stringify(params) 
        : undefined;

      const response = await fetch(url, {
        method: endpointConfig.method,
        headers,
        body,
        timeout: options.timeout || 30000
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      this.stats.success++;

      return {
        success: true,
        data,
        duration: Date.now() - startTime
      };
    } catch (error) {
      this.stats.failed++;
      return {
        success: false,
        error: error.message,
        duration: Date.now() - startTime
      };
    }
  }

  /**
   * 构建 URL
   */
  buildUrl(endpointConfig, params) {
    let url = this.config.baseUrl + endpointConfig.path;

    if (endpointConfig.method === 'GET') {
      const query = new URLSearchParams();
      for (const param of endpointConfig.params || []) {
        if (params[param] !== undefined) {
          query.append(param, params[param]);
        }
      }
      url += '?' + query.toString();
    }

    return url;
  }

  /**
   * 构建请求头
   */
  buildHeaders() {
    const headers = {
      'Content-Type': 'application/json'
    };

    const { authType, authHeader, credentials } = this.config;

    if (authType === 'apikey' && credentials?.apiKey) {
      headers[authHeader || 'Authorization'] = credentials.apiKey;
    } else if (authType === 'bearer' && credentials?.token) {
      headers['Authorization'] = `Bearer ${credentials.token}`;
    } else if (authType === 'cookie' && credentials?.cookie) {
      headers['Cookie'] = credentials.cookie;
    }

    return headers;
  }

  /**
   * 获取统计
   */
  getStats() {
    return {
      ...this.stats,
      successRate: this.stats.total > 0
        ? (this.stats.success / this.stats.total * 100).toFixed(1) + '%'
        : '0%'
    };
  }
}

// ==================== 企业信息查询器 ====================
class CompanyInfoQuerier {
  constructor(apiCaller) {
    this.caller = apiCaller;
    this.cache = new Map();
    this.cacheTimeout = 3600000; // 1小时
  }

  /**
   * 搜索公司
   */
  async searchCompany(keyword, options = {}) {
    // 检查缓存
    const cacheKey = `search:${keyword}`;
    const cached = this.cache.get(cacheKey);
    if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
      return cached.data;
    }

    // 调用 API
    const result = await this.caller.call('searchCompany', {
      keyword,
      pageIndex: options.pageIndex || 1,
      pageSize: options.pageSize || 10
    });

    // 缓存结果
    if (result.success) {
      this.cache.set(cacheKey, {
        data: result,
        timestamp: Date.now()
      });
    }

    return result;
  }

  /**
   * 获取公司详情
   */
  async getCompanyDetail(companyId) {
    // 检查缓存
    const cacheKey = `detail:${companyId}`;
    const cached = this.cache.get(cacheKey);
    if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
      return cached.data;
    }

    // 调用 API
    const result = await this.caller.call('getCompanyDetail', {
      companyId
    });

    // 缓存结果
    if (result.success) {
      this.cache.set(cacheKey, {
        data: result,
        timestamp: Date.now()
      });
    }

    return result;
  }

  /**
   * 获取股东信息
   */
  async getShareholders(companyId) {
    const cacheKey = `shareholders:${companyId}`;
    const cached = this.cache.get(cacheKey);
    if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
      return cached.data;
    }

    const result = await this.caller.call('getShareholders', {
      companyId
    });

    if (result.success) {
      this.cache.set(cacheKey, {
        data: result,
        timestamp: Date.now()
      });
    }

    return result;
  }

  /**
   * 清理缓存
   */
  clearCache() {
    this.cache.clear();
  }
}

// ==================== 统一 API 管理器 ====================
class UnifiedAPIManager {
  constructor() {
    this.configManager = new APIConfigManager();
    this.callers = new Map();
    this.queriers = new Map();
  }

  /**
   * 注册 API
   */
  registerAPI(apiId, config) {
    this.configManager.register(apiId, config);
    const caller = new APICaller(this.configManager.get(apiId));
    this.callers.set(apiId, caller);
    return caller;
  }

  /**
   * 使用预设 API
   */
  usePreset(presetId, credentials) {
    this.configManager.usePreset(presetId, credentials);
    const caller = new APICaller(this.configManager.get(presetId));
    this.callers.set(presetId, caller);

    // 如果是企业查询类 API，创建查询器
    if (['qichacha', 'tianyancha', 'aiqicha'].includes(presetId)) {
      const querier = new CompanyInfoQuerier(caller);
      this.queriers.set(presetId, querier);
    }

    return caller;
  }

  /**
   * 获取调用器
   */
  getCaller(apiId) {
    return this.callers.get(apiId);
  }

  /**
   * 获取查询器
   */
  getQuerier(apiId) {
    return this.queriers.get(apiId);
  }

  /**
   * 搜索公司（便捷方法）
   */
  async searchCompany(apiId, keyword, options = {}) {
    const querier = this.queriers.get(apiId);
    if (!querier) {
      throw new Error(`Querier not found for: ${apiId}`);
    }
    return querier.searchCompany(keyword, options);
  }

  /**
   * 获取公司详情（便捷方法）
   */
  async getCompanyDetail(apiId, companyId) {
    const querier = this.queriers.get(apiId);
    if (!querier) {
      throw new Error(`Querier not found for: ${apiId}`);
    }
    return querier.getCompanyDetail(companyId);
  }

  /**
   * 列出所有可用 API
   */
  listAPIs() {
    return this.configManager.list();
  }

  /**
   * 获取统计
   */
  getStats() {
    const stats = {};
    for (const [id, caller] of this.callers) {
      stats[id] = caller.getStats();
    }
    return stats;
  }
}

// 导出
module.exports = {
  APIConfigManager,
  APICaller,
  CompanyInfoQuerier,
  UnifiedAPIManager
};

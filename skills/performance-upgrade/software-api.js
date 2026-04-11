/**
 * 软件操作 API 自动生成器
 * 
 * 当操作某个软件后，自动将其封装为可复用的 API
 */

// ==================== 操作记录器 ====================
class OperationRecorder {
  constructor() {
    this.operations = new Map();
    this.patterns = new Map();
    this.stats = {
      total: 0,
      recorded: 0,
      converted: 0
    };
  }

  /**
   * 记录操作
   */
  record(operation) {
    const {
      app,           // 应用名称
      action,        // 操作类型
      steps,         // 操作步骤
      params,        // 参数
      result,        // 结果
      success        // 是否成功
    } = operation;

    const id = `op_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    const record = {
      id,
      app,
      action,
      steps,
      params,
      result: success ? result : null,
      error: success ? null : result,
      success,
      timestamp: Date.now(),
      count: 1
    };

    this.operations.set(id, record);
    this.stats.total++;
    this.stats.recorded++;

    // 分析模式
    this.analyzePattern(record);

    return record;
  }

  /**
   * 分析操作模式
   */
  analyzePattern(record) {
    const { app, action, steps, params } = record;
    const patternKey = `${app}:${action}`;

    if (!this.patterns.has(patternKey)) {
      this.patterns.set(patternKey, {
        app,
        action,
        steps: [],
        params: new Set(),
        examples: [],
        count: 0,
        successRate: 0,
        avgDuration: 0
      });
    }

    const pattern = this.patterns.get(patternKey);
    pattern.count++;
    pattern.params = new Set([...pattern.params, ...Object.keys(params || {})]);
    pattern.examples.push(record.id);

    // 保留最近 10 个示例
    if (pattern.examples.length > 10) {
      pattern.examples.shift();
    }

    // 更新成功率
    const examples = pattern.examples.map(id => this.operations.get(id));
    const successCount = examples.filter(r => r?.success).length;
    pattern.successRate = (successCount / examples.length * 100).toFixed(1);

    // 提取通用步骤
    if (pattern.steps.length === 0 && record.success) {
      pattern.steps = this.extractCommonSteps(steps);
    }
  }

  /**
   * 提取通用步骤
   */
  extractCommonSteps(steps) {
    if (!steps || steps.length === 0) return [];

    return steps.map((step, index) => {
      // 将具体值替换为参数占位符
      let template = step;
      
      // 常见替换规则
      const replacements = [
        { pattern: /搜索["'](.+?)["']/, template: '搜索"{keyword}"' },
        { pattern: /点击["'](.+?)["']/, template: '点击"{element}"' },
        { pattern: /输入["'](.+?)["']/, template: '输入"{text}"' },
        { pattern: /选择["'](.+?)["']/, template: '选择"{option}"' }
      ];

      for (const { pattern, template: t } of replacements) {
        if (pattern.test(step)) {
          template = step.replace(pattern, t);
          break;
        }
      }

      return {
        index,
        template,
        original: step
      };
    });
  }

  /**
   * 获取模式
   */
  getPattern(app, action) {
    return this.patterns.get(`${app}:${action}`);
  }

  /**
   * 获取所有模式
   */
  getAllPatterns() {
    return Array.from(this.patterns.entries()).map(([key, pattern]) => ({
      key,
      app: pattern.app,
      action: pattern.action,
      count: pattern.count,
      successRate: pattern.successRate,
      params: Array.from(pattern.params)
    }));
  }

  /**
   * 获取统计
   */
  getStats() {
    return {
      ...this.stats,
      patterns: this.patterns.size
    };
  }
}

// ==================== API 生成器 ====================
class APIGenerator {
  constructor(recorder) {
    this.recorder = recorder;
    this.apis = new Map();
    this.stats = {
      generated: 0,
      invoked: 0
    };
  }

  /**
   * 从操作记录生成 API
   */
  generateFromPattern(app, action, options = {}) {
    const pattern = this.recorder.getPattern(app, action);
    if (!pattern) {
      throw new Error(`Pattern not found: ${app}:${action}`);
    }

    const apiId = `${app}_${action}`.toLowerCase().replace(/\s+/g, '_');
    
    const api = {
      id: apiId,
      app,
      action,
      description: options.description || `${app} - ${action}`,
      params: this.inferParams(pattern),
      steps: pattern.steps,
      examples: pattern.examples.slice(0, 3),
      metadata: {
        createdAt: Date.now(),
        successRate: pattern.successRate,
        usageCount: 0
      }
    };

    this.apis.set(apiId, api);
    this.recorder.stats.converted++;
    this.stats.generated++;

    return api;
  }

  /**
   * 推断参数
   */
  inferParams(pattern) {
    const params = {};
    
    for (const param of pattern.params) {
      params[param] = {
        type: 'string',
        required: true,
        description: `${param} 参数`
      };
    }

    // 从步骤中推断参数
    for (const step of pattern.steps) {
      const matches = step.template.match(/\{(\w+)\}/g);
      if (matches) {
        for (const match of matches) {
          const paramName = match.slice(1, -1);
          if (!params[paramName]) {
            params[paramName] = {
              type: 'string',
              required: true,
              description: `${paramName} 参数`
            };
          }
        }
      }
    }

    return params;
  }

  /**
   * 获取 API
   */
  getAPI(apiId) {
    return this.apis.get(apiId);
  }

  /**
   * 列出所有 API
   */
  listAPIs() {
    return Array.from(this.apis.values()).map(api => ({
      id: api.id,
      app: api.app,
      action: api.action,
      description: api.description,
      params: Object.keys(api.params),
      usageCount: api.metadata.usageCount
    }));
  }

  /**
   * 获取统计
   */
  getStats() {
    return {
      ...this.stats,
      totalAPIs: this.apis.size
    };
  }
}

// ==================== API 调用器 ====================
class SoftwareAPICaller {
  constructor(generator, guiAgent) {
    this.generator = generator;
    this.guiAgent = guiAgent; // xiaoyi_gui_agent
    this.stats = {
      total: 0,
      success: 0,
      failed: 0
    };
  }

  /**
   * 调用 API
   */
  async call(apiId, params = {}) {
    const api = this.generator.getAPI(apiId);
    if (!api) {
      throw new Error(`API not found: ${apiId}`);
    }

    this.stats.total++;
    api.metadata.usageCount++;

    // 构建操作指令
    const instruction = this.buildInstruction(api, params);

    try {
      // 调用 GUI Agent 执行操作
      const result = await this.executeWithGUI(instruction);
      
      this.stats.success++;
      
      return {
        success: true,
        result,
        api: apiId,
        params
      };
    } catch (error) {
      this.stats.failed++;
      
      return {
        success: false,
        error: error.message,
        api: apiId,
        params
      };
    }
  }

  /**
   * 构建操作指令
   */
  buildInstruction(api, params) {
    let instruction = `在${api.app}中执行${api.action}操作：\n`;

    for (const step of api.steps) {
      let stepText = step.template;
      
      // 替换参数
      for (const [key, value] of Object.entries(params)) {
        stepText = stepText.replace(`{${key}}`, value);
      }

      instruction += `${step.index + 1}. ${stepText}\n`;
    }

    return instruction;
  }

  /**
   * 使用 GUI Agent 执行
   */
  async executeWithGUI(instruction) {
    // 自动记录操作
    const operation = {
      app: this.extractAppName(instruction),
      action: this.extractAction(instruction),
      steps: this.extractSteps(instruction),
      params: this.extractParams(instruction),
      result: null,
      success: false
    };

    try {
      // 调用 xiaoyi_gui_agent
      const result = await this.callGUIAgent(instruction);
      
      // 更新记录
      operation.result = result;
      operation.success = true;
      
      // 自动记录到管理器
      if (this.softwareAPIManager) {
        this.softwareAPIManager.recordOperation(operation);
      }
      
      return result;
    } catch (error) {
      operation.result = error.message;
      operation.success = false;
      
      // 即使失败也记录
      if (this.softwareAPIManager) {
        this.softwareAPIManager.recordOperation(operation);
      }
      
      throw error;
    }
  }

  /**
   * 调用 GUI Agent
   */
  async callGUIAgent(instruction) {
    // 这里需要实际调用 xiaoyi_gui_agent 工具
    // 实际实现需要根据工具接口
    
    console.log('[SoftwareAPICaller] 执行指令:', instruction);
    
    // 模拟执行
    return {
      executed: true,
      instruction
    };
  }

  /**
   * 从指令中提取应用名称
   */
  extractAppName(instruction) {
    const appPatterns = [
      { pattern: /小红书/, name: '小红书' },
      { pattern: /抖音/, name: '抖音' },
      { pattern: /百度/, name: '百度' },
      { pattern: /淘宝/, name: '淘宝' },
      { pattern: /京东/, name: '京东' },
      { pattern: /美团/, name: '美团' },
      { pattern: /大众点评/, name: '大众点评' },
      { pattern: /知乎/, name: '知乎' },
      { pattern: /微博/, name: '微博' }
    ];

    for (const { pattern, name } of appPatterns) {
      if (pattern.test(instruction)) {
        return name;
      }
    }

    return '未知应用';
  }

  /**
   * 从指令中提取操作类型
   */
  extractAction(instruction) {
    const actionPatterns = [
      { pattern: /搜索/, action: '搜索' },
      { pattern: /查找/, action: '搜索' },
      { pattern: /打开/, action: '打开' },
      { pattern: /浏览/, action: '浏览' },
      { pattern: /购买/, action: '购买' },
      { pattern: /下单/, action: '购买' }
    ];

    for (const { pattern, action } of actionPatterns) {
      if (pattern.test(instruction)) {
        return action;
      }
    }

    return '未知操作';
  }

  /**
   * 从指令中提取步骤
   */
  extractSteps(instruction) {
    const steps = [];
    const lines = instruction.split('\n').filter(l => l.trim());
    
    for (const line of lines) {
      if (/^\d+\./.test(line)) {
        steps.push(line.replace(/^\d+\.\s*/, ''));
      }
    }

    return steps;
  }

  /**
   * 从指令中提取参数
   */
  extractParams(instruction) {
    const params = {};
    
    // 提取搜索关键词
    const searchMatch = instruction.match(/搜索["'](.+?)["']/);
    if (searchMatch) {
      params.keyword = searchMatch[1];
    }

    // 提取输入内容
    const inputMatch = instruction.match(/输入["'](.+?)["']/);
    if (inputMatch) {
      params.text = inputMatch[1];
    }

    return params;
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

// ==================== GUI Agent 包装器 ====================
class GUIAgentWrapper {
  constructor(guiAgentTool, softwareAPIManager) {
    this.guiAgentTool = guiAgentTool;
    this.softwareAPIManager = softwareAPIManager;
    this.stats = {
      total: 0,
      recorded: 0,
      apiGenerated: 0
    };
  }

  /**
   * 执行操作（自动记录）
   */
  async execute(query) {
    this.stats.total++;

    // 提取操作信息
    const operation = {
      app: this.extractAppName(query),
      action: this.extractAction(query),
      steps: [],
      params: this.extractParams(query),
      query,
      result: null,
      success: false
    };

    try {
      // 调用实际的 GUI Agent
      const result = await this.guiAgentTool({ query });
      
      operation.result = result;
      operation.success = true;
      operation.steps = this.extractStepsFromResult(result);

      // 自动记录
      this.softwareAPIManager.recordOperation(operation);
      this.stats.recorded++;

      return result;
    } catch (error) {
      operation.result = error.message;
      operation.success = false;

      // 失败也记录
      this.softwareAPIManager.recordOperation(operation);
      this.stats.recorded++;

      throw error;
    }
  }

  /**
   * 从查询中提取应用名称
   */
  extractAppName(query) {
    const appPatterns = [
      { pattern: /小红书/, name: '小红书' },
      { pattern: /抖音/, name: '抖音' },
      { pattern: /百度/, name: '百度' },
      { pattern: /淘宝/, name: '淘宝' },
      { pattern: /京东/, name: '京东' },
      { pattern: /美团/, name: '美团' },
      { pattern: /大众点评/, name: '大众点评' },
      { pattern: /知乎/, name: '知乎' },
      { pattern: /微博/, name: '微博' },
      { pattern: /微信/, name: '微信' },
      { pattern: /支付宝/, name: '支付宝' }
    ];

    for (const { pattern, name } of appPatterns) {
      if (pattern.test(query)) {
        return name;
      }
    }

    return '未知应用';
  }

  /**
   * 从查询中提取操作类型
   */
  extractAction(query) {
    const actionPatterns = [
      { pattern: /搜索|查找|找/, action: '搜索' },
      { pattern: /打开|启动/, action: '打开' },
      { pattern: /浏览|查看/, action: '浏览' },
      { pattern: /购买|下单|买/, action: '购买' },
      { pattern: /发布|发|上传/, action: '发布' },
      { pattern: /评论|回复/, action: '评论' },
      { pattern: /关注|订阅/, action: '关注' }
    ];

    for (const { pattern, action } of actionPatterns) {
      if (pattern.test(query)) {
        return action;
      }
    }

    return '未知操作';
  }

  /**
   * 从查询中提取参数
   */
  extractParams(query) {
    const params = {};

    // 提取引号中的内容
    const quotedMatch = query.match(/["'](.+?)["']/);
    if (quotedMatch) {
      params.keyword = quotedMatch[1];
    }

    // 提取"搜索XXX"格式
    const searchMatch = query.match(/搜索(.+?)(?:\s|，|。|$)/);
    if (searchMatch) {
      params.keyword = searchMatch[1].trim();
    }

    return params;
  }

  /**
   * 从结果中提取步骤
   */
  extractStepsFromResult(result) {
    if (!result || typeof result !== 'string') return [];

    const steps = [];
    const lines = result.split('\n');

    for (const line of lines) {
      if (/^\d+\./.test(line) || /步骤|操作|执行/.test(line)) {
        steps.push(line.trim());
      }
    }

    return steps;
  }

  /**
   * 获取统计
   */
  getStats() {
    return {
      ...this.stats,
      apis: this.softwareAPIManager.listAPIs()
    };
  }
}

// ==================== 统一软件 API 管理器 ====================
class UnifiedSoftwareAPIManager {
  constructor(guiAgent) {
    this.recorder = new OperationRecorder();
    this.generator = new APIGenerator(this.recorder);
    this.caller = new SoftwareAPICaller(this.generator, guiAgent);
    this.autoGenerate = true; // 自动生成 API
  }

  /**
   * 记录操作（操作完成后调用）
   */
  recordOperation(operation) {
    const record = this.recorder.record(operation);

    // 自动生成 API（如果操作成功且出现 2 次以上）
    if (this.autoGenerate && operation.success) {
      const pattern = this.recorder.getPattern(operation.app, operation.action);
      if (pattern && pattern.count >= 2) {
        const apiId = `${operation.app}_${operation.action}`.toLowerCase().replace(/\s+/g, '_');
        
        if (!this.generator.getAPI(apiId)) {
          this.generator.generateFromPattern(operation.app, operation.action);
          console.log(`[SoftwareAPIManager] 自动生成 API: ${apiId}`);
        }
      }
    }

    return record;
  }

  /**
   * 手动生成 API
   */
  generateAPI(app, action, options = {}) {
    return this.generator.generateFromPattern(app, action, options);
  }

  /**
   * 调用 API
   */
  async callAPI(apiId, params = {}) {
    return this.caller.call(apiId, params);
  }

  /**
   * 列出所有 API
   */
  listAPIs() {
    return this.generator.listAPIs();
  }

  /**
   * 获取操作模式
   */
  getPatterns() {
    return this.recorder.getAllPatterns();
  }

  /**
   * 获取完整统计
   */
  getFullStats() {
    return {
      recorder: this.recorder.getStats(),
      generator: this.generator.getStats(),
      caller: this.caller.getStats()
    };
  }
}

// 导出
module.exports = {
  OperationRecorder,
  APIGenerator,
  SoftwareAPICaller,
  GUIAgentWrapper,
  UnifiedSoftwareAPIManager
};

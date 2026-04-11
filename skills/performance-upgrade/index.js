/**
 * Performance Upgrade - 性能升级
 * 
 * 通过代码级别的优化，提升系统性能
 */

// 导入各层模块
const core = require('./core');
const intelligence = require('./intelligence');
const capabilities = require('./capabilities');
const execution = require('./execution');
const control = require('./control');
const platform = require('./platform');
const token = require('./token');
const skillManager = require('./skill-manager');
const xiaoyiHelper = require('./xiaoyi-helper');
const heartbeat = require('./heartbeat');
const apiIntegration = require('./api-integration');
const softwareApi = require('./software-api');

// ==================== 统一性能管理器 ====================
class UnifiedPerformanceManager {
  constructor(options = {}) {
    // 核心层
    this.startupOptimizer = new core.StartupOptimizer();
    this.memoryManager = new core.MemoryManager(options.memory);

    // 智能层
    this.responseOptimizer = new intelligence.ResponseOptimizer(options.response);
    this.cacheManager = new intelligence.SmartCacheManager();

    // 能力层
    this.concurrencyManager = new capabilities.ConcurrencyManager(options.concurrency);

    // 执行层
    this.taskScheduler = new execution.SmartTaskScheduler(options.scheduler);
    this.timeoutController = new execution.TimeoutController(options.timeout);

    // 控制层
    this.performanceMonitor = new control.PerformanceMonitor(options.monitor);
    this.degradationManager = new control.AutoDegradationManager(options.degradation);
    this.leakDetector = new control.ResourceLeakDetector(options.leak);

    // 平台层
    this.connectionManager = new platform.ConnectionManager(options.connection);

    // Token 优化
    this.tokenOptimizer = new token.TokenOptimizer(options.token);

    // 技能管理
    this.batchInstaller = new skillManager.BatchSkillInstaller(options.skillInstall);
    this.skillSearcher = new skillManager.SkillSearcher(options.skillSearch);

    // 小艺帮记
    this.xiaoyiHelper = new xiaoyiHelper.UnifiedHelperManager(options.helper);

    // Heartbeat 优化
    this.heartbeatOptimizer = new heartbeat.HeartbeatOptimizer(options.heartbeat);

    // API 集成
    this.apiManager = new apiIntegration.UnifiedAPIManager();

    // 软件 API 自动生成
    this.softwareAPIManager = new softwareApi.UnifiedSoftwareAPIManager();

    // 初始化
    this.init();
  }

  /**
   * 初始化
   */
  init() {
    // 设置监控器
    this.degradationManager.setMonitor(this.performanceMonitor);

    // 启动监控
    this.performanceMonitor.startMonitoring(60000);
    this.leakDetector.startDetection(300000);
    this.memoryManager.startCleanup(60000);
  }

  /**
   * 执行任务（统一入口）
   */
  async executeTask(task, options = {}) {
    const startTime = Date.now();

    // 检查是否可以执行
    const check = this.concurrencyManager.semaphore.getStatus();
    if (check.current >= check.maxConcurrent) {
      return {
        success: false,
        error: '系统繁忙，请稍后再试',
        load: check.current + '/' + check.maxConcurrent
      };
    }

    // 记录开始
    const taskId = options.taskId || `task-${Date.now()}`;
    this.leakDetector.register(taskId, 'task', { options });

    try {
      // 执行任务
      const result = await this.concurrencyManager.execute(task, {
        timeout: options.timeout || 120000
      });

      // 记录指标
      const duration = Date.now() - startTime;
      this.performanceMonitor.recordMetric('responseTime', duration);

      return result;
    } finally {
      this.leakDetector.release(taskId);
    }
  }

  /**
   * 获取完整状态
   */
  getFullStatus() {
    return {
      core: {
        startup: this.startupOptimizer.getStatus(),
        memory: this.memoryManager.getStatus()
      },
      intelligence: {
        response: this.responseOptimizer.getStatus(),
        caches: this.cacheManager.getAllStatus()
      },
      capabilities: this.concurrencyManager.getFullStatus(),
      execution: {
        scheduler: this.taskScheduler.getStatus(),
        timeouts: this.timeoutController.getStatus()
      },
      control: {
        monitor: this.performanceMonitor.getStatus(),
        degradation: this.degradationManager.getStatus(),
        leaks: this.leakDetector.getStatus()
      },
      platform: this.connectionManager.getFullStatus(),
      token: this.tokenOptimizer.getFullStats(),
      skillManager: {
        installer: this.batchInstaller.getStatus(),
        searcher: this.skillSearcher.getStatus()
      },
      xiaoyiHelper: this.xiaoyiHelper.getFullStats(),
      heartbeat: this.heartbeatOptimizer.getStats(),
      apiIntegration: {
        apis: this.apiManager.listAPIs(),
        stats: this.apiManager.getStats()
      },
      softwareAPI: {
        apis: this.softwareAPIManager.listAPIs(),
        patterns: this.softwareAPIManager.getPatterns(),
        stats: this.softwareAPIManager.getFullStats()
      }
    };
  }

  /**
   * 执行优化
   */
  optimize() {
    const before = this.getFullStatus();

    // 清理缓存
    const cacheCleaned = this.cacheManager.cleanupAll();

    // 清理泄漏
    const leaksCleaned = this.leakDetector.cleanupLeaks();

    // 清理超时
    const timeoutsCleared = this.timeoutController.clearAll();

    // 清理任务队列
    const tasksCleared = this.taskScheduler.cancelAll();

    const after = this.getFullStatus();

    return {
      before,
      after,
      cleaned: {
        cache: cacheCleaned,
        leaks: leaksCleaned,
        timeouts: timeoutsCleared,
        tasks: tasksCleared
      }
    };
  }

  /**
   * 关闭
   */
  shutdown() {
    this.performanceMonitor.stopMonitoring();
    this.leakDetector.stopDetection();
    this.memoryManager.stopCleanup();
  }
}

// 导出单例
const performanceManager = new UnifiedPerformanceManager();

// 导出所有模块
module.exports = {
  // 核心层
  StartupOptimizer: core.StartupOptimizer,
  MemoryManager: core.MemoryManager,

  // 智能层
  ResponseOptimizer: intelligence.ResponseOptimizer,
  LRUCache: intelligence.LRUCache,
  SmartCacheManager: intelligence.SmartCacheManager,

  // 能力层
  Semaphore: capabilities.Semaphore,
  SkillInstancePool: capabilities.SkillInstancePool,
  ContextCachePool: capabilities.ContextCachePool,
  ConcurrencyManager: capabilities.ConcurrencyManager,

  // 执行层
  PriorityQueue: execution.PriorityQueue,
  SmartTaskScheduler: execution.SmartTaskScheduler,
  TimeoutController: execution.TimeoutController,

  // 控制层
  PerformanceMonitor: control.PerformanceMonitor,
  AutoDegradationManager: control.AutoDegradationManager,
  ResourceLeakDetector: control.ResourceLeakDetector,

  // 平台层
  HTTPConnectionPool: platform.HTTPConnectionPool,
  RequestCoalescer: platform.RequestCoalescer,
  ResponseCompressor: platform.ResponseCompressor,
  ConnectionManager: platform.ConnectionManager,

  // Token 优化
  TokenCounter: token.TokenCounter,
  ContextCompressor: token.ContextCompressor,
  PromptOptimizer: token.PromptOptimizer,
  ResponseCache: token.ResponseCache,
  TokenOptimizer: token.TokenOptimizer,

  // 技能管理
  BatchSkillInstaller: skillManager.BatchSkillInstaller,
  SkillSearcher: skillManager.SkillSearcher,

  // 小艺帮记
  XiaoyiHelperManager: xiaoyiHelper.XiaoyiHelperManager,
  DocumentHandler: xiaoyiHelper.DocumentHandler,
  ImageHandler: xiaoyiHelper.ImageHandler,
  VideoHandler: xiaoyiHelper.VideoHandler,
  LinkHandler: xiaoyiHelper.LinkHandler,
  UnifiedHelperManager: xiaoyiHelper.UnifiedHelperManager,

  // Heartbeat 优化
  HeartbeatOptimizer: heartbeat.HeartbeatOptimizer,
  LightweightHeartbeat: heartbeat.LightweightHeartbeat,

  // API 集成
  APIConfigManager: apiIntegration.APIConfigManager,
  APICaller: apiIntegration.APICaller,
  CompanyInfoQuerier: apiIntegration.CompanyInfoQuerier,
  UnifiedAPIManager: apiIntegration.UnifiedAPIManager,

  // 软件 API 自动生成
  OperationRecorder: softwareApi.OperationRecorder,
  APIGenerator: softwareApi.APIGenerator,
  SoftwareAPICaller: softwareApi.SoftwareAPICaller,
  GUIAgentWrapper: softwareApi.GUIAgentWrapper,
  UnifiedSoftwareAPIManager: softwareApi.UnifiedSoftwareAPIManager,

  // 统一管理器
  UnifiedPerformanceManager,
  performanceManager
};

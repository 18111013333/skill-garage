/**
 * 执行层性能升级
 * 
 * 优化任务调度和超时控制
 */

// ==================== 优先级队列 ====================
class PriorityQueue {
  constructor() {
    this.heap = [];
  }

  /**
   * 入队
   */
  enqueue(item, priority = 0) {
    this.heap.push({ item, priority });
    this.bubbleUp(this.heap.length - 1);
  }

  /**
   * 出队
   */
  dequeue() {
    if (this.heap.length === 0) return null;
    if (this.heap.length === 1) return this.heap.pop().item;

    const top = this.heap[0];
    this.heap[0] = this.heap.pop();
    this.bubbleDown(0);
    return top.item;
  }

  /**
   * 上浮
   */
  bubbleUp(index) {
    while (index > 0) {
      const parentIndex = Math.floor((index - 1) / 2);
      if (this.heap[parentIndex].priority >= this.heap[index].priority) break;
      [this.heap[parentIndex], this.heap[index]] = [this.heap[index], this.heap[parentIndex]];
      index = parentIndex;
    }
  }

  /**
   * 下沉
   */
  bubbleDown(index) {
    const length = this.heap.length;
    while (true) {
      const leftChild = 2 * index + 1;
      const rightChild = 2 * index + 2;
      let largest = index;

      if (leftChild < length && this.heap[leftChild].priority > this.heap[largest].priority) {
        largest = leftChild;
      }
      if (rightChild < length && this.heap[rightChild].priority > this.heap[largest].priority) {
        largest = rightChild;
      }

      if (largest === index) break;
      [this.heap[largest], this.heap[index]] = [this.heap[index], this.heap[largest]];
      index = largest;
    }
  }

  /**
   * 查看队首
   */
  peek() {
    return this.heap.length > 0 ? this.heap[0].item : null;
  }

  /**
   * 获取长度
   */
  get length() {
    return this.heap.length;
  }

  /**
   * 清空
   */
  clear() {
    this.heap = [];
  }
}

// ==================== 智能任务调度器 ====================
class SmartTaskScheduler {
  constructor(options = {}) {
    this.maxConcurrent = options.maxConcurrent || 3;
    this.defaultTimeout = options.defaultTimeout || 120000; // 2分钟
    this.queue = new PriorityQueue();
    this.running = new Map();
    this.completed = [];
    this.failed = [];
    this.taskId = 0;
  }

  /**
   * 调度任务
   */
  schedule(task, options = {}) {
    const taskId = ++this.taskId;
    const priority = options.priority || 0;
    const timeout = options.timeout || this.defaultTimeout;

    const taskWrapper = {
      id: taskId,
      task,
      priority,
      timeout,
      status: 'pending',
      createdAt: Date.now()
    };

    this.queue.enqueue(taskWrapper, priority);
    this.tryExecute();

    return taskId;
  }

  /**
   * 尝试执行任务
   */
  tryExecute() {
    while (this.running.size < this.maxConcurrent && this.queue.length > 0) {
      const taskWrapper = this.queue.dequeue();
      this.execute(taskWrapper);
    }
  }

  /**
   * 执行任务
   */
  async execute(taskWrapper) {
    taskWrapper.status = 'running';
    taskWrapper.startedAt = Date.now();
    this.running.set(taskWrapper.id, taskWrapper);

    // 设置超时
    const timeoutId = setTimeout(() => {
      this.timeout(taskWrapper.id);
    }, taskWrapper.timeout);

    try {
      const result = await taskWrapper.task();
      clearTimeout(timeoutId);

      taskWrapper.status = 'completed';
      taskWrapper.result = result;
      taskWrapper.duration = Date.now() - taskWrapper.startedAt;
      this.completed.push(taskWrapper);
    } catch (error) {
      clearTimeout(timeoutId);

      taskWrapper.status = 'failed';
      taskWrapper.error = error.message;
      taskWrapper.duration = Date.now() - taskWrapper.startedAt;
      this.failed.push(taskWrapper);
    } finally {
      this.running.delete(taskWrapper.id);
      this.tryExecute();
    }
  }

  /**
   * 任务超时
   */
  timeout(taskId) {
    const task = this.running.get(taskId);
    if (!task) return;

    task.status = 'timeout';
    task.error = 'Task timeout';
    task.duration = Date.now() - task.startedAt;
    this.failed.push(task);
    this.running.delete(taskId);
    this.tryExecute();
  }

  /**
   * 取消任务
   */
  cancel(taskId) {
    // 如果在运行中，无法取消
    if (this.running.has(taskId)) {
      return false;
    }

    // 从队列中移除
    const index = this.queue.heap.findIndex(t => t.item.id === taskId);
    if (index !== -1) {
      this.queue.heap.splice(index, 1);
      return true;
    }

    return false;
  }

  /**
   * 取消所有任务
   */
  cancelAll() {
    const count = this.queue.length;
    this.queue.clear();
    return count;
  }

  /**
   * 获取状态
   */
  getStatus() {
    return {
      queueLength: this.queue.length,
      running: this.running.size,
      maxConcurrent: this.maxConcurrent,
      completed: this.completed.length,
      failed: this.failed.length,
      avgDuration: this.getAvgDuration()
    };
  }

  /**
   * 获取平均执行时间
   */
  getAvgDuration() {
    const all = [...this.completed, ...this.failed];
    if (all.length === 0) return 0;
    const total = all.reduce((sum, t) => sum + (t.duration || 0), 0);
    return Math.round(total / all.length);
  }
}

// ==================== 超时控制器 ====================
class TimeoutController {
  constructor(defaultTimeout = 30000) {
    this.defaultTimeout = defaultTimeout;
    this.timeouts = new Map();
    this.stats = {
      total: 0,
      triggered: 0,
      cleared: 0
    };
  }

  /**
   * 设置超时
   */
  setTimeout(id, callback, timeout = this.defaultTimeout) {
    this.clearTimeout(id);

    this.stats.total++;

    const timeoutId = setTimeout(() => {
      this.stats.triggered++;
      this.timeouts.delete(id);
      callback();
    }, timeout);

    this.timeouts.set(id, {
      timeoutId,
      callback,
      startedAt: Date.now(),
      duration: timeout
    });

    return id;
  }

  /**
   * 清除超时
   */
  clearTimeout(id) {
    const item = this.timeouts.get(id);
    if (item) {
      clearTimeout(item.timeoutId);
      this.timeouts.delete(id);
      this.stats.cleared++;
      return true;
    }
    return false;
  }

  /**
   * 清除所有超时
   */
  clearAll() {
    const count = this.timeouts.size;
    for (const [id, item] of this.timeouts) {
      clearTimeout(item.timeoutId);
    }
    this.timeouts.clear();
    this.stats.cleared += count;
    return count;
  }

  /**
   * 获取剩余时间
   */
  getRemaining(id) {
    const item = this.timeouts.get(id);
    if (!item) return null;
    return Math.max(0, item.duration - (Date.now() - item.startedAt));
  }

  /**
   * 获取状态
   */
  getStatus() {
    return {
      active: this.timeouts.size,
      stats: this.stats,
      items: Array.from(this.timeouts.entries()).map(([id, item]) => ({
        id,
        elapsed: Date.now() - item.startedAt,
        remaining: item.duration - (Date.now() - item.startedAt)
      }))
    };
  }
}

// 导出
module.exports = {
  PriorityQueue,
  SmartTaskScheduler,
  TimeoutController
};

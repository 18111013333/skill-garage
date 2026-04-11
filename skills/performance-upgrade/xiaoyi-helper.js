/**
 * 小艺帮记 Skill
 * 
 * 支持小艺Claw收藏、查询文档、图片、视频、网页链接
 */

// ==================== 小艺帮记管理器 ====================
class XiaoyiHelperManager {
  constructor(options = {}) {
    this.collections = new Map();
    this.index = new Map();
    this.maxItems = options.maxItems || 1000;
    this.stats = {
      total: 0,
      documents: 0,
      images: 0,
      videos: 0,
      links: 0
    };
  }

  /**
   * 添加收藏
   */
  async addCollection(item) {
    const { type, content, title, tags = [] } = item;
    const id = `col_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

    const collection = {
      id,
      type,
      title,
      content,
      tags,
      createdAt: Date.now(),
      updatedAt: Date.now()
    };

    this.collections.set(id, collection);
    this.updateIndex(collection);
    this.updateStats(type, 1);

    return collection;
  }

  /**
   * 查询收藏
   */
  async queryCollections(query = {}) {
    const { type, keyword, tags, limit = 10 } = query;
    let results = Array.from(this.collections.values());

    // 按类型过滤
    if (type) {
      results = results.filter(c => c.type === type);
    }

    // 按关键词过滤
    if (keyword) {
      const lowerKeyword = keyword.toLowerCase();
      results = results.filter(c => 
        c.title?.toLowerCase().includes(lowerKeyword) ||
        c.content?.toLowerCase().includes(lowerKeyword)
      );
    }

    // 按标签过滤
    if (tags && tags.length > 0) {
      results = results.filter(c => 
        tags.some(tag => c.tags?.includes(tag))
      );
    }

    // 按时间排序（最新的在前）
    results.sort((a, b) => b.createdAt - a.createdAt);

    // 限制数量
    return results.slice(0, limit);
  }

  /**
   * 获取单个收藏
   */
  async getCollection(id) {
    return this.collections.get(id);
  }

  /**
   * 更新收藏
   */
  async updateCollection(id, updates) {
    const collection = this.collections.get(id);
    if (!collection) return null;

    const updated = {
      ...collection,
      ...updates,
      updatedAt: Date.now()
    };

    this.collections.set(id, updated);
    this.updateIndex(updated);

    return updated;
  }

  /**
   * 删除收藏
   */
  async deleteCollection(id) {
    const collection = this.collections.get(id);
    if (!collection) return false;

    this.collections.delete(id);
    this.removeFromIndex(collection);
    this.updateStats(collection.type, -1);

    return true;
  }

  /**
   * 更新索引
   */
  updateIndex(collection) {
    const { type, tags = [] } = collection;

    // 类型索引
    if (!this.index.has(type)) {
      this.index.set(type, new Set());
    }
    this.index.get(type).add(collection.id);

    // 标签索引
    for (const tag of tags) {
      const tagKey = `tag:${tag}`;
      if (!this.index.has(tagKey)) {
        this.index.set(tagKey, new Set());
      }
      this.index.get(tagKey).add(collection.id);
    }
  }

  /**
   * 从索引中移除
   */
  removeFromIndex(collection) {
    const { type, tags = [] } = collection;

    // 移除类型索引
    if (this.index.has(type)) {
      this.index.get(type).delete(collection.id);
    }

    // 移除标签索引
    for (const tag of tags) {
      const tagKey = `tag:${tag}`;
      if (this.index.has(tagKey)) {
        this.index.get(tagKey).delete(collection.id);
      }
    }
  }

  /**
   * 更新统计
   */
  updateStats(type, delta) {
    this.stats.total += delta;
    
    switch (type) {
      case 'document':
        this.stats.documents += delta;
        break;
      case 'image':
        this.stats.images += delta;
        break;
      case 'video':
        this.stats.videos += delta;
        break;
      case 'link':
        this.stats.links += delta;
        break;
    }
  }

  /**
   * 获取统计
   */
  getStats() {
    return {
      ...this.stats,
      indexTypes: this.index.size
    };
  }

  /**
   * 清空所有收藏
   */
  clear() {
    this.collections.clear();
    this.index.clear();
    this.stats = {
      total: 0,
      documents: 0,
      images: 0,
      videos: 0,
      links: 0
    };
  }
}

// ==================== 文档处理器 ====================
class DocumentHandler {
  constructor(helper) {
    this.helper = helper;
  }

  /**
   * 保存文档
   */
  async saveDocument(title, content, tags = []) {
    return this.helper.addCollection({
      type: 'document',
      title,
      content,
      tags
    });
  }

  /**
   * 查询文档
   */
  async queryDocuments(keyword, limit = 10) {
    return this.helper.queryCollections({
      type: 'document',
      keyword,
      limit
    });
  }
}

// ==================== 图片处理器 ====================
class ImageHandler {
  constructor(helper) {
    this.helper = helper;
  }

  /**
   * 保存图片
   */
  async saveImage(title, url, description = '', tags = []) {
    return this.helper.addCollection({
      type: 'image',
      title,
      content: url,
      description,
      tags
    });
  }

  /**
   * 查询图片
   */
  async queryImages(keyword, limit = 10) {
    return this.helper.queryCollections({
      type: 'image',
      keyword,
      limit
    });
  }
}

// ==================== 视频处理器 ====================
class VideoHandler {
  constructor(helper) {
    this.helper = helper;
  }

  /**
   * 保存视频
   */
  async saveVideo(title, url, description = '', tags = []) {
    return this.helper.addCollection({
      type: 'video',
      title,
      content: url,
      description,
      tags
    });
  }

  /**
   * 查询视频
   */
  async queryVideos(keyword, limit = 10) {
    return this.helper.queryCollections({
      type: 'video',
      keyword,
      limit
    });
  }
}

// ==================== 链接处理器 ====================
class LinkHandler {
  constructor(helper) {
    this.helper = helper;
  }

  /**
   * 保存链接
   */
  async saveLink(title, url, description = '', tags = []) {
    return this.helper.addCollection({
      type: 'link',
      title,
      content: url,
      description,
      tags
    });
  }

  /**
   * 查询链接
   */
  async queryLinks(keyword, limit = 10) {
    return this.helper.queryCollections({
      type: 'link',
      keyword,
      limit
    });
  }
}

// ==================== 统一帮记管理器 ====================
class UnifiedHelperManager {
  constructor(options = {}) {
    this.helper = new XiaoyiHelperManager(options);
    this.documents = new DocumentHandler(this.helper);
    this.images = new ImageHandler(this.helper);
    this.videos = new VideoHandler(this.helper);
    this.links = new LinkHandler(this.helper);
  }

  /**
   * 智能保存（自动识别类型）
   */
  async smartSave(item) {
    const { url, type } = item;

    // 自动识别类型
    if (!type && url) {
      if (url.match(/\.(jpg|jpeg|png|gif|webp)$/i)) {
        item.type = 'image';
      } else if (url.match(/\.(mp4|avi|mov|mkv)$/i)) {
        item.type = 'video';
      } else if (url.match(/\.(pdf|doc|docx|xls|xlsx|ppt|pptx)$/i)) {
        item.type = 'document';
      } else {
        item.type = 'link';
      }
    }

    return this.helper.addCollection(item);
  }

  /**
   * 智能查询
   */
  async smartQuery(query) {
    return this.helper.queryCollections(query);
  }

  /**
   * 获取完整统计
   */
  getFullStats() {
    return this.helper.getStats();
  }
}

// 导出
module.exports = {
  XiaoyiHelperManager,
  DocumentHandler,
  ImageHandler,
  VideoHandler,
  LinkHandler,
  UnifiedHelperManager
};

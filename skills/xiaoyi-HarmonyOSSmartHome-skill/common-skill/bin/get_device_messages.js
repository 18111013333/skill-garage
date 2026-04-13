// ==================== get_device_messages 子技能 ====================
// 功能：获取设备消息/告警
import path from 'path';
import { fileURLToPath } from 'url';
import {
  hagSkillServicePost,
  saveDataToTxt,
  generateTraceId,
  hagSkillServicePostWithPathParams
} from '../../utils/hag-connect/utils.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DEVICE_MESSAGES_DIR = path.join(__dirname, '../out_put/get_device_messages');
const DEVICE_MESSAGES_TXT = path.join(DEVICE_MESSAGES_DIR, 'device_messages.txt');

function resolveCutoffTimestamp(opts) {
  const now = Date.now();
  const maxDays = 30;
  
  if (opts.lastDays) {
    const days = parseInt(opts.lastDays, 10);
    if (isNaN(days) || days <= 0) {
      throw new Error('lastDays必须是大于0的整数');
    }
    if (days > maxDays) {
      throw new Error(`lastDays不能超过${maxDays}天`);
    }
    return now - days * 24 * 60 * 60 * 1000;
  }
  if (opts.date) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    if (opts.date === 'today') return today.getTime();
    else if (opts.date === 'yesterday') return today.getTime() - 24 * 60 * 60 * 1000;
  }
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return today.getTime() - 24 * 60 * 60 * 1000;
}

/**
 * 获取设备消息
 */
export async function getDeviceMessages(opts = {}, verbose = false) {
  if (!opts || typeof opts !== 'object') {
    opts = {}; // 默认空对象
  }
  
  const traceId = generateTraceId();
  process.stderr.write(`[trace-id] ${traceId}\n`);
  
  try {
    const cutoff = resolveCutoffTimestamp(opts);
    if (verbose) console.error(`[verbose] 消息截止时间戳：${cutoff}`);
    if (verbose) console.error('[verbose] 开始获取设备消息列表');
    
    // 验证最大返回条数限制
    const maxPageSize = 50;
    const currentIndex = '1';
    const pageSize = '10';
    
    if (parseInt(pageSize, 10) > maxPageSize) {
      throw new Error(`页面大小${pageSize}超过最大值${maxPageSize}`);
    }
  // ==================== 第一步：查询未读消息列表 ====================
  // HAG 请求：{"type": "queryUnreadMessagesV1", "pathParams": {"type": 2}}
  const listResp = await hagSkillServicePostWithPathParams('queryUnreadMessagesV1',  { type: 2 }
  , verbose);
  
  // 解析响应（hag 返回格式：{"errorCode":"0","errorMsg":"success","data":{"total":0,"hasMore":false,"messages":[...]}}）
    const listData = listResp?.data || {};
    const messages = listData?.messages || [];
    
    // 验证消息数据格式
    if (!Array.isArray(messages)) {
      throw new Error('消息数据不是数组格式');
    }
    
    // 获取唯一设备ID列表，验证其格式
    const subIds = [...new Set(messages
      .map(m => m?.subId)
      .filter(subId => subId && typeof subId === 'string')
    )];
    
    if (verbose) console.error(`[verbose] 获取到 ${subIds.length} 个设备的消息`);
    
    // ==================== 第二步：根据 subId 查询每个设备的消息详情 ====================
    const allDetails = [];
    const maxDevices = 300; // 最大设备数量限制
    
    if (subIds.length > maxDevices) {
      console.warn(`[warning] 设备数量${subIds.length}超过限制${maxDevices}，只处理前${maxDevices}个`);
      subIds.length = maxDevices;
    }
    
    for (const subId of subIds) {
      if (!subId || typeof subId !== 'string') {
        console.warn(`[warning] 无效的设备ID: ${subId}，跳过`);
        continue;
      }
      
      if (verbose) console.error(`[verbose] 查询设备 ${subId} 的消息详情`);
      
      try {
        // HAG 请求：{"type": "queryMessages", "pathParams": {"pageIndex": "1", "pageSize": "10", "subId": "xxx"}, "urlParams": {"type": "2"}}
        const detailResp = await hagSkillServicePost('queryMessages', {
          pathParams: {
            pageIndex: currentIndex,
            pageSize: pageSize,
            subId: subId
          },
          urlParams: { type: '2' }
        }, verbose);
        
        // 解析响应
        const detailData = detailResp?.data || {};
        allDetails.push({ subId, messages: detailData?.messages || [] });
      } catch (deviceError) {
        console.error(`[error] 查询设备${subId}消息详情失败: ${deviceError.message}`);
        continue;
      }
    }
    
    // ==================== 过滤和处理消息 ====================
    for (const d of allDetails) {
      const filtered = d.messages
        .filter(m => {
          // 验证消息对象基本结构
          if (!m || typeof m !== 'object') return false;
          
          // 验证时间戳
          if (typeof m.timestamp !== 'number' || m.timestamp < cutoff) return false;
          
          return true;
        })
        .map(m => ({
          subId: d.subId,
          timestamp: m.timestamp,
          title: m.title || '',
          description: m.body?.format?.richText?.description || '',
          msgTitle: m.body?.format?.richText?.title || ''
        }));
      
      if (filtered.length) result.push(...filtered);
    }
  
    // ==================== 过滤和处理消息 ====================
    const result = [];
    for (const d of allDetails) {
        const filtered = d.messages
          .filter(m => m.timestamp >= cutoff)
          .map(m => ({
            subId: d.subId,
            timestamp: m.timestamp,
            title: m.title,
            description: m.body?.format?.richText?.description || '',
            msgTitle: m.body?.format?.richText?.title || ''
        }));
      if (filtered.length) result.push(...filtered);
    }
    
    // 按时间戳降序排序
    result.sort((a, b) => b.timestamp - a.timestamp);
    
    // 限制返回消息数量，避免过大响应
    const maxMessages = 1000;
    let finalResult = result;
    if (result.length > maxMessages) {
      const truncated = result.slice(0, maxMessages);
      console.warn(`[warning] 消息总数${result.length}超过限制${maxMessages}，只返回前${maxMessages}条`);
      finalResult = truncated;
    }
    
    if (verbose) console.error(`[verbose] 过滤后剩余 ${finalResult.length} 条消息`);
    
    saveDataToTxt(DEVICE_MESSAGES_TXT, finalResult, '设备消息');
    
    return { traceId, deviceCount: subIds.length, totalMessages: finalResult.length, messages: finalResult };
    
  } catch (error) {
    console.error(`[error] 获取设备消息失败: ${error.message}`);
    throw error;
  }
}

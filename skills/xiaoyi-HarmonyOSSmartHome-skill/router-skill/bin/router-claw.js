// ==================== router-claw.js 主入口 ====================
// 功能：路由器技能总调度入口
// 版本：2.0.0 (使用 hag-connect)
import { Command } from 'commander';
import { randomUUID } from 'crypto';
import fs from 'fs';
import zlib from 'zlib';
import { promisify } from 'util';
import path from 'path';
import { fileURLToPath } from 'url';

// ==================== 引入公共模块（hag-connect） ====================
import { hagControl, generateTraceId, generateTimestamp } from '../../utils/hag-connect/utils.js';

// 导入应用信息模块
import { g_saAppInfo } from './sa_app_info.js';

// ==================== 路由器配置 ====================
const PROGRAM_NAME = 'router-claw';
const VERSION = '2.0.0';
const DEFAULT_SKILL_ID = 'xiaoyi_router';
const OPENCLAW_ENV_FILE = '/home/sandbox/.openclaw/.xiaoyienv';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 路由器设备配置（从环境变量加载）
const ROUTER_CONFIG = {
  devId: process.env.ROUTER_DEVID,
  prodId: process.env.ROUTER_PRODID
};

// 路由器 API 路径配置
const ROUTER_PATHS = {
  get_host_info: '.sys/gateway/system/HostInfo?filterAndroid=true&isSupportHostZip=true',
  get_child_protect: '.sys/gateway/ntwk/childHomepage',
  get_wan_status: '.sys/gateway/ntwk/wan?type=active',
  get_wandetect: '.sys/gateway/ntwk/wandetect',
  get_channel_info: '.sys/gateway/ntwk/channelinfo',
  get_5g_optimize: '.sys/gateway/ntwk/wlandbho',
  get_ipv6: '.sys/gateway/ntwk/ipv6_enable',
  get_user_behavior: '.sys/gateway/system/userbehavior',
  get_router_status: '.sys/gateway/system/processstatus',
  get_wifi_config: '.sys/gateway/ntwk/wlanradio',
  set_ipv6: '.sys/gateway/ntwk/ipv6_enable',
  add_child_device: '.sys/gateway/ntwk/childManage',
  del_child_device: '.sys/gateway/ntwk/childHomepage',
  set_net_time: '.sys/gateway/ntwk/childFrame',
  set_app_control: '.sys/gateway/ntwk/childModelApps',
  set_net_off: '.sys/gateway/ntwk/childHomepage',
  set_net_duration: '.sys/gateway/ntwk/childDailyUpdate',
  deny_games: '.sys/gateway/ntwk/childModelApps',
  deny_videos: '.sys/gateway/ntwk/childModelApps',
  deny_social: '.sys/gateway/ntwk/childModelApps',
  deny_shopping: '.sys/gateway/ntwk/childModelApps',
  deny_install: '.sys/gateway/ntwk/childModelApps',
  allow_games: '.sys/gateway/ntwk/childModelApps',
  allow_videos: '.sys/gateway/ntwk/childModelApps',
  allow_social: '.sys/gateway/ntwk/childModelApps',
  allow_shopping: '.sys/gateway/ntwk/childModelApps',
  allow_install: '.sys/gateway/ntwk/childModelApps',
  // 应用信息查询（本地功能，不调用路由器API）
  get_app_info: null, // 本地功能
  get_all_apps: null  // 本地功能
};

// ==================== 工具函数 ====================
/**
 * 格式化本地日期 YYYY-MM-DD
 */
function toLocalDateStr(d) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}

/**
 * 解密 HostInfo 的 gzip+base64 数据
 */
const gunzip = promisify(zlib.gunzip);

async function decodeHostInfo(content) {
  try {
    const buffer = Buffer.from(content, 'base64');
    const result = await gunzip(buffer);
    return JSON.parse(result.toString());
  } catch (e) {
    console.error('[decode] 解析设备信息失败:', e.message);
    return null;
  }
}

/**
 * 加载环境变量
 */
function loadOpenclawEnv(verbose) {
  const env = {};
  try {
    const content = fs.readFileSync(OPENCLAW_ENV_FILE, 'utf-8');
    for (const line of content.split('\n')) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      const idx = trimmed.indexOf('=');
      if (idx === -1) continue;
      const key = trimmed.slice(0, idx).trim();
      const value = trimmed.slice(idx + 1).trim();
      env[key] = value;
    }
    if (verbose) {
      console.error(`[verbose] 加载环境变量：${OPENCLAW_ENV_FILE}`);
    }
  } catch (err) {
    if (err.code === 'ENOENT' && verbose) {
      console.error(`[verbose] 未找到环境文件，使用系统环境变量`);
    }
  }
  return env;
}

/**
 * 生成请求 ID
 */
function generateRequestId() {
  return randomUUID();
}

/**
 * 根据应用分类ID获取分类名称
 */
function getCategoryName(categ) {
  const categoryMap = {
    1: '默认节点',
    2: '应用商店',
    4: '游戏',
    8: '应用服务',
    16: '视频类',
    32: '直播类',
    128: '社交类',
    256: '办公类',
    512: '购物类',
    1024: '支付类',
    2048: 'WiFi相关',
    4096: '教育类',
    8192: '学习类'
  };
  
  return categoryMap[categ] || `未知分类(${categ})`;
}

// ==================== 核心调度函数 ====================
async function callRouterClaw(tools, skillId, verbose = false, retryCount = 0) {
  const MAX_RETRY = 1; // 最多重试 1 次，避免无限循环
  const fileEnv = loadOpenclawEnv(verbose);
  
  const devId = fileEnv.ROUTER_DEVID || process.env.ROUTER_DEVID || ROUTER_CONFIG.devId;
  const prodId = fileEnv.ROUTER_PRODID || process.env.ROUTER_PRODID || ROUTER_CONFIG.prodId;

  if (verbose) {
    console.error(`[verbose] DEV_ID = ${devId}`);
    console.error(`[verbose] PROD_ID = ${prodId}`);
  }

  if (!devId || !prodId) {
    console.error('错误：必须配置 ROUTER_DEVID 和 ROUTER_PRODID 环境变量');
    process.exit(1);
  }

  const results = [];
  for (const tool of tools) {
    const { name, args } = tool;
    const sid = ROUTER_PATHS[name];
    
    if (!sid) {
      console.error(`[warning] 未知工具：${name}`);
      continue;
    }

    let payload = {
      devId,
      prodId,
      sid,
      mode: 'ACK',  // 路由器使用 ACK 模式
      operation: 'GET'  // 默认 GET
    };

    // ========== 信息查询 GET ==========
    if (name === 'get_host_info') {
      payload.operation = 'GET';
    } else if (name === 'get_child_protect') {
      payload.operation = 'GET';
    } else if (name === 'get_wan_status') {
      payload.operation = 'GET';
    } else if (name === 'get_wandetect') {
      payload.operation = 'GET';
    } else if (name === 'get_channel_info') {
      payload.operation = 'GET';
    } else if (name === 'get_5g_optimize') {
      payload.operation = 'GET';
    } else if (name === 'get_ipv6') {
      payload.operation = 'GET';
    } else if (name === 'get_user_behavior') {
      payload.operation = 'GET';
    } else if (name === 'get_router_status') {
      payload.operation = 'GET';
    } else if (name === 'get_wifi_config') {
      payload.operation = 'GET';
    }

    // ========== 控制操作 POST ==========
    else if (name === 'set_ipv6') {
      payload.operation = 'POST';
      payload.data = args.data || { Enable: 0, ID: 'InternetGatewayDevice.Services.X_IPv6.' };
    } else if (name === 'add_child_device') {
      const action = 'create';
      payload.operation = 'POST';
      payload.sid = ROUTER_PATHS.add_child_device;
      payload.data = {
        action: action,
        data: {
          action: action,
          devices: args.data?.devices || [],
          names: args.data?.names || [],
          privacyStatus: args.data?.privacyStatus || 0,
          type: args.data?.type || 0,
          urlStatus: args.data?.urlStatus || 0
        }
      };
    } else if (name === 'del_child_device') {
      const action = 'delete';
      payload.operation = 'POST';
      payload.sid = ROUTER_PATHS.del_child_device;
      payload.data = {
        action: action,
        data: {
          device: args.data?.device || '1'
        }
      };
    } else if (name === 'set_net_time') {
      const action = args.action || 'newCreate';
      payload.operation = 'POST';
      payload.sid = `.sys/gateway/ntwk/childFrame?devid=${String(args.deviceId || '1')}`;
      payload.data = {
        action: action,
        data: args.data
      };
    } else if (name === 'set_app_control') {
      const action = 'update';
      payload.operation = 'POST';
      payload.sid = `.sys/gateway/ntwk/childModelApps?devid=${String(args.deviceId || '1')}&type=${args.type || 1}`;
      payload.data = {
        action: action,
        data: args.data
      };
    } else if (name === 'set_net_off') {
      const action = 'delayUpdate';
      payload.operation = 'POST';
      payload.sid = '.sys/gateway/ntwk/childHomepage';
      payload.data = {
        action: action,
        data: args.data
      };
    } else if (name === 'set_net_duration') {
      const action = args.action || 'update';
      payload.operation = 'POST';
      payload.sid = '.sys/gateway/ntwk/childDailyUpdate';
      payload.data = {
        action: action,
        data: args.data || { daily: { monday: 90000, tuesday: 90000, wednesday: 90000, thursday: 90000, friday: 90000, saturday: 90000, sunday: 90000 }, device: "1" }
      };
    }

    // ========== 应用管理禁止操作 POST ==========
    else if (name === 'deny_games') {
      payload.operation = 'POST';
      payload.sid = '.sys/gateway/ntwk/childModelApps';
      payload.data = {
        action: 'update',
        data: {
          device: args.deviceId || '1',
          apps: ["153","221","152","220","118","287","151","218","286","252","251","285","250","284","114","283","249","147","113","215","282","248","112","281","145","247","213","280","144","246","108","279","107","175","278","244","106","140","243","209","277","105","207","276","104","206","275","171","239","103","170","238","102","203","169","101","100","201","233","131","199","232","130","163","231","230","196","195","228","193","123","191","192","122","156","225","155","189","224","154","255","254","216","181","180","179","178","211","210","271","270","167","133","234","268","166","267","165","266","265","197","264","161","160","158","227","261","157","226","260","259","222","257","187","256","186","185","253","117","184","150","116","217","149","182","148","146","214","109","142","177","139","274","240","204","273","135","202","134","200","132","198","164","129","162","126","125","124","121","223","258","120","188"],
          denyAll: 0,
          type: 1
        }
      };
    } else if (name === 'deny_videos') {
      payload.operation = 'POST';
      payload.sid = '.sys/gateway/ntwk/childModelApps';
      payload.data = {
        action: 'update',
        data: {
          device: args.deviceId || '1',
          apps: ["320","314","348","347","313","346","311","309","339","338","337","335","802","804","803","324","323","322","321","319","318","312","310","308","303","336","334","333","332","331","330","328","327","350","349","342","341","340","345","344","343"],
          denyAll: 0,
          type: 2
        }
      };
    } else if (name === 'deny_social') {
      payload.operation = 'POST';
      payload.sid = '.sys/gateway/ntwk/childModelApps';
      payload.data = {
        action: 'update',
        data: {
          device: args.deviceId || '1',
          apps: ["401","400","408","407","406"],
          denyAll: 0,
          type: 3
        }
      };
    } else if (name === 'deny_shopping') {
      payload.operation = 'POST';
      payload.sid = '.sys/gateway/ntwk/childModelApps';
      payload.data = {
        action: 'update',
        data: {
          device: args.deviceId || '1',
          apps: ["503","502","501","500","512","508","511","510","509"],
          denyAll: 0,
          type: 4
        }
      };
    } else if (name === 'deny_install') {
      payload.operation = 'POST';
      payload.sid = '.sys/gateway/ntwk/childModelApps';
      payload.data = {
        action: 'update',
        data: {
          device: args.deviceId || '1',
          apps: ["8","7","6","5","4","3","2","1"],
          denyAll: 0,
          type: 5
        }
      };
    }

    // ========== 应用管理取消操作 POST（两步） ==========
    else if (name === 'allow_games') {
      const deviceId = String(args.deviceId || '1');
      
      // 第一步：调用 Homepage 接口
      const payload1 = {
        devId,
        prodId,
        mode: 'ACK',
        operation: 'POST',
        sid: '.sys/gateway/ntwk/childHomepage',
        data: {
          action: 'gameUpdate',
          data: {
            device: deviceId,
            game: 1,
            video: 0,
            social: 0,
            payEnable: 0,
            appDownload: 0,
            urlEnable: 0,
            denyEnable: 0,
            delayEnable: 0,
            allow: 0,
            increaseTime: 0
          }
        }
      };
      
      // 第二步：调用 childModelApps 接口清空应用列表
      const payload2 = {
        devId,
        prodId,
        mode: 'ACK',
        operation: 'POST',
        sid: '.sys/gateway/ntwk/childModelApps',
        data: {
          action: 'update',
          data: {
            device: deviceId,
            apps: [],
            denyAll: 0,
            type: 1
          }
        }
      };
      
      let res1;
      let res2;
      try {
        res1 = await hagControl(payload1, verbose);
        res2 = await hagControl(payload2, verbose);
        
        results.push({ tool: name + "_step1", success: true, data: res1 });
        results.push({ tool: name + "_step2", success: true, data: res2 });
        continue;
       } catch (err) {        if (err.code === 401 && retryCount < MAX_RETRY) {
          console.log('[info] token 已过期，正在自动刷新...');
          return callRouterClaw(tools, skillId, verbose, retryCount + 1);
        }
        throw err;
      }
    } else if (name === 'allow_videos') {
      const deviceId = String(args.deviceId || '1');
      
      const payload1 = {
        devId,
        prodId,
        mode: 'ACK',
        operation: 'POST',
        sid: '.sys/gateway/ntwk/childHomepage',
        data: {
          action: 'videoUpdate',
          data: {
            device: deviceId,
            game: 0,
            video: 1,
            social: 0,
            payEnable: 0,
            appDownload: 0,
            urlEnable: 0,
            denyEnable: 0,
            delayEnable: 0,
            allow: 0,
            increaseTime: 0
          }
        }
      };
      
      const payload2 = {
        devId,
        prodId,
        mode: 'ACK',
        operation: 'POST',
        sid: '.sys/gateway/ntwk/childModelApps',
        data: {
          action: 'update',
          data: {
            device: deviceId,
            apps: [],
            denyAll: 0,
            type: 2
          }
        }
      };
      
      let res1;
      let res2;
      try {
        res1 = await hagControl(payload1, verbose);
        res2 = await hagControl(payload2, verbose);
        
        results.push({ tool: name + "_step1", success: true, data: res1 });
        results.push({ tool: name + "_step2", success: true, data: res2 });
        continue;
      } catch (err) {
        if (err.code === 401 && retryCount < MAX_RETRY) {
          console.log('[info] token 已过期，正在自动刷新...');
          return callRouterClaw(tools, skillId, verbose, retryCount + 1);
        }
        throw err;
      }
    } else if (name === 'allow_social') {
      const deviceId = String(args.deviceId || '1');
      
      const payload1 = {
        devId,
        prodId,
        mode: 'ACK',
        operation: 'POST',
        sid: '.sys/gateway/ntwk/childHomepage',
        data: {
          action: 'socialUpdate',
          data: {
            device: deviceId,
            game: 0,
            video: 0,
            social: 1,
            payEnable: 0,
            appDownload: 0,
            urlEnable: 0,
            denyEnable: 0,
            delayEnable: 0,
            allow: 0,
            increaseTime: 0
          }
        }
      };
      
      const payload2 = {
        devId,
        prodId,
        mode: 'ACK',
        operation: 'POST',
        sid: '.sys/gateway/ntwk/childModelApps',
        data: {
          action: 'update',
          data: {
            device: deviceId,
            apps: [],
            denyAll: 0,
            type: 3
          }
        }
      };
      
      let res1;
      let res2;
      try {
        res1 = await hagControl(payload1, verbose);
        res2 = await hagControl(payload2, verbose);
        
        results.push({ tool: name + "_step1", success: true, data: res1 });
        results.push({ tool: name + "_step2", success: true, data: res2 });
        continue;
      } catch (err) {
        if (err.code === 401 && retryCount < MAX_RETRY) {
          console.log('[info] token 已过期，正在自动刷新...');
          return callRouterClaw(tools, skillId, verbose, retryCount + 1);
        }
        throw err;
      }
    } else if (name === 'allow_shopping') {
      const deviceId = String(args.deviceId || '1');
      
      const payload1 = {
        devId,
        prodId,
        mode: 'ACK',
        operation: 'POST',
        sid: '.sys/gateway/ntwk/childHomepage',
        data: {
          action: 'payUpdate',
          data: {
            device: deviceId,
            game: 0,
            video: 0,
            social: 0,
            payEnable: 1,
            appDownload: 0,
            urlEnable: 0,
            denyEnable: 0,
            delayEnable: 0,
            allow: 0,
            increaseTime: 0
          }
        }
      };
      
      const payload2 = {
        devId,
        prodId,
        mode: 'ACK',
        operation: 'POST',
        sid: '.sys/gateway/ntwk/childModelApps',
        data: {
          action: 'update',
          data: {
            device: deviceId,
            apps: [],
            denyAll: 0,
            type: 4
          }
        }
      };
      
      let res1;
      let res2;
      try {
        res1 = await hagControl(payload1, verbose);
        res2 = await hagControl(payload2, verbose);
        
        results.push({ tool: name + "_step1", success: true, data: res1 });
        results.push({ tool: name + "_step2", success: true, data: res2 });
        continue;
      } catch (err) {
        if (err.code === 401 && retryCount < MAX_RETRY) {
          console.log('[info] token 已过期，正在自动刷新...');
          return callRouterClaw(tools, skillId, verbose, retryCount + 1);
        }
        throw err;
      }
    } else if (name === 'allow_install') {
      const deviceId = String(args.deviceId || '1');
      
      const payload1 = {
        devId,
        prodId,
        mode: 'ACK',
        operation: 'POST',
        sid: '.sys/gateway/ntwk/childHomepage',
        data: {
          action: 'installUpdate',
          data: {
            device: deviceId,
            game: 0,
            video: 0,
            social: 0,
            payEnable: 0,
            appDownload: 1,
            urlEnable: 0,
            denyEnable: 0,
            delayEnable: 0,
            allow: 0,
            increaseTime: 0
          }
        }
      };
      
      const payload2 = {
        devId,
        prodId,
        mode: 'ACK',
        operation: 'POST',
        sid: '.sys/gateway/ntwk/childModelApps',
        data: {
          action: 'update',
          data: {
            device: deviceId,
            apps: [],
            denyAll: 0,
            type: 5
          }
        }
      };
      
      let res1;
      let res2;
      try {
        res1 = await hagControl(payload1, verbose);
        res2 = await hagControl(payload2, verbose);
        
        results.push({ tool: name + "_step1", success: true, data: res1 });
        results.push({ tool: name + "_step2", success: true, data: res2 });
        continue;
       } catch (err) {
         if (err.code === 401 && retryCount < MAX_RETRY) {
           console.log('[info] token 已过期，正在自动刷新...');
           return callRouterClaw(tools, skillId, verbose, retryCount + 1);
         }
         throw err;
       }
     } else if (name === 'get_router_device_by_prodid') {      // 从本地 router_device_info.js 获取设备信息映射
      const deviceInfoData = await import('../router_device_info.js');
      const prodId = args.prodid || args.deviceId || 'K1AP'; // 默认使用 K1AP
      
      // 在本地映射表中查找 prodid 对应的设备信息
      let deviceInfo = null;
      
      // 查找匹配的 prodid
      const match = deviceInfoData.default.g_routerDeviceInfo.find(info => 
        info[1].toLowerCase() === String(prodId).toLowerCase()
      );
      
      if (match) {
        deviceInfo = {
          isRouter: true,
          prodId: match[1],
          device: match[0],
          chineseName: match[2],
          englishName: match[3],
          fromLocal: true, // 标记使用本地映射
          totalCount: deviceInfoData.default.g_routerDeviceInfo.length, // 总设备数
          note: '使用本地路由设备信息映射'
        };
      } else {
        deviceInfo = {
          isRouter: false,
          prodId: String(prodId),
          chineseName: '未识别的设备',
          englishName: 'Unrecognized Device',
          fromLocal: false,
          suggestion: '请检查prodid是否正确，查看支持的路由器设备列表'
        };
      }
      
      // 直接返回结果，不调用云侧接口
      results.push({
        tool: name,
        success: deviceInfo.isRouter,
        data: deviceInfo,
        message: deviceInfo.isRouter ? 
          `路由器识别成功: ${deviceInfo.chineseName} (${deviceInfo.englishName})` : 
          '该prodid在路由器设备映射表中未找到'
      });
      continue;
    } else if (name === 'get_app_info') {
      // 根据应用ID查询具体应用信息
      const appId = args.app_id || args.appId || String(args.id);
      
      if (!appId) {
        results.push({
          tool: name,
          success: false,
          message: '请提供要查询的应用ID'
        });
        continue;
      }
      
      // 在应用信息数组中查找匹配的应用
      const appInfo = g_saAppInfo.find(app => 
        String(app[1]) === String(appId)
      );
      
      if (appInfo) {
        results.push({
          tool: name,
          success: true,
          data: {
            appName: appInfo[0],
            appId: appInfo[1],
            categ: appInfo[2],
            message: `应用查询成功: ${appInfo[0]} (ID: ${appInfo[1]}, 分类: ${appInfo[2]})`
          }
        });
      } else {
        results.push({
          tool: name,
          success: false,
          message: `未找到ID为 ${appId} 的应用`
        });
      }
      continue;
    } else if (name === 'get_all_apps') {
      // 查询所有可用的应用列表
      const categorizedApps = {};
      
      // 按分类整理应用
      g_saAppInfo.forEach(app => {
        const categ = app[2];
        const categoryName = getCategoryName(categ);
        
        if (!categorizedApps[categoryName]) {
          categorizedApps[categoryName] = [];
        }
        
        categorizedApps[categoryName].push({
          name: app[0],
          id: app[1],
          categ: app[2]
        });
      });
      
      results.push({
        tool: name,
        success: true,
        data: {
          totalApps: g_saAppInfo.length,
          categories: categorizedApps,
          message: `共找到 ${g_saAppInfo.length} 个应用，按分类显示`
        }
      });
      continue;
    }

    let res;
    try {
      // 使用 hagControl 发送请求
      res = await hagControl(payload, verbose);
    } catch (err) {
      if (err.code === 401 && retryCount < MAX_RETRY) {
        console.log('[info] token 已过期，正在自动刷新...');
        return callRouterClaw(tools, skillId, verbose, retryCount + 1);
      }
      throw err;
    }

    // 自动解码 HostInfo 的 gzip+base64 数据
    if (name === 'get_host_info' && res?.data?.payload) {
      let payloadObj = typeof res.data.payload === 'string' ? JSON.parse(res.data.payload) : res.data.payload;
      if (payloadObj.content) {
        const decoded = await decodeHostInfo(payloadObj.content);
        res.data.payload = decoded;
      }
    }

    results.push({ tool: name, success: true, data: res });
  }

  console.log(JSON.stringify(results, null, 2));
}

// ==================== 注册命令 ====================
function registerCommands(program) {
  const toolNamesNeedAction = ['set_net_time', 'set_net_duration'];
  const toolNamesNeedData = ['add_child_device', 'del_child_device'];
  const toolNamesNeedProdid = ['get_router_device_by_prodid'];
  const toolNamesNeedAppId = ['get_app_info'];
  const toolNames = Object.keys(ROUTER_PATHS);
  
  for (const toolName of toolNames) {
    let command = program
      .command(toolName)
      .description(`路由器操作：${toolName}`)
      .option('--device-id <id>', '设备 ID', '1')
      .option('--data <json>', '控制参数 (JSON 字符串)')
      .option('--type <num>', '应用分类 1 游戏/2 影音/3 社交/4 购物/5 安装/7 学习')
      .option('--skill-id <id>', '技能 ID', DEFAULT_SKILL_ID)
      .option('--verbose', '调试日志')
      .action(async (opts) => {
        let args = {};
        if (opts.data) args.data = JSON.parse(opts.data);
        if (opts.deviceId) args.deviceId = String(opts.deviceId);
        if (opts.type) args.type = opts.type;
        if (toolNamesNeedAction.includes(toolName) && opts.action) {
          args.action = opts.action;
        }
        if (toolNamesNeedProdid.includes(toolName) && opts.prodid) {
          args.prodid = opts.prodid;
        }
        if (toolNamesNeedAppId.includes(toolName) && opts.appId) {
          args.appId = opts.appId;
        }

        await callRouterClaw([{ name: toolName, args }], opts.skillId, opts.verbose);
      });

    if (toolNamesNeedAction.includes(toolName)) {
      command.option('--action <type>', '操作类型 create/update/delete');
    }
    if (toolNamesNeedProdid.includes(toolName)) {
      command.option('--prodid <id>', '产品ID / 产品型号');
    }
    if (toolNamesNeedAppId.includes(toolName)) {
      command.option('--app-id <id>', '应用ID');
    }
  }
}

// ==================== 启动程序 ====================
const program = new Command();
program
  .name(PROGRAM_NAME)
  .description('路由器儿童上网保护控制工具（hag-connect 版）')
  .version(VERSION)
  .option('--tools <json>', '批量执行工具')
  .option('--skill-id <id>', '技能 ID', DEFAULT_SKILL_ID)
  .option('--verbose', '调试模式')
  .action(async (opts) => {
    if (!opts.tools) {
      program.help();
      return;
    }
    const tools = JSON.parse(opts.tools);
    await callRouterClaw(tools, opts.skillId, opts.verbose);
  });

registerCommands(program);

program.parse();

# GKD 整合订阅

把 GitHub 上 10 份主流 GKD 第三方订阅全部下载、去重、合并成一份，附带官方 APK 与使用教程。

> 生成时间：2026-10-23　订阅版本：v1　规则总量：**31,939 条**　覆盖应用：**1,071 个**

---

## 一、GKD 是什么

GKD（搞快点）是一个基于 Android **无障碍服务**的开源屏幕自动化点击工具。免 Root，完全免费开源（GPL-3.0）。

主要用来自动跳过开屏广告、关闭各类弹窗，也能做自动签到、自动确认等自定义操作。它靠「选择器 + 规则」定位屏幕上的按钮并自动点击，规则通过**订阅**远程下发、自动更新。

### 官方地址

| 项目 | 地址 |
|---|---|
| **GKD 官网** | **https://gkd.li/** |
| 官方 GitHub 仓库 | https://github.com/gkd-kit/gkd |
| 官方 Releases（APK 下载） | https://github.com/gkd-kit/gkd/releases |
| 规则审查工具（写规则用） | https://i.gkd.li/ |
| 官方默认订阅（已归档） | https://github.com/gkd-kit/subscription |

### APK 直链

本仓库已内置最新官方 APK，省去你翻 Releases：

| 版本 | 文件 | 大小 | 发布时间 |
|---|---|---|---|
| v1.12.1 | [`apk/gkd-v1.12.1.apk`](apk/gkd-v1.12.1.apk) | 3.14 MB | 2026-05-20 |

下载后直接用手机安装。若提示「禁止安装未知来源应用」，按系统提示临时授权即可。

---

## 二、订阅地址

### 国内推荐（jsDelivr CDN，无需代理）

```
https://cdn.jsdelivr.net/gh/dlzbm/gkd-merged-subscription@main/dist/gkd.json5
```

### 备用（GitHub Raw，国内需代理）

```
https://raw.githubusercontent.com/dlzbm/gkd-merged-subscription/main/dist/gkd.json5
```

> jsDelivr 有缓存，更新后最多滞后 24 小时。想抢先拿最新版用 Raw 源。

---

## 三、怎么用（从零开始）

### 第 1 步：安装 GKD

1. 下载上面的 APK 并安装（或去[官网](https://gkd.li/)下最新版）。
2. 打开 GKD，**打开「无障碍服务」开关** —— 这是必须的，否则什么都做不了。
3. 系统会跳到无障碍设置页，找到 GKD 并开启。弹窗警告点确认（GKD 开源，代码公开）。

### 第 2 步：保活（很重要，不做会被系统杀掉）

小米 / 华为 / OPPO / vivo 等国产 ROM 会主动清理后台，务必做这几步：

- 打开系统「设置 → 应用管理 → GKD → 电池」改成**无限制 / 允许后台高耗电**
- 打开 GKD 的**悬浮窗权限**
- 在多任务界面把 GKD **加锁**（下拉卡片上锁）
- 部分 ROM 还需在「自启动管理」里允许 GKD 自启动

不保活的表现：用着用着突然不跳广告了，回去看 GKD 已经被杀。

### 第 3 步：添加订阅

1. GKD 底部导航栏 → 「**订阅**」
2. 点右下角「**+**」
3. 粘贴订阅地址：
   ```
   https://cdn.jsdelivr.net/gh/dlzbm/gkd-merged-subscription@main/dist/gkd.json5
   ```
4. 点「确定」，等待下载完成（文件 3.6 MB，建议连 WiFi）
5. 列表里出现「GKD整合订阅」，右侧开关打开

### 第 4 步：把分类打开（不装等于白装）

**这是最容易踩的坑。**

本订阅共 **16 个分类**，默认**只有「开屏广告」是开启的**，其余 15 类全部关闭：

| 分类 | 默认 | 分类 | 默认 |
|---|:--:|---|:--:|
| 开屏广告 | ✅ 开 | 分段广告 | ❌ 关 |
| 青少年模式 | ❌ 关 | 功能类 | ❌ 关 |
| 更新提示 | ❌ 关 | 其他 | ❌ 关 |
| 评价提示 | ❌ 关 | 定位提示 | ❌ 关 |
| 通知提示 | ❌ 关 | 全屏弹窗 | ❌ 关 |
| 权限提示 | ❌ 关 | 权限控制 | ❌ 关 |
| 局部广告 | ❌ 关 | 青少年弹窗 | ❌ 关 |
| 全屏广告 | ❌ 关 | 其它 | ❌ 关 |

开启方法：订阅 → GKD整合订阅 → 「**规则类别**」 → 把想要的类别打开。

建议先只开「开屏广告」跑两天，确认没误触，再逐步加「全屏广告」「局部广告」。**不要一上来全开**，规则越多越容易误触、越耗电。

### 第 5 步：验证是否生效

1. 从最近任务里**划掉**一个目标 App（比如微博），再重新打开
2. 出现开屏广告时**不要自己点**，看「跳过」是否被自动点击
3. GKD → 「触发记录」里能看到刚才的操作记录

广告自己倒计时结束**不算**验证成功，必须看到按钮被自动点击。

---

## 四、订阅内容

| 指标 | 数值 |
|---|---|
| 应用数 | 1,071 |
| 应用规则组 | 4,003 |
| 应用规则数 | 31,861 |
| 全局规则组 | 13（78 条） |
| 分类数 | 16 |
| 文件体积 | 3.61 MB |
| 原始规则总量 | 90,883 条 |
| 去重后保留 | 31,939 条（保留率 35%） |

### 合并来源（按优先级）

| # | 仓库 | Star | 状态 | 贡献 |
|---|---|---|---|---|
| 1 | [Lin-arm/GKD_subscription](https://github.com/Lin-arm/GKD_subscription) | 6.2k | 活跃 | 基线，985 应用 |
| 2 | [VolcanoSAhrimp/gkd-rule](https://github.com/VolcanoSAhrimp/gkd-rule) | 19 | 活跃 | +60 应用 |
| 3 | [ganlinte/GKD-subscription](https://github.com/ganlinte/GKD-subscription) | 898 | 活跃 | +54 应用 |
| 4 | [mrlctate/gkd-mrlc](https://github.com/mrlctate/gkd-mrlc) | 146 | 活跃 | +6 应用 |
| 5 | [MengNianxiaoyao/gkd-subscription](https://github.com/MengNianxiaoyao/gkd-subscription) | 476 | 活跃 | +15 应用 |
| 6 | [AIsouler/GKD_subscription](https://github.com/AIsouler/GKD_subscription) | 12k | **已归档** | 规则补充 |
| 7 | [aoguai/subscription](https://github.com/aoguai/subscription) | 1.1k | 活跃 | +1 应用 |
| 8 | [yanmuq/muqi_gkd](https://github.com/yanmuq/muqi_gkd) | 19 | 活跃 | +4 应用 |
| 9 | [LenorEric/GK-Lemon-D](https://github.com/LenorEric/GK-Lemon-D) | 16 | 活跃 | 规则补充 |
| 10 | [Lin-arm/gkd-Rules](https://github.com/Lin-arm/gkd-Rules) | 85 | 活跃 | +8 应用 |

> AIsouler 虽然 star 最高（12k），但仓库已归档且作者自述「已停止维护」，其 886 个应用全部被 Lin-arm 覆盖，网上大量教程还在推它，属过期信息。

---

## 五、合并是怎么做的

脚本：`merge_gkd.py`，校验脚本：`validate_gkd.py`。

1. **按包名聚合** —— 同一个应用的规则组从不同来源汇总到一起
2. **按规则组名归并** —— 同名规则组合并成一个
3. **按语义签名去重** —— 规则签名取 `matches` + `anyMatches` + `excludeMatches` + `activityIds` + `excludeActivityIds` + `action` + `position` + `matchRoot`，`snapshotUrls` / `exampleUrls` 等元数据不计入
4. **重写 key / preKeys** —— 组内优先保留原 key，新 key 从应用级池分配，避免跨源引用失效
5. **剔除 `scopeKeys`** —— 该字段依赖各源自己的分类 key 编号，跨源必失效

### 处理的脏数据

| 类型 | 数量 | 处理方式 |
|---|---|---|
| 重复规则 | 56,816 条 | 丢弃 |
| 空选择器规则（`matches: ""`） | 2,950 条 | 丢弃（无法触发且可能误匹配） |
| 重复规则组 | 72 个 | 丢弃 |
| 空规则应用 | 2 个 | 整包丢弃 |

### 全局规则组策略

全局规则对所有 App 生效，开多了必误触。因此做了一刀切：

- 前 3 个全局组（开屏广告 / 更新提示 / 青少年模式）来自 Lin-arm 基线，**默认开启**
- 其余 10 个来自其他来源，**设 `enable: false` 默认关闭**，需要的自己去「全局规则」里打开

---

## 六、避坑清单

- **别叠加多个大订阅。** 本订阅已包含 10 份来源，再叠加必然重复，卡顿、耗电、误触全来。
- **别把 GitHub 项目主页当订阅地址。** 必须以 `.json5` 结尾才是订阅链接。
- **类别和全局规则组是两个入口。** 类别开了还不管用，去「全局规则」里检查对应规则组。
- **GKD 不是「所有广告一键消失」。** 广告会先出现再被跳过；没有可匹配按钮时仍需手动。
- **首次验证时先关掉其他自动点击工具**（李跳跳等），避免判断干扰。
- **耗电与规则数量正相关。** 按需开启分类，别全开。

---

## 七、仓库结构

```
.
├── README.md
├── dist/
│   ├── gkd.json5            # 订阅规则主文件（3.61 MB）
│   └── gkd.version.json5    # 版本文件，供 GKD 检查更新
├── apk/
│   └── gkd-v1.12.1.apk      # GKD 官方最新版
├── merge_gkd.py             # 合并去重脚本
└── validate_gkd.py          # 订阅校验脚本
```

重新生成：

```bash
pip install json5
# 把各订阅的 dist/*.json5 放进 gkd/ 目录后
python merge_gkd.py
python validate_gkd.py
```

---

## 八、声明

- 本仓库仅做规则聚合与分发，所有规则的著作权归各自原作者所有。
- GKD 本体为开源项目，许可证 GPL-3.0，官方仓库 https://github.com/gkd-kit/gkd。
- 请勿用于任何违反法律法规或服务条款的用途。
- 规则为社区维护，可能存在误触、失效的情况。发现异常可在 GKD 里单独关掉对应应用或规则组，或到 [Issues](https://github.com/dlzbm/gkd-merged-subscription/issues) 反馈。

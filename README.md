# study-plan-six

VeeTalk · 每日学习计划 PRD（StudyPlan）的可交互 Demo + PRD 文档静态站。

部署在 https://study-plan-six.vercel.app

## 索引

| 路径                                                     | 说明                                                       |
| -------------------------------------------------------- | ---------------------------------------------------------- |
| [`/`](https://study-plan-six.vercel.app)                 | 默认首页（指向最新版 PRD）                                  |
| [`/study-plan-6`](https://study-plan-six.vercel.app/study-plan-6) | **v6（最新）**：UI 修复 + EXAM 全动态化（雅思 0-9 分制 + Part 1/2/Mock + 动态雅思报告 + 纯 CSS 动态 Roleplay 场景） |
| [`/study-plan-5`](https://study-plan-six.vercel.app/study-plan-5) | v5：去 ID + 闹钟图标 + Class 简化评分 + EXAM 跳雅思报告 + 历史报告页 |
| [`/study-plan-4`](https://study-plan-six.vercel.app/study-plan-4) | v4：精简版（去技术细节 + 评分公式化 + 埋点统一一张表）     |
| [`/v3`](https://study-plan-six.vercel.app/v3)            | v3：可交互 demo 雏形                                       |
| [`/v2`](https://study-plan-six.vercel.app/v2)            | v2：高保真截图 + 详细页面逻辑                              |
| [`/v1`](https://study-plan-six.vercel.app/v1)            | v1：初版 PRD                                                |

## 文档结构

每份 `study-plan-N.html` 都是**单文件应用**：HTML / CSS / JavaScript / 图片（base64 内嵌）全部打包在同一个文件里，可离线打开。

主要章节：

1. ⚡ **交互 Demo**：左侧手机模拟器 + 右侧控制台，覆盖 0/3 → 3/3 → 切换 Goal → Daily / IELTS Report → 历史报告 全状态
2. **一、为什么做**：现状痛点（学习路径太散 / 跨模块协同失败 / 启动→完成大流失 / goal 信号被浪费 / 无反馈闭环）
3. **二、目标与期望效果**：3 北极星指标 + 7 支撑指标 + 反向监控
4. **三、需求详细描述**（11 屏 × 2 列）
5. **四、评分机制**：Words / Class / Roleplay / IELTS 公式 + Today's habits 三大指标
6. **五、埋点规范**：统一一张表（page / action / type / sub_type / result / int / content）
7. **六、风险与依赖**

## 本地预览

```bash
cd deploy
python3 -m http.server 8080
# 浏览器打开 http://localhost:8080/study-plan-6.html
```

## 部署

仓库根目录是 Vercel 项目 root；`vercel.json` 配置了从 `/study-plan-N` 到 `/study-plan-N.html` 的 rewrite。

```bash
cd deploy
vercel --prod
```

## 源文件

源 HTML 和图片在父仓库 `data/` 下；通过 `scripts/inline_html_images.py` 把本地图片 base64 内嵌后输出到本目录。

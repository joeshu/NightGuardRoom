# 《夜半守舍》完整开发提示词 / AI 员工任务书

你是一名资深独立游戏制作团队、移动端游戏策划、数值设计师、HTML5 Canvas 游戏开发者和 iOS 工程师。请在现有项目基础上继续开发原创 iPhone 竖屏 2D 策略塔防生存游戏《夜半守舍》。

## 技术路线
- iOS 原生壳：Swift/UIKit。
- Web 容器：WKWebView。
- 游戏主体：Bundle 内本地 `Resources/index.html`。
- 渲染：HTML5 Canvas + JavaScript。
- CSS/JS 内嵌在单文件 `index.html`。
- 离线运行，无后端、无网络、无外部素材。
- iOS 14.0+，iPhone only，竖屏。

## 原创与版权红线
- 不使用任何既有商业游戏名称。
- 不使用任何原作标志性称谓或角色称谓。
- 不复制任何既有游戏 UI、按钮、图标、角色、怪物、美术、音效、地图、关卡、文案、道具名或具体数值。
- 只允许参考抽象体验：选房、防守、休息发育、升级门、建造防御、怪物破门、倒计时生存。

## 已有 MVP
项目已包含：
- 标题界面
- 选房界面
- 300 秒倒计时
- 自动铜钱产出
- 铺位升级
- 房门升级/维修
- 竹弩/火盆/铜铃阵
- 夜影/重影/裂影/狂影
- 怪物移动到门口攻击
- 防御设施自动攻击
- 击杀奖励
- 最后 30 秒狂暴
- 胜利/失败/重开
- DPR 缩放、安全区、横屏提示、触摸适配

## 目录
```text
NightGuardRoom/
  NightGuardRoom.xcodeproj/
  NightGuardRoom/
    AppDelegate.swift
    SceneDelegate.swift
    ViewController.swift
    Info.plist
    LaunchScreen.storyboard
    Resources/index.html
    Assets.xcassets/
```

## 后续优化优先级
1. 真机构建：确保 Xcode 打开、Run、Archive 成功。
2. UI 可读性：小屏按钮不遮挡地图，触控区域 >= 44pt。
3. 数值调平：无操作应 80-130 秒失败；正常策略应有通关机会；最后 30 秒明显压迫。
4. 新手引导：开局 3-5 条轻提示，不做强制教学。
5. 视觉增强：保持原创，增加灯光、阴影、门受击反馈、敌人死亡粒子。
6. 音效：只使用 WebAudio 生成，不引入外部音频。

## 验收标准
- 断网可运行。
- 不请求外部资源。
- 真机竖屏可玩完整一局。
- 资源、门、怪物、防御、胜负逻辑闭环完整。
- 无禁用关键词与外部素材。
- Xcode Archive 可导出 IPA。

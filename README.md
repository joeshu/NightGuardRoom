# 夜半守舍 NightGuardRoom

原创 iPhone 竖屏 2D 策略塔防生存游戏 MVP。技术方案：Swift UIKit + WKWebView 加载 Bundle 内 `Resources/index.html`，核心玩法由本地 HTML5 Canvas + JavaScript 实现。

## 运行
1. 用 Xcode 打开 `NightGuardRoom.xcodeproj`。
2. 修改 Bundle Identifier，例如 `com.example.nightguardroom`。
3. Signing & Capabilities 选择你的 Team。
4. 选择 iPhone 模拟器或真机，点击 Run。

## 打包 IPA
1. 选择 Any iOS Device 或连接真机。
2. Product > Archive。
3. Organizer > Distribute App。
4. 按用途选择 Development / Ad Hoc / TestFlight / App Store Connect。
5. 导出 IPA。

## 版权说明
本项目为原创作品，仅参考“房间防守、休息发育、升级门、炮塔防守、倒计时生存”等抽象玩法结构；未使用任何既有游戏名称、角色、UI、图标、音频、图片或截图素材。

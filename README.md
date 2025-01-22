# Sprunkr - 在线音乐游戏平台 (v0.2.0)

Sprunkr是一个充满创意的在线音乐游戏平台，让用户可以通过简单有趣的方式创作音乐。

## 功能特点

### 1. 游戏主题
- 丰富多样的游戏主题（包括 Lily, Fiddlebops, Megalovania, Sprunkr, Spruted, Banana, Garnold, Ketchup, Retake, Parodybox, Pyramixed）
- 每个主题都有独特的视觉和音效设计
- 支持在线游玩和体验

### 2. 核心功能
- FAQ 帮助中心
- 多语言支持（英语和西班牙语）
- 响应式设计，完美支持移动端
- 优化的游戏性能

## 技术栈
- 后端：Flask (Python)
- 前端：HTML + Tailwind CSS + JavaScript
- 部署：Vercel

## 项目结构

```
sprunkr/
├── app.py              # Flask应用主文件
├── requirements.txt    # Python依赖
├── static/            # 静态资源
│   ├── css/          # 样式文件
│   ├── js/           # JavaScript文件
│   ├── images/       # 图片资源
│   └── data/         # 配置数据（如翻译文件）
└── templates/         # HTML模板
    ├── base.html     # 基础模板
    ├── components/   # 可重用组件
    └── *.html        # 页面模板
```

## 快速开始

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 设置环境变量：
- 复制 `.env.example` 为 `.env`
- 填写必要的环境变量

3. 运行应用：
```bash
python app.py
```

## 主要页面

- 首页 (`/`)：游戏主页面
- 游戏页面：
  - `/sprunki-lily`
  - `/sprunki-fiddlebops`
  - `/sprunki-megalovania`
  - `/sprunki-sprunkr`
  - `/sprunki-spruted`
  - `/sprunki-banana`
  - `/sprunki-garnold`
  - `/sprunki-ketchup`
  - `/sprunki-retake-but-human`
  - `/sprunki-parodybox`
  - `/sprunki-pyramixed`
- 其他页面：
  - `/about`：关于我们
  - `/faq`：常见问题
  - `/privacy-policy`：隐私政策
  - `/terms-of-service`：服务条款

## 性能优化

- 使用 Tailwind CSS 实现高效的样式管理
- 实现响应式设计，确保移动端体验
- 优化图片和媒体资源加载
- 使用语义化 HTML 标签，提升 SEO 效果

## 版本历史

### v0.2.0 (2025-01-22)
- 重构日志系统，改进日志配置管理
- 新增 Sprunki Sprunksters 游戏主题
- 优化页面UI设计，添加现代化渐变效果
- 改进SEO配置
- 优化FAQ系统
- 完善游戏页面响应式布局

### v0.1.0 (2025-01-16)
- 初始版本发布
- 实现基础游戏功能
- 支持11个游戏主题
- 添加多语言支持
- 实现响应式设计
- 优化 SEO 设置

## 浏览器支持
- Chrome (推荐)
- Firefox
- Safari
- Edge

## 许可证
版权所有 2025 Sprunkr

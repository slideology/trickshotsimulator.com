# Sprunkr - 在线音乐游戏平台

Sprunkr是一个充满创意的在线音乐游戏平台，让用户可以通过简单有趣的方式创作音乐。

## 项目功能

### 1. 音乐游戏
- 多个独特版本的游戏主题（Lily, Fiddlebops, Megalovania等）
- 每个版本都有独特的视觉和音效设计
- 支持在线保存和分享创作

### 2. 社区功能
- 用户排行榜
- 活动中心
- 社区讨论
- 用户反馈系统

### 3. 技术特点
- 支持多语言（英语和西班牙语）
- 响应式设计，支持各种设备
- 安全的用户数据保护
- 高性能的音频处理

## 项目结构

```
sprunkr/
├── app.py              # 主应用程序文件
├── models.py           # 数据模型定义
├── init_db.py          # 数据库初始化
├── requirements.txt    # 项目依赖
├── static/            # 静态资源文件
│   ├── css/          # 样式文件
│   ├── js/           # JavaScript文件
│   ├── images/       # 图片资源
│   └── data/         # 配置数据
└── templates/         # HTML模板
    ├── base.html     # 基础模板
    └── game/         # 游戏相关模板
```

## 如何运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 设置环境变量：
- 复制 `.env.example` 为 `.env`
- 填写必要的环境变量

3. 初始化数据库：
```bash
python init_db.py
```

4. 运行应用：
```bash
python app.py
```

## 开发指南

### 添加新游戏版本
1. 在 `templates/` 目录下创建新的游戏模板
2. 在 `app.py` 中添加对应的路由
3. 在 `static/data/translations.json` 添加相关翻译
4. 更新游戏列表配置

### 性能优化建议
1. 使用CDN加载静态资源
2. 压缩CSS和JavaScript文件
3. 优化图片大小和格式
4. 实施浏览器缓存策略

## 待优化项目
1. 前端框架升级到Next.js + React
2. 引入Tailwind CSS优化样式系统
3. 添加更多游戏主题
4. 优化移动端体验
5. 增强社区互动功能

## 联系方式
如有问题或建议，请通过网站的反馈系统联系我们。

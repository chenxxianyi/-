# 知识型阅读工作台 - 后端

知识型阅读工作台（Knowledge Reader）后端服务，基于 FastAPI 构建。

## 技术栈

- Python 3.11+
- FastAPI
- SQLAlchemy 2.x
- MySQL 8
- Redis
- MinIO
- Celery
- Alembic
- Docker Compose

## 快速开始

### 环境要求

- Python 3.11+
- MySQL 8
- Redis 7+
- MinIO

### 本地开发

1. 克隆项目并进入 backend 目录：

```bash
cd backend
```

2. 创建虚拟环境：

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

4. 配置环境变量：

```bash
cp .env.example .env
# 编辑 .env 填入实际配置
```

5. 创建数据库：

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS knowledge_reader CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

6. 运行数据库迁移：

```bash
alembic upgrade head
```

7. 启动服务：

```bash
uvicorn app.main:app --reload --port 8000
```

8. 访问 API 文档：

- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Docker Compose 启动

在项目根目录执行：

```bash
docker compose up --build
```

这将启动所有服务：
- MySQL (端口 3306)
- Redis (端口 6379)
- MinIO (端口 9000, 控制台 9001)
- Backend (端口 8000)
- Celery Worker

## 项目结构

```
backend/
  app/
    main.py                 # FastAPI 应用入口
    core/
      config.py             # 配置管理
      security.py           # 安全工具
      dependencies.py       # FastAPI 依赖
      exceptions.py         # 自定义异常
    db/
      session.py            # 数据库连接
      base.py               # SQLAlchemy Base
    models/                 # 数据库模型
    schemas/                # Pydantic 数据校验
    api/
      v1/
        router.py           # 路由汇总
        endpoints/           # API 端点
    services/               # 业务逻辑层
    repositories/           # 数据访问层
    utils/                  # 工具函数
    tasks/                  # Celery 异步任务
  alembic/                  # 数据库迁移
  tests/                    # 单元测试
```

## API 端点

### 健康检查

- `GET /health` - 健康检查

### 认证

- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户

### 文档管理

- `GET /api/documents` - 文档列表
- `GET /api/documents/{id}` - 文档详情
- `POST /api/documents/upload` - 上传文档
- `PUT /api/documents/{id}` - 更新文档（重命名）
- `DELETE /api/documents/{id}` - 删除文档（软删除）
- `GET /api/documents/{id}/content` - 文档内容
- `PUT /api/documents/{id}/read-position` - 保存阅读进度

### 批注

- `GET /api/documents/{id}/annotations` - 批注列表
- `POST /api/documents/{id}/annotations` - 创建批注
- `PUT /api/documents/{id}/annotations/{ann_id}` - 更新批注
- `DELETE /api/documents/{id}/annotations/{ann_id}` - 删除批注

### 笔记

- `GET /api/notes` - 笔记列表
- `POST /api/notes` - 创建笔记
- `GET /api/notes/{id}` - 笔记详情
- `PUT /api/notes/{id}` - 更新笔记
- `DELETE /api/notes/{id}` - 删除笔记
- `POST /api/notes/from-annotation` - 从批注生成笔记

### AI 助手

- `POST /api/documents/{id}/ai/ask` - 问答（按文档）
- `POST /api/ai/summary` - 文档摘要
- `POST /api/ai/explain` - 文本解释
- `POST /api/ai/translate` - 文本翻译
- `POST /api/ai/chat` - 对话

## 数据库迁移

### 创建新的迁移

```bash
alembic revision --autogenerate -m "描述变更"
```

### 执行迁移

```bash
alembic upgrade head
```

### 回滚迁移

```bash
alembic downgrade -1
```

## 运行测试

```bash
pytest tests/ -v
```

## 统一响应格式

所有 API 响应使用统一格式：

```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

错误响应：

```json
{
  "code": 401,
  "message": "Unauthorized",
  "data": null
}
```

## MVP 验收清单

- [x] `/health` 正常返回
- [x] `/docs` 可以访问 Swagger
- [x] 可以注册用户
- [x] 可以登录并获得 JWT
- [x] `/auth/me` 可以返回当前用户
- [x] 密码以 hash 保存
- [x] 可以上传 PDF / Markdown / TXT / DOCX
- [x] 文件保存到 MinIO
- [x] 文件元信息保存到 MySQL
- [x] 可以查询文件列表
- [x] 可以查询文件详情
- [x] 可以获取文件内容或预览 URL
- [x] 可以重命名文件
- [x] 可以软删除文件
- [x] 可以保存阅读进度
- [x] 可以创建批注
- [x] 可以查询当前文档批注
- [x] 可以更新批注
- [x] 可以删除批注
- [x] 可以创建笔记
- [x] 可以编辑笔记
- [x] 可以删除笔记
- [x] 可以从批注生成笔记
- [x] AI 总结接口返回 mock 数据
- [x] AI 解释接口返回 mock 数据
- [x] AI 翻译接口返回 mock 数据
- [x] AI 问答接口返回 mock 数据
- [x] 所有文档、批注、笔记接口完成用户权限校验
- [x] Docker Compose 可以启动后端依赖服务
- [x] Alembic 迁移可执行
- [x] README 写清楚后端启动和迁移方式

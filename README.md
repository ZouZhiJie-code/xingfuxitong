# 幸福设计系统（初始化骨架）

## 目录
- `frontend/`: H5 前端（React + Vite）骨架，用于首期业务验证。
- `backend/`: FastAPI 后端骨架，提供健康检查、对话流式接口、日记示例接口。

## 快速启动

### 1) 后端
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2) 前端
```bash
cd frontend
npm install
npm run dev
```

- 前端地址：`http://localhost:5173`
- 后端地址：`http://localhost:8000`
- 健康检查：`http://localhost:8000/health`

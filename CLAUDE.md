# CLAUDE.md - ラクマネ プロジェクト設定

## プロジェクト概要

プロジェクト名: ラクマネ（デジタル商品販売支援システム）
目的: AIを活用してデジタル商品を効率的に作成・販売し、不労所得を実現する

---

## 技術スタック

```yaml
frontend:
  framework: React 18 + TypeScript 5
  ui: MUI v6
  build: Vite 5
  routing: React Router v6
  state: Zustand
  server-state: React Query
  chart: Recharts

backend:
  language: Python 3.11+
  framework: FastAPI
  server: Uvicorn
  orm: SQLAlchemy

database:
  primary: PostgreSQL (Neon)

infrastructure:
  frontend: Vercel
  backend: Google Cloud Run
```

---

## ポート設定

```yaml
frontend: 3847
backend: 8291
# 複数プロジェクト並行開発のため、一般的でないポートを使用
```

---

## テスト認証情報

```yaml
開発用アカウント:
  email: test@rakumane.local
  password: RakuDev2026!
```

---

## 環境変数

```yaml
設定ファイル: .env.local（ルートのみ）
設定モジュール: src/config/index.ts（frontend）, src/config.py（backend）
ハードコード禁止: 環境変数はconfig経由のみ
```

### 必要な環境変数

```bash
# Frontend (.env.local)
VITE_API_URL=http://localhost:8291

# Backend (.env)
ANTHROPIC_API_KEY=your_claude_api_key
DATABASE_URL=postgresql://...
GUMROAD_CLIENT_ID=optional
GUMROAD_CLIENT_SECRET=optional
```

---

## 命名規則

```yaml
ファイル:
  コンポーネント: PascalCase.tsx (例: ProductGenerator.tsx)
  その他: camelCase.ts (例: apiClient.ts)
  スタイル: camelCase.module.css

変数/関数: camelCase
定数: UPPER_SNAKE_CASE
型/インターフェース: PascalCase
コンポーネント: PascalCase
```

---

## 型定義

```yaml
frontend: src/types/index.ts
backend: src/types.py
# 両ファイルは常に同期すること
```

---

## コード品質基準

```yaml
関数行数: 100行以下
ファイル行数: 700行以下
複雑度: 10以下
行長: 120文字
```

---

## ディレクトリ構造

```
/
├── CLAUDE.md
├── docs/
│   ├── requirements.md
│   └── SCOPE_PROGRESS.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── types/
│   │   ├── config/
│   │   └── utils/
│   ├── package.json
│   └── vite.config.ts
└── backend/
    ├── src/
    │   ├── routers/
    │   ├── services/
    │   ├── models/
    │   └── config.py
    ├── requirements.txt
    └── main.py
```

---

## API設計規約

```yaml
ベースパス: /api
バージョニング: なし（MVP版）
レスポンス形式: JSON
エラーレスポンス:
  format: { "detail": "エラーメッセージ" }
  codes: 400, 401, 404, 500
```

---

## Git規約

```yaml
ブランチ戦略: GitHub Flow
  main: 本番環境
  feature/*: 機能開発

コミットメッセージ:
  format: "<type>: <subject>"
  types:
    - feat: 新機能
    - fix: バグ修正
    - docs: ドキュメント
    - style: フォーマット
    - refactor: リファクタリング
    - test: テスト
    - chore: その他
```

---

## 最新技術情報（知識カットオフ対応）

### Gumroad API
- エンドポイント: https://api.gumroad.com/v2/
- 認証: Bearer Token
- 売上取得: GET /sales
- Rate Limit: 明示なし（常識的な範囲で）

### Claude API (2026年版)
- モデル: claude-haiku-4-5-20251101（コスト効率重視）
- 入力: $1/100万トークン
- 出力: $5/100万トークン
- プロンプトキャッシング利用推奨

---

## 開発コマンド

```bash
# Frontend
cd frontend
npm install
npm run dev      # 開発サーバー起動 (port 3847)
npm run build    # ビルド
npm run lint     # Lint実行

# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8291  # 開発サーバー起動
```

---

## 注意事項

1. **APIキーの取り扱い**
   - Claude API Keyは絶対にフロントエンドに露出させない
   - .env ファイルは .gitignore に必ず含める

2. **Gumroad連携**
   - ユーザーのアクセストークンはローカルストレージに保存
   - 将来的には暗号化を検討

3. **AI生成のレート制限**
   - 連続生成時は1秒以上の間隔を空ける
   - エラー時は指数バックオフでリトライ

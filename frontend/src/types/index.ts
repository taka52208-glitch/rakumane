// 商品生成リクエスト
export interface GenerateRequest {
  category: ProductCategory;
  target: string;
  additionalNotes?: string;
}

// 商品生成レスポンス
export interface GenerateResponse {
  productNames: string[];
  description: string;
  suggestedPrice: number;
  tags: string[];
}

// 商品カテゴリ
export type ProductCategory =
  | 'prompt'        // プロンプト集
  | 'notion'        // Notionテンプレート
  | 'canva'         // Canvaテンプレート
  | 'ebook'         // 電子書籍
  | 'excel'         // Excelテンプレート
  | 'spreadsheet'   // スプレッドシート
  | 'powerpoint'    // PowerPointテンプレート
  | 'figma'         // Figmaテンプレート
  | 'checklist'     // チェックリスト/ワークシート
  | 'linestamp'     // LINEスタンプ
  | 'icon'          // アイコンセット
  | 'course';       // オンラインコース

// カテゴリ表示名
export const CATEGORY_LABELS: Record<ProductCategory, string> = {
  prompt: 'AIプロンプト集',
  notion: 'Notionテンプレート',
  canva: 'Canvaテンプレート',
  ebook: '電子書籍',
  excel: 'Excelテンプレート',
  spreadsheet: 'スプレッドシート',
  powerpoint: 'PowerPointテンプレート',
  figma: 'Figmaテンプレート',
  checklist: 'チェックリスト/ワークシート',
  linestamp: 'LINEスタンプ',
  icon: 'アイコンセット',
  course: 'オンラインコース',
};

// Gumroad売上データ
export interface Sale {
  id: string;
  productName: string;
  price: number;
  saleTimestamp: string;
  email: string;
}

// ダッシュボードサマリー
export interface DashboardSummary {
  totalSales: number;
  totalRevenue: number;
  monthlyGoal: number;
  salesByProduct: { productName: string; count: number; revenue: number }[];
  dailySales: { date: string; revenue: number }[];
}

// 設定
export interface Settings {
  gumroadToken: string;
  monthlyGoal: number;
}

// コンテンツ生成リクエスト
export interface GenerateContentRequest {
  category: ProductCategory;
  productName: string;
  target: string;
  additionalNotes?: string;
}

// コンテンツ生成レスポンス
export interface GenerateContentResponse {
  content: string;
  filename: string;
}

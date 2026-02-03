import { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  FormControl,
  Grid,
  IconButton,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Typography,
  Chip,
  Snackbar,
  Alert,
  CircularProgress,
  Divider,
  Paper,
} from '@mui/material';
import {
  AutoAwesome as GenerateIcon,
  ContentCopy as CopyIcon,
  Refresh as RefreshIcon,
  Download as DownloadIcon,
  AutoFixHigh as ContentIcon,
  Storefront as StorefrontIcon,
} from '@mui/icons-material';
import { useMutation } from '@tanstack/react-query';
import axios from 'axios';
import { config } from '../config';
import type { GenerateRequest, GenerateResponse, GenerateContentRequest, GenerateContentResponse, ProductCategory } from '../types';
import { CATEGORY_LABELS } from '../types';

const generateProduct = async (request: GenerateRequest): Promise<GenerateResponse> => {
  const response = await axios.post(`${config.apiUrl}/api/generate`, request);
  return response.data;
};

const generateContent = async (request: GenerateContentRequest): Promise<GenerateContentResponse> => {
  const response = await axios.post(`${config.apiUrl}/api/generate-content`, request);
  return response.data;
};

export const Generator = () => {
  const [category, setCategory] = useState<ProductCategory>('prompt');
  const [target, setTarget] = useState('');
  const [additionalNotes, setAdditionalNotes] = useState('');
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' as 'success' | 'error' });
  const [selectedProductName, setSelectedProductName] = useState<string>('');

  const mutation = useMutation({
    mutationFn: generateProduct,
    onError: () => {
      setSnackbar({ open: true, message: '生成に失敗しました。バックエンドが起動しているか確認してください。', severity: 'error' });
    },
    onSuccess: (data) => {
      if (data.productNames.length > 0) {
        setSelectedProductName(data.productNames[0]);
      }
    },
  });

  const contentMutation = useMutation({
    mutationFn: generateContent,
    onError: () => {
      setSnackbar({ open: true, message: 'コンテンツ生成に失敗しました。', severity: 'error' });
    },
    onSuccess: () => {
      setSnackbar({ open: true, message: 'コンテンツを生成しました', severity: 'success' });
    },
  });

  const handleGenerate = () => {
    if (!target.trim()) {
      setSnackbar({ open: true, message: 'ターゲットを入力してください', severity: 'error' });
      return;
    }
    mutation.mutate({ category, target, additionalNotes: additionalNotes || undefined });
  };

  const handleCopy = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    setSnackbar({ open: true, message: `${label}をコピーしました`, severity: 'success' });
  };

  const handleGenerateContent = () => {
    if (!selectedProductName) {
      setSnackbar({ open: true, message: '商品名を選択してください', severity: 'error' });
      return;
    }
    contentMutation.mutate({
      category,
      productName: selectedProductName,
      target,
      additionalNotes: additionalNotes || undefined,
    });
  };

  const handleDownload = () => {
    if (!contentMutation.data) return;
    const blob = new Blob([contentMutation.data.content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = contentMutation.data.filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    setSnackbar({ open: true, message: 'ダウンロードしました', severity: 'success' });
  };

  const handleCopyContent = () => {
    if (!contentMutation.data) return;
    navigator.clipboard.writeText(contentMutation.data.content);
    setSnackbar({ open: true, message: '全文をコピーしました', severity: 'success' });
  };

  const handlePublishToGumroad = () => {
    if (!mutation.data || !contentMutation.data) return;

    const productInfo = `商品名: ${selectedProductName}

説明文:
${mutation.data.description}

価格: ${mutation.data.suggestedPrice}円

タグ: ${mutation.data.tags.join(', ')}`;

    navigator.clipboard.writeText(productInfo);
    setSnackbar({ open: true, message: '商品情報をコピーしました。Gumroadで貼り付けてください', severity: 'success' });

    window.open('https://app.gumroad.com/products/new', '_blank');
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        AIで売れる商品を生成
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        カテゴリとターゲットを入力するだけで、商品名・説明文・価格・タグを自動生成します
      </Typography>

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 5 }}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                入力
              </Typography>

              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>カテゴリ</InputLabel>
                <Select
                  value={category}
                  label="カテゴリ"
                  onChange={(e) => setCategory(e.target.value as ProductCategory)}
                >
                  {Object.entries(CATEGORY_LABELS).map(([value, label]) => (
                    <MenuItem key={value} value={value}>
                      {label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              <TextField
                fullWidth
                label="ターゲット"
                placeholder="例: 副業で稼ぎたい会社員"
                value={target}
                onChange={(e) => setTarget(e.target.value)}
                sx={{ mb: 2 }}
              />

              <TextField
                fullWidth
                label="追加の要望（任意）"
                placeholder="例: 初心者向けにシンプルに"
                value={additionalNotes}
                onChange={(e) => setAdditionalNotes(e.target.value)}
                multiline
                rows={2}
                sx={{ mb: 3 }}
              />

              <Button
                variant="contained"
                size="large"
                fullWidth
                startIcon={mutation.isPending ? <CircularProgress size={20} color="inherit" /> : <GenerateIcon />}
                onClick={handleGenerate}
                disabled={mutation.isPending}
              >
                {mutation.isPending ? '生成中...' : '生成する'}
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, md: 7 }}>
          <Card sx={{ minHeight: 400 }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">生成結果</Typography>
                {mutation.data && (
                  <IconButton onClick={() => handleGenerate()} size="small" title="再生成">
                    <RefreshIcon />
                  </IconButton>
                )}
              </Box>

              {!mutation.data && !mutation.isPending && (
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 300, color: 'text.secondary' }}>
                  <Typography>左のフォームから生成してください</Typography>
                </Box>
              )}

              {mutation.isPending && (
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 300 }}>
                  <CircularProgress />
                </Box>
              )}

              {mutation.data && (
                <Box>
                  <Box sx={{ mb: 3 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="subtitle2" color="text.secondary">商品名（3案）</Typography>
                      <IconButton size="small" onClick={() => handleCopy(mutation.data.productNames.join('\n'), '商品名')}>
                        <CopyIcon fontSize="small" />
                      </IconButton>
                    </Box>
                    {mutation.data.productNames.map((name, i) => (
                      <Typography key={i} variant="body1" sx={{ fontWeight: 600, mb: 0.5 }}>
                        {i + 1}. {name}
                      </Typography>
                    ))}
                  </Box>

                  <Box sx={{ mb: 3 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="subtitle2" color="text.secondary">商品説明文</Typography>
                      <IconButton size="small" onClick={() => handleCopy(mutation.data.description, '説明文')}>
                        <CopyIcon fontSize="small" />
                      </IconButton>
                    </Box>
                    <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                      {mutation.data.description}
                    </Typography>
                  </Box>

                  <Box sx={{ mb: 3 }}>
                    <Typography variant="subtitle2" color="text.secondary">推奨価格</Typography>
                    <Typography variant="h5" color="primary.main" sx={{ fontWeight: 700 }}>
                      ¥{mutation.data.suggestedPrice.toLocaleString()}
                    </Typography>
                  </Box>

                  <Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="subtitle2" color="text.secondary">タグ</Typography>
                      <IconButton size="small" onClick={() => handleCopy(mutation.data.tags.join(', '), 'タグ')}>
                        <CopyIcon fontSize="small" />
                      </IconButton>
                    </Box>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
                      {mutation.data.tags.map((tag) => (
                        <Chip key={tag} label={tag} size="small" />
                      ))}
                    </Box>
                  </Box>

                  {/* コンテンツ生成ボタン */}
                  <Divider sx={{ my: 3 }} />
                  <Box>
                    <FormControl fullWidth sx={{ mb: 2 }}>
                      <InputLabel size="small">生成する商品名を選択</InputLabel>
                      <Select
                        size="small"
                        value={selectedProductName}
                        label="生成する商品名を選択"
                        onChange={(e) => setSelectedProductName(e.target.value)}
                      >
                        {mutation.data.productNames.map((name, i) => (
                          <MenuItem key={i} value={name}>{name}</MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                    <Button
                      variant="contained"
                      fullWidth
                      startIcon={contentMutation.isPending ? <CircularProgress size={20} color="inherit" /> : <ContentIcon />}
                      onClick={handleGenerateContent}
                      disabled={contentMutation.isPending || !selectedProductName}
                      sx={{
                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        '&:hover': { opacity: 0.9 },
                      }}
                    >
                      {contentMutation.isPending ? 'コンテンツ生成中...' : '実物コンテンツを生成する'}
                      <Chip label="NEW" size="small" sx={{ ml: 1, bgcolor: 'rgba(255,255,255,0.2)', color: 'white', fontSize: '10px', height: '20px' }} />
                    </Button>
                  </Box>

                  {/* コンテンツプレビュー */}
                  {contentMutation.data && (
                    <Box sx={{ mt: 3 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                        <Typography variant="subtitle1" sx={{ color: '#667eea', fontWeight: 500 }}>
                          生成されたコンテンツ
                        </Typography>
                        <Chip label="生成完了" size="small" color="success" />
                      </Box>
                      <Paper
                        variant="outlined"
                        sx={{
                          p: 2,
                          maxHeight: 400,
                          overflow: 'auto',
                          bgcolor: '#fafafa',
                          fontFamily: 'monospace',
                          fontSize: '13px',
                          lineHeight: 1.8,
                          whiteSpace: 'pre-wrap',
                        }}
                      >
                        {contentMutation.data.content}
                      </Paper>
                      <Box sx={{ display: 'flex', gap: 1, mt: 2, flexWrap: 'wrap' }}>
                        <Button
                          variant="contained"
                          color="success"
                          startIcon={<DownloadIcon />}
                          onClick={handleDownload}
                        >
                          ダウンロード (.txt)
                        </Button>
                        <Button
                          variant="outlined"
                          startIcon={<CopyIcon />}
                          onClick={handleCopyContent}
                        >
                          全文コピー
                        </Button>
                        <Button
                          variant="outlined"
                          startIcon={<RefreshIcon />}
                          onClick={handleGenerateContent}
                          disabled={contentMutation.isPending}
                        >
                          再生成
                        </Button>
                      </Box>
                      <Box sx={{ mt: 2 }}>
                        <Button
                          variant="contained"
                          fullWidth
                          startIcon={<StorefrontIcon />}
                          onClick={handlePublishToGumroad}
                          sx={{
                            background: 'linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%)',
                            '&:hover': { background: 'linear-gradient(135deg, #ee5a5a 0%, #dd4a4a 100%)' },
                            py: 1.5,
                            fontSize: '1rem',
                          }}
                        >
                          Gumroadで出品する
                        </Button>
                        <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1, textAlign: 'center' }}>
                          商品情報をコピーしてGumroadの商品作成ページを開きます
                        </Typography>
                      </Box>
                    </Box>
                  )}
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={3000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert severity={snackbar.severity} onClose={() => setSnackbar({ ...snackbar, open: false })}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

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
} from '@mui/material';
import {
  AutoAwesome as GenerateIcon,
  ContentCopy as CopyIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { useMutation } from '@tanstack/react-query';
import axios from 'axios';
import { config } from '../config';
import type { GenerateRequest, GenerateResponse, ProductCategory } from '../types';
import { CATEGORY_LABELS } from '../types';

const generateProduct = async (request: GenerateRequest): Promise<GenerateResponse> => {
  const response = await axios.post(`${config.apiUrl}/api/generate`, request);
  return response.data;
};

export const Generator = () => {
  const [category, setCategory] = useState<ProductCategory>('prompt');
  const [target, setTarget] = useState('');
  const [additionalNotes, setAdditionalNotes] = useState('');
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' as 'success' | 'error' });

  const mutation = useMutation({
    mutationFn: generateProduct,
    onError: () => {
      setSnackbar({ open: true, message: '生成に失敗しました。バックエンドが起動しているか確認してください。', severity: 'error' });
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

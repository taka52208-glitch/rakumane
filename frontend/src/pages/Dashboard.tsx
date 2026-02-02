import { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Grid,
  LinearProgress,
  TextField,
  Typography,
  List,
  ListItem,
  ListItemText,
  Alert,
} from '@mui/material';
import {
  TrendingUp as RevenueIcon,
  ShoppingCart as SalesIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import axios from 'axios';
import { config } from '../config';
import type { DashboardSummary, Settings } from '../types';

const fetchDashboard = async (): Promise<DashboardSummary> => {
  const response = await axios.get(`${config.apiUrl}/api/sales`);
  return response.data;
};

const saveSettings = async (settings: Settings): Promise<void> => {
  await axios.post(`${config.apiUrl}/api/settings`, settings);
};

export const Dashboard = () => {
  const queryClient = useQueryClient();
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [gumroadToken, setGumroadToken] = useState('');
  const [monthlyGoal, setMonthlyGoal] = useState(100000);

  const { data, isLoading, error } = useQuery({
    queryKey: ['dashboard'],
    queryFn: fetchDashboard,
    refetchInterval: 5 * 60 * 1000,
  });

  const settingsMutation = useMutation({
    mutationFn: saveSettings,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      setSettingsOpen(false);
    },
  });

  const handleSaveSettings = () => {
    settingsMutation.mutate({ gumroadToken, monthlyGoal });
  };

  const achievementRate = data ? Math.min((data.totalRevenue / data.monthlyGoal) * 100, 100) : 0;

  const formatCurrency = (value: number) => {
    return `¥${value.toLocaleString()}`;
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h5" gutterBottom>
            売上ダッシュボード
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Gumroadの売上をリアルタイムで確認
          </Typography>
        </Box>
        <Button startIcon={<SettingsIcon />} onClick={() => setSettingsOpen(true)}>
          設定
        </Button>
      </Box>

      {error && (
        <Alert severity="warning" sx={{ mb: 3 }}>
          データを取得できません。設定からGumroadトークンを入力してください。
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <RevenueIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="body2" color="text.secondary">
                  今月の売上
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 700 }}>
                {formatCurrency(data?.totalRevenue || 0)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <SalesIcon color="secondary" sx={{ mr: 1 }} />
                <Typography variant="body2" color="text.secondary">
                  販売数
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 700 }}>
                {data?.totalSales || 0}件
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, md: 4 }}>
          <Card>
            <CardContent>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                目標達成率
              </Typography>
              <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
                {achievementRate.toFixed(1)}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={achievementRate}
                sx={{ height: 8, borderRadius: 4 }}
              />
              <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                目標: {formatCurrency(data?.monthlyGoal || monthlyGoal)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, md: 8 }}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                売上推移
              </Typography>
              <Box sx={{ height: 300 }}>
                {isLoading ? (
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                    <Typography color="text.secondary">読み込み中...</Typography>
                  </Box>
                ) : data?.dailySales && data.dailySales.length > 0 ? (
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data.dailySales}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <Tooltip formatter={(value) => formatCurrency(Number(value))} />
                      <Line type="monotone" dataKey="revenue" stroke="#2563eb" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                ) : (
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                    <Typography color="text.secondary">データがありません</Typography>
                  </Box>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, md: 4 }}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                商品別ランキング
              </Typography>
              {data?.salesByProduct && data.salesByProduct.length > 0 ? (
                <List dense>
                  {data.salesByProduct.slice(0, 5).map((item, index) => (
                    <ListItem key={item.productName} sx={{ px: 0 }}>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <Typography
                              variant="body2"
                              sx={{
                                width: 24,
                                height: 24,
                                borderRadius: '50%',
                                bgcolor: index < 3 ? 'primary.main' : 'grey.300',
                                color: index < 3 ? 'white' : 'text.primary',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                mr: 1,
                                fontSize: 12,
                              }}
                            >
                              {index + 1}
                            </Typography>
                            <Typography variant="body2" noWrap sx={{ flex: 1 }}>
                              {item.productName}
                            </Typography>
                          </Box>
                        }
                        secondary={`${item.count}件 / ${formatCurrency(item.revenue)}`}
                      />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  データがありません
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Dialog open={settingsOpen} onClose={() => setSettingsOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>設定</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Gumroadアクセストークン"
            type="password"
            value={gumroadToken}
            onChange={(e) => setGumroadToken(e.target.value)}
            placeholder="Gumroadの設定画面から取得"
            sx={{ mt: 2, mb: 2 }}
            helperText="Gumroad → Settings → Advanced → Application で取得できます"
          />
          <TextField
            fullWidth
            label="月間目標金額"
            type="number"
            value={monthlyGoal}
            onChange={(e) => setMonthlyGoal(Number(e.target.value))}
            InputProps={{ startAdornment: '¥' }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSettingsOpen(false)}>キャンセル</Button>
          <Button variant="contained" onClick={handleSaveSettings} disabled={settingsMutation.isPending}>
            保存
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

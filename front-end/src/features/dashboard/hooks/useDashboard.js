import { useState, useEffect } from 'react';
import { getDashboardSummary } from '../services/dashboardService';
import { toDashboardViewModel } from '../mappers/dashboardMapper';


export function useDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = async () => {
    try {
      setLoading(true);
      const raw = await getDashboardSummary();
      setData(toDashboardViewModel(raw));
    } catch (err) {
      console.error(err)
      setError("Falha ao carregar radar operacional");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadData(); }, []);

  return { data, loading, error, refresh: loadData };
}

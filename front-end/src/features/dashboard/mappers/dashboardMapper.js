export const toDashboardViewModel = (apiData) => {
  const fuelDist = apiData.fuel_distribution || {};
  
  return {
    fuelDistribution: [
      { name: "Gasolina", value: fuelDist.GASOLINE || 0, color: "#f59e0b" },
      { name: "Diesel", value: fuelDist.DIESEL || 0, color: "#3b82f6" },
    ],
    
    statusHistory: {
      // Usamos chaves em MAIÚSCULAS para bater com o status_history do Django
      PENDING: apiData.status_history.PENDING || 0,
      APPROVED: apiData.status_history.APPROVED || 0,
      REJECTED: apiData.status_history.REJECTED || 0,
      CANCELLED: apiData.status_history.CANCELLED || 0,
      FUELED: apiData.status_history.FUELED || 0,
    },

    summary: {
      totalLiters: apiData.summary.total_liters,
      totalRequests: apiData.summary.total_requests,
      totalPending: apiData.summary.total_pending // Novo campo do Repository
    },

    fleetPerformance: apiData.fleet_performance.map(v => ({
      plate: v.license_plate,
      model: v.model,
      fuelType: v.fuel_type,
      
      // SINCRONIZADO: Mapeando os novos contadores do .annotate() do Django
      pending_requests: v.pending_count || 0,
      approved_requests: v.approved_count || 0,
      rejected_requests: v.rejected_count || 0,
      
      completedRequests: v.req_completed, 
      totalLiters: v.liters_total || 0    
    })),

    weeklyFlow: apiData.weekly_flow.map(f => ({
      day: f.day,
      liters: f.total_liters
    })),

    // Adicionado mapeamento para garantir que o ID chegue na tabela de atividades
    recentActivities: apiData.recent_activities.map(a => ({
      id: a.id,
      vehicle: a.vehicle,
      liters: a.liters,
      status: a.status,
      fuel_type: a.fuel_type
    }))
  };
};

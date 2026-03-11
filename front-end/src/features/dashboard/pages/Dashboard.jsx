import React from "react";
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
} from "recharts";
import { TrendingUp, Calendar, Car, Droplets } from "lucide-react";

import { useDashboard } from "../hooks/useDashboard";
import StatusBadge from "../../../shared/components/ui/StatusBadge";

// CORES DOS STATUS PARA O RADAR (Para não ficar cinzento como na imagem)
const STATUS_COLORS = {
  PENDING: "#f59e0b",
  APPROVED: "#3b82f6",
  REJECTED: "#ef4444",
  CANCELLED: "#64748b",
  FUELED: "#10b981",
};

export default function Dashboard() {
  const { data, loading, error } = useDashboard();

  if (loading)
    return (
      <div className="p-10 text-center font-black animate-pulse text-slate-400">
        Sincronizando ...
      </div>
    );
  if (error)
    return (
      <div className="p-10 text-red-500 font-bold text-center">{error}</div>
    );

  const statusPieData = Object.entries(data.statusHistory || {}).map(
    ([name, value]) => ({
      name,
      value,
      color: STATUS_COLORS[name.toUpperCase()] || "#black",
    }),
  );

  return (
    <div className="p-6 bg-slate-50 min-h-screen space-y-6">
      {/* HEADER / CARDS DE TOPO */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex items-center gap-4">
          <div className="p-3 bg-emerald-100 text-emerald-600 rounded-xl">
            <Droplets size={24} />
          </div>
          <div>
            <p className="text-xs font-bold text-slate-500 uppercase">
              Total Geral
            </p>
            <p className="text-2xl font-black text-slate-900">
              {data.summary?.totalLiters?.toLocaleString() || 0} L
            </p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex items-center gap-4">
          <div className="p-3 bg-blue-100 text-blue-600 rounded-xl">
            <Calendar size={24} />
          </div>
          <div>
            <p className="text-xs font-bold text-slate-500 uppercase">
              Pedidos Totais
            </p>
            <p className="text-2xl font-black text-slate-900">
              {data.summary?.totalRequests || 0}
            </p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex items-center gap-4">
          <div className="p-3 bg-amber-100 text-amber-600 rounded-xl">
            <TrendingUp size={24} />
          </div>
          <div>
            <p className="text-xs font-bold text-slate-500 uppercase">
              Pendentes
            </p>
            <p className="text-2xl font-black text-slate-900">
              {data.statusHistory?.PENDING || 0}
            </p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex items-center gap-4">
          <div className="p-3 bg-slate-100 text-slate-600 rounded-xl">
            <Car size={24} />
          </div>
          <div>
            <p className="text-xs font-bold text-slate-500 uppercase">
              Frota Activa
            </p>
            <p className="text-2xl font-black text-slate-900">
              {data.fleetPerformance?.length || 0}
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-3">
        {/* 1. BAR CHART - FLUXO SEMANAL */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm relative">
          <h2 className="text-sm font-black text-slate-800 uppercase tracking-widest mb-8">
            Fluxo Semanal (L)
          </h2>
          <ResponsiveContainer width="100%" height={250}>
            {/* Sincronizado com o mapper: weeklyFlow */}
            <BarChart data={data.weeklyFlow || []}>
              <CartesianGrid
                strokeDasharray="3 3"
                vertical={false}
                stroke="#f1f5f9"
              />
              {/* dataKey alterado para "day" conforme o seu mapper */}
              <XAxis
                dataKey="day"
                axisLine={false}
                tickLine={false}
                tick={{ fill: "#94a3b8", fontSize: 10, fontWeight: 700 }}
              />
              <YAxis
                axisLine={false}
                tickLine={false}
                tick={{ fill: "#94a3b8", fontSize: 10 }}
              />
              <Tooltip
                cursor={{ fill: "#f8fafc" }}
                contentStyle={{
                  borderRadius: "16px",
                  border: "none",
                  boxShadow: "0 10px 15px -3px rgba(0,0,0,0.1)",
                }}
              />
              <Bar
                dataKey="liters"
                fill="#3b82f6"
                radius={[6, 6, 0, 0]}
                barSize={24}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* 2. DISTRIBUIÇÃO COM TOTAL */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
          <h3 className="text-xs font-black text-slate-400 uppercase mb-4 text-center">
            Distribuição de Tipo
          </h3>
          <div className="h-64 relative">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data.fuelDistribution}
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                  nameKey="name"
                >
                  {data.fuelDistribution?.map((entry, index) => (
                    <Cell key={index} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend verticalAlign="bottom" />
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
              <span className="text-[10px] font-bold text-slate-400 uppercase">
                Total
              </span>
              <span className="text-xl font-black text-slate-900">
                {data.summary?.totalLiters?.toLocaleString()}L
              </span>
            </div>
          </div>
        </div>

        {/* 3. RADAR DE ESTADOS */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
          <h3 className="text-xs font-black text-slate-400 uppercase mb-6">
            Radar de Estados
          </h3>
          <div className="flex items-center h-64">
            <div className="w-1/2 h-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={statusPieData} dataKey="value" outerRadius={80}>
                    {statusPieData.map((entry, index) => (
                      <Cell key={index} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="w-1/2 space-y-1">
              {statusPieData.map((s, i) => (
                <div
                  key={i}
                  className="flex items-center justify-between px-2 py-1 bg-slate-50 rounded-lg"
                >
                  <StatusBadge status={s.name} />
                  <span className="font-black text-slate-700 text-xs">
                    {s.value}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* PERFORMANCE DA FROTA */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-slate-50">
          <h3 className="text-sm font-black text-slate-400 uppercase">
            Performance da Frota
          </h3>
        </div>
        <table className="w-full">
          <thead className="bg-slate-50 text-slate-500 text-[10px] uppercase font-bold">
            <tr>
              <th className="px-6 py-4 text-left">Veículo</th>
              <th className="px-6 py-4 text-center">Pendente</th>
              <th className="px-6 py-4 text-center text-blue-500">Aprovado</th>
              <th className="px-6 py-4 text-center text-emerald-500">
                Concluído
              </th>
              <th className="px-6 py-4 text-center text-red-500">Rejeitado</th>
              <th className="px-6 py-4 text-right">Total (L)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-50">
            {data.fleetPerformance?.map((v, i) => (
              <tr key={i} className="hover:bg-slate-50/50 transition-colors">
                <td className="px-6 py-4">
                  <div className="font-bold text-slate-900">{v.plate}</div>
                  <div className="text-[10px] text-slate-400 font-bold">
                    {v.model}
                  </div>
                </td>
                <td className="px-6 py-4 text-center text-sm font-bold text-slate-600">
                  {v.pending_requests || 0}
                </td>
                <td className="px-6 py-4 text-center text-sm font-bold text-blue-500">
                  {v.approved_requests || 0}
                </td>
                <td className="px-6 py-4 text-center text-sm font-bold text-emerald-600">
                  {v.completedRequests || 0}
                </td>
                <td className="px-6 py-4 text-center text-sm font-bold text-red-400">
                  {v.rejected_requests || 0}
                </td>
                <td className="px-6 py-4 text-right font-black text-slate-900">
                  {v.totalLiters?.toLocaleString()}{" "}
                  <span className="text-[10px] text-slate-400">L</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* ACTIVIDADES RECENTES - ADICIONADO COLUNA ID */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
        <h3 className="text-sm font-black text-slate-400 uppercase mb-4 tracking-widest">
          Actividades Recentes
        </h3>
        <div className="space-y-4">
          {data.recentActivities?.map((activity, i) => (
            <div
              key={i}
              className="flex items-center justify-between p-4 bg-slate-50 rounded-xl hover:bg-slate-100 transition-all border border-transparent hover:border-slate-200"
            >
              <div className="flex items-center gap-4">
                {/* COLUNA ID ADICIONADA AQUI */}
                <div className="text-[10px] font-black text-blue-400">
                  #{activity.id}
                </div>
                <div className="p-2 bg-white rounded-lg shadow-sm font-bold text-xs text-slate-600">
                  {activity.vehicle}
                </div>
                <div>
                  <p className="text-sm font-black text-slate-900">
                    {activity.liters} Litros
                  </p>
                  <p className="text-[10px] font-bold text-slate-400 uppercase">
                    {activity.fuel_type}
                  </p>
                </div>
              </div>
              <StatusBadge status={activity.status} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../core/auth/useAuth';
import { LayoutDashboard, Car, Fuel, Settings, ShieldCheck, Plus } from 'lucide-react';

const Sidebar = () => {
  const { isManager, isAdmin } = useAuth();
  const location = useLocation();

  const menuItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard, show: true },
    { name: 'Requisições (v1)', path: '/requestsv1', icon: Plus, show: true },
    { name: 'Novo Lote (v2)', path: '/requests/bulk', icon: Plus, show: true },
    { name: 'Requisições (v2)', path: '/requestsv2', icon: Fuel, show: true },
    { name: 'Viaturas', path: '/vehicles', icon: Car, show: true },
    { name: 'Configurações', path: '/settings', icon: Settings, show: isAdmin },
  ];

  return (
    <aside className="w-64 bg-slate-900 text-white flex flex-col">
      <div className="p-6 text-xl font-bold border-b border-slate-800">
        🚀 Fuel Management
      </div>
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => item.show && (
          <Link
            key={item.path}
            to={item.path}
            className={`flex items-center space-y-2 p-3 rounded-lg transition-colors ${
              location.pathname === item.path ? 'bg-blue-600' : 'hover:bg-slate-800'
            }`}
          >
            <item.icon className="w-5 h-5 mr-3" />
            <span>{item.name}</span>
          </Link>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;

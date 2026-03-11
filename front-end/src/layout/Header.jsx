import { useAuth } from '../core/auth/useAuth';
import { LogOut, User } from 'lucide-react';

const Header = () => {
  const { user, logout } = useAuth();

  return (
    <header className="h-16 bg-white shadow-sm flex items-center justify-between px-8">
      <div className="text-sm text-gray-500">
        Status: <span className="text-green-500 font-medium">Online</span>
      </div>

      <div className="flex items-center space-x-4">
        <div className="flex flex-col text-right">
          <span className="font-bold text-slate-800">{user?.display_name}</span>
          <span className="text-xs text-blue-600 font-semibold">{user?.role}</span>
        </div>
        <div className="w-10 h-10 bg-slate-200 rounded-full flex items-center justify-center">
          <User className="text-slate-600" />
        </div>
        <button 
          onClick={logout}
          className="p-2 hover:bg-red-50 rounded-lg text-red-500 transition-colors"
          title="Sair do Sistema"
        >
          <LogOut className="w-5 h-5" />
        </button>
      </div>
    </header>
  );
};

export default Header;

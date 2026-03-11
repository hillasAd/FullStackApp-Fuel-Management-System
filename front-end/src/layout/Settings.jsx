import React, { useState } from 'react';
import { 
  Users, Fuel, Settings, UserPlus, ShieldCheck, 
  Lock, Edit3, Save, Search, AlertTriangle,
  Mail, MessageSquare, Bell, Calendar, X, Hash, Clock
} from 'lucide-react';

const AdminSettingsPage = () => {
  const [activeTab, setActiveTab] = useState('users');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);

  // --- ESTADO DE UTILIZADORES ---
  const [users, setUsers] = useState([
    { id: 1, name: "Admilson Itech", email: "admilson@empresa.co.mz", role: "ADMIN", status: "active" },
    { id: 2, name: "Hilario Amamo", email: "hilario@empresa.co.mz", role: "OPERATOR", status: "active" },
    { id: 3, name: "Maria Santos", email: "maria@empresa.co.mz", role: "MANAGER", status: "blocked" },
    { id: 4, name: "João Paulo", email: "joao@empresa.co.mz", role: "OPERATOR", status: "active" },
    { id: 5, name: "Carla Matos", email: "carla@empresa.co.mz", role: "MANAGER", status: "active" },
    { id: 6, name: "Pedro Nuro", email: "pedro@empresa.co.mz", role: "OPERATOR", status: "blocked" },
    { id: 7, name: "Elena Sitoe", email: "elena@empresa.co.mz", role: "ADMIN", status: "active" },
    { id: 8, name: "Ricardo Bila", email: "ricardo@empresa.co.mz", role: "OPERATOR", status: "active" },
    { id: 9, name: "Sofia Langa", email: "sofia@empresa.co.mz", role: "MANAGER", status: "active" },
  ]);

  const [fuelPrices, setFuelPrices] = useState({ gasolina: "86.25", diesel: "91.50" });

  const toggleUserStatus = (id) => {
    setUsers(prev => prev.map(u => u.id === id ? { ...u, status: u.status === 'active' ? 'blocked' : 'active' } : u));
  };

  const openUserModal = (user = null) => {
    setSelectedUser(user);
    setIsModalOpen(true);
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6 animate-in fade-in duration-500 pb-20">
      <header>
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">Painel Administrativo</h1>
        <p className="text-slate-500 font-medium italic">Gestão centralizada de utilizadores e regras de negócio.</p>
      </header>

      {/* NAVEGAÇÃO */}
      <div className="flex p-1 bg-slate-100 rounded-2xl w-fit border border-slate-200 overflow-x-auto">
        <TabButton active={activeTab === 'users'} onClick={() => setActiveTab('users')} icon={<Users size={18} />} label="Utilizadores" />
        <TabButton active={activeTab === 'fuel'} onClick={() => setActiveTab('fuel')} icon={<Fuel size={18} />} label="Preços" />
        <TabButton active={activeTab === 'notifications'} onClick={() => setActiveTab('notifications')} icon={<Bell size={18} />} label="Notificações" />
        <TabButton active={activeTab === 'system'} onClick={() => setActiveTab('system')} icon={<Settings size={18} />} label="Sistema" />
      </div>

      <main className="bg-white rounded-[2.5rem] shadow-sm border border-slate-200 p-10 min-h- [550px]">
        {activeTab === 'users' && (
          <UsersManagement users={users} onToggleStatus={toggleUserStatus} onEdit={openUserModal} onAdd={() => openUserModal(null)} />
        )}
        
        {activeTab === 'fuel' && (
          <FuelPriceManagement prices={fuelPrices} setPrices={setFuelPrices} />
        )}

        {activeTab === 'notifications' && (
          <NotificationSettings />
        )}

        {activeTab === 'system' && (
          <SystemParameters />
        )}
      </main>

      {/* MODAL CRUD UTILIZADOR */}
      {isModalOpen && (
        <UserFormModal 
          user={selectedUser} 
          onClose={() => setIsModalOpen(false)} 
          onSave={() => setIsModalOpen(false)}
        />
      )}
    </div>
  );
};

// --- SUB-COMPONENTES DETALHADOS ---

const UsersManagement = ({ users, onToggleStatus, onEdit, onAdd }) => (
  <div className="space-y-8">
    <div className="flex flex-col md:flex-row justify-between items-center gap-4">
      <div className="relative w-full md:w-80">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
        <input type="text" placeholder="Procurar por nome ou e-mail..." className="w-full pl-12 pr-4 py-3 bg-slate-50 border-none rounded-2xl text-sm focus:ring-2 focus:ring-blue-500" />
      </div>
      <button onClick={onAdd} className="w-full md:w-auto bg-blue-600 hover:bg-blue-700 text-white px-8 py-3.5 rounded-2xl text-sm font-black flex items-center justify-center transition-all shadow-lg shadow-blue-100 active:scale-95">
        <UserPlus size={18} className="mr-2" /> NOVO UTILIZADOR
      </button>
    </div>

    <div className="overflow-x-auto">
      <table className="w-full text-left border-separate border-spacing-y-3">
        <thead>
          <tr className="text-slate-400 text-[10px] font-black uppercase tracking-widest px-6">
            <th className="px-6">Identificação</th>
            <th className="px-6 text-center">Nível Acesso</th>
            <th className="px-6 text-center">Estado</th>
            <th className="px-6 text-right">Acções</th>
          </tr>
        </thead>
        <tbody>
          {users.map(u => (
            <UserRow key={u.id} {...u} onToggle={() => onToggleStatus(u.id)} onEdit={() => onEdit(u)} />
          ))}
        </tbody>
      </table>
    </div>
  </div>
);

const FuelPriceManagement = ({ prices, setPrices }) => (
  <div className="max-w-3xl space-y-10 animate-in slide-in-from-bottom-4">
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div className="p-8 rounded-[2.5rem] bg-amber-50 border border-amber-100 space-y-4 shadow-sm">
        <div className="flex justify-between items-center text-amber-700">
          <span className="text-xs font-black uppercase tracking-widest">Gasolina 95</span>
          <Fuel size={24} />
        </div>
        <div className="flex items-baseline space-x-2">
            <input 
              type="number" 
              value={prices.gasolina} 
              onChange={(e) => setPrices({...prices, gasolina: e.target.value})}
              className="text-5xl font-black bg-transparent border-none w-36 focus:ring-0 p-0 text-amber-900"
            />
            <span className="text-xl font-black text-amber-900/30">MT</span>
        </div>
        <p className="text-[10px] text-amber-600 font-bold flex items-center"><Calendar size={12} className="mr-1"/> Actualizado hoje às 08:30</p>
      </div>

      <div className="p-8 rounded-[2.5rem] bg-slate-900 border border-slate-800 space-y-4 shadow-2xl">
        <div className="flex justify-between items-center text-slate-400">
          <span className="text-xs font-black uppercase tracking-widest">Diesel (Gasóleo)</span>
          <Fuel size={24} />
        </div>
        <div className="flex items-baseline space-x-2 text-white">
            <input 
              type="number" 
              value={prices.diesel} 
              onChange={(e) => setPrices({...prices, diesel: e.target.value})}
              className="text-5xl font-black bg-transparent border-none w-36 focus:ring-0 p-0 text-white"
            />
            <span className="text-xl font-black text-slate-700">MT</span>
        </div>
        <button className="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-[10px] font-black uppercase tracking-widest transition-all">Fixar Novo Preço</button>
      </div>
    </div>

    <div className="bg-blue-50/50 p-6 rounded-3xl border border-blue-100 flex items-start">
      <AlertTriangle className="text-blue-600 mr-4 shrink-0" size={24} />
      <p className="text-blue-800 text-sm font-medium leading-relaxed">
        <strong>Atenção Operacional:</strong> A alteração dos preços afecta apenas lotes criados 
        posteriormente. Lotes em estado <strong>PROCESSED</strong> ou <strong>PENDING</strong> mantêm o custo histórico.
      </p>
    </div>
  </div>
);

const NotificationSettings = () => (
  <div className="max-w-2xl space-y-10">
    <section className="space-y-6">
      <div className="flex items-center space-x-3 text-slate-800">
        <div className="p-2 bg-blue-100 rounded-lg text-blue-600"><Mail size={20}/></div>
        <h3 className="text-lg font-black tracking-tight">Servidor de E-mail (SMTP)</h3>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <InputSetting title="Host SMTP" defaultValue="://mandrill.com" />
        <InputSetting title="Porta" defaultValue="587" />
        <InputSetting title="Utilizador" defaultValue="frotas@empresa.co.mz" />
        <InputSetting title="Senha" defaultValue="********" type="password" />
      </div>
    </section>

    <section className="space-y-6 pt-10 border-t border-slate-100">
      <div className="flex items-center space-x-3 text-slate-800">
        <div className="p-2 bg-emerald-100 rounded-lg text-emerald-600"><MessageSquare size={20}/></div>
        <h3 className="text-lg font-black tracking-tight">Canais de SMS</h3>
      </div>
      <div className="space-y-4">
        <InputSetting title="API Key SMS" defaultValue="sk_live_v8271hjsh" />
        <ToggleSetting title="Notificações Críticas" description="Enviar SMS ao Gestor quando um lote for rejeitado." active={true} />
        <ToggleSetting title="Alertas de Motorista" description="Notificar motorista via SMS após aprovação do abastecimento." active={false} />
      </div>
    </section>

    <button className="bg-slate-900 text-white px-10 py-4 rounded-2xl font-black text-sm hover:bg-blue-600 transition-all flex items-center">
      <Save size={18} className="mr-2" /> GRAVAR CONFIGURAÇÕES
    </button>
  </div>
);

const SystemParameters = () => (
  <div className="max-w-2xl space-y-10">
    <div className="space-y-8">
      <div className="flex items-center space-x-3 text-slate-800">
        <div className="p-2 bg-purple-100 rounded-lg text-purple-600"><Hash size={20}/></div>
        <h3 className="text-lg font-black tracking-tight">Controle Operacional</h3>
      </div>
      
      <div className="grid grid-cols-1 gap-6">
        <ToggleSetting 
          title="Idempotência de Pedidos" 
          description="Garante que cliques duplos não criem abastecimentos repetidos." 
          active={true} 
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4">
          <InputSetting 
            title="Limite Diário (L)" 
            description="Teto máximo de combustível por viatura/dia." 
            defaultValue="150" 
          />
          <InputSetting 
            title="Timeout de Lote (h)" 
            description="Horas para um lote pendente expirar." 
            defaultValue="12" 
          />
        </div>
      </div>
    </div>

    <div className="p-6 bg-amber-50 rounded-3xl border border-amber-100 space-y-3">
        <h4 className="font-black text-amber-900 text-xs uppercase tracking-widest flex items-center">
          <AlertTriangle size={14} className="mr-2" /> Zona de Risco
        </h4>
        <p className="text-amber-800 text-xs">Alterar parâmetros do sistema pode afectar a sincronização entre o backend e dispositivos móveis.</p>
    </div>

    <button className="w-full md:w-auto bg-slate-900 text-white px-10 py-4 rounded-2xl font-black text-sm hover:bg-rose-600 transition-all">
       ACTUALIZAR PARÂMETROS
    </button>
  </div>
);

// --- ATOM COMPONENTS ---

const UserFormModal = ({ user, onClose, onSave }) => (
  <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-md z-50 flex items-center justify-center p-4">
    <div className="bg-white w-full max-w-md rounded-[2.5rem] shadow-2xl overflow-hidden border border-white/20 animate-in zoom-in-95 duration-200">
      <div className="p-8 border-b border-slate-50 flex justify-between items-center bg-slate-50/50">
        <h2 className="text-2xl font-black text-slate-900">{user ? 'Editar User' : 'Novo Acesso'}</h2>
        <button onClick={onClose} className="p-2 hover:bg-slate-200 rounded-full transition-colors"><X size={24}/></button>
      </div>
      <div className="p-10 space-y-6">
        <InputSetting title="Nome Completo" defaultValue={user?.name || ""} />
        <InputSetting title="E-mail" defaultValue={user?.email || ""} />
        <div className="space-y-2">
          <label className="font-bold text-slate-800 text-xs uppercase tracking-widest">Cargo Operacional</label>
          <select defaultValue={user?.role || "OPERATOR"} className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl text-sm font-bold focus:ring-2 focus:ring-blue-500 transition-all outline-none appearance-none">
            <option value="ADMIN">ADMINISTRADOR MASTER</option>
            <option value="MANAGER">GESTOR DE FROTA</option>
            <option value="OPERATOR">OPERADOR DE BOMBA</option>
          </select>
        </div>
        <button onClick={onSave} className="w-full py-5 bg-blue-600 hover:bg-blue-700 text-white rounded-2xl font-black text-sm shadow-xl shadow-blue-100 transition-all flex items-center justify-center">
          <Save size={20} className="mr-2" /> {user ? 'Actualizar Dados' : 'Criar Utilizador'}
        </button>
      </div>
    </div>
  </div>
);

const UserRow = ({ name, email, role, status, onToggle, onEdit }) => (
  <tr className="bg-slate-50/50 hover:bg-white hover:shadow-md transition-all group">
    <td className="px-6 py-5 rounded-l-3xl">
      <div className="font-black text-slate-900 text-base">{name}</div>
      <div className="text-xs text-slate-400 font-medium">{email}</div>
    </td>
    <td className="px-6 text-center">
      <span className={`text-[10px] font-black border px-3 py-1.5 rounded-xl ${
        role === 'ADMIN' ? 'bg-purple-100 border-purple-200 text-purple-700' : 'bg-white border-slate-200 text-slate-600'
      }`}>
        {role}
      </span>
    </td>
    <td className="px-6 text-center">
      <span className={`text-[10px] font-black px-4 py-1.5 rounded-full ${status === 'active' ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'}`}>
        {status === 'active' ? '● ACTIVO' : '○ BLOQUEADO'}
      </span>
    </td>
    <td className="px-6 text-right rounded-r-3xl space-x-2">
      <button onClick={onEdit} className="p-3 bg-white border border-slate-100 rounded-xl text-slate-400 hover:text-blue-600 hover:shadow-sm transition-all"><Edit3 size={18} /></button>
      <button onClick={onToggle} className={`p-3 border rounded-xl transition-all ${status === 'active' ? 'bg-rose-50 border-rose-100 text-rose-600' : 'bg-emerald-50 border-emerald-100 text-emerald-700'}`}>
        {status === 'active' ? <Lock size={18} /> : <ShieldCheck size={18} />}
      </button>
    </td>
  </tr>
);

const TabButton = ({ active, onClick, icon, label }) => (
  <button onClick={onClick} className={`flex items-center space-x-3 px-8 py-3 rounded-2xl text-sm font-black transition-all ${active ? 'bg-white text-blue-600 shadow-md scale-105' : 'text-slate-500 hover:text-slate-800'}`}>
    {icon} <span>{label}</span>
  </button>
);

const ToggleSetting = ({ title, description, active }) => (
  <div className="flex items-center justify-between p-5 bg-slate-50 rounded-3xl border border-slate-100 hover:border-blue-100 transition-colors">
    <div className="max-w-[80%]">
      <div className="font-black text-slate-900 text-sm tracking-tight">{title}</div>
      <div className="text-xs text-slate-400 font-medium leading-relaxed">{description}</div>
    </div>
    <div className={`w-14 h-7 rounded-full p-1 transition-all cursor-pointer ${active ? 'bg-blue-600' : 'bg-slate-300'}`}>
      <div className={`bg-white w-5 h-5 rounded-full transition-all shadow-sm ${active ? 'translate-x-7' : 'translate-x-0'}`} />
    </div>
  </div>
);

const InputSetting = ({ title, defaultValue, description, type = "text" }) => (
  <div className="space-y-1">
    <label className="font-black text-slate-800 text-[10px] uppercase tracking-widest">{title}</label>
    {description && <p className="text-[10px] text-slate-400 mb-2">{description}</p>}
    <input 
      type={type} 
      defaultValue={defaultValue} 
      className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl text-sm font-bold focus:ring-2 focus:ring-blue-500 outline-none transition-all" 
    />
  </div>
);

export default AdminSettingsPage;

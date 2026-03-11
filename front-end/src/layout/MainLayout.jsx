import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';
import Footer from './Footer';

/**
 * Layout Principal
 */
const MainLayout = () => {
  return (
    <div className="flex h-screen bg-gray-300 overflow-hidden">
      {/* Menu Lateral Fixo */}
      <Sidebar />

      <div className="flex flex-col flex-1 w-full overflow-y-auto">
        {/* Barra Superior (User Profile, Logout) */}
        <Header />

        {/* Conteúdo Dinâmico (Injetado pelo Router) */}
        <main className="p-6">
          <Outlet />
        </main>
        <Footer />
      </div>
    </div>
  );
};

export default MainLayout;

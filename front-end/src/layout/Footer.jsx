import React from 'react';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="w-full bg-white backdrop-blur-sm border-t border-slate-100 py-4 mt-auto">
      <div className="max-w-7xl mx-auto px-10 flex flex-col md:flex-row justify-between items-center gap-3">
        
        {/* Lado Esquerdo: Info Sistema */}
        <div className="flex items-center space-x-2 text-[10px] font-black text-slate-400 uppercase tracking-widest">
          <span>&copy; {currentYear}</span>
          <span className="text-slate-200">|</span>
          <span>Fleet Management System v2.0</span>
        </div>
        
        {/* Lado Direito: Créditos */}
        <div className="flex items-center text-xs">
          <span className="text-slate-400 font-medium mr-1.5 italic">Desenvolvido por</span>
          <a 
            href="https://linkedin.com/in/hilárioamamo" 
            target="_blank" 
            rel="noopener noreferrer" 
            className="group flex items-center font-black text-slate-600 hover:text-blue-600 transition-all duration-300"
          >
            Hilario Amamo
            <span className="ml-1 opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all duration-300">
               ↗
            </span>
          </a>
        </div>
        
      </div>
    </footer>
  );
};

export default Footer;

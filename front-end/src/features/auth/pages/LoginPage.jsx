import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useAuth } from '../../../core/auth/useAuth';
import { authApi } from '../services/authApi';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { Lock, User, Loader2 } from 'lucide-react';
import Swal from 'sweetalert2';

// 1. Esquema de Validação
const loginSchema = z.object({
  username: z.string().min(3, 'Utilizador deve ter pelo menos 3 caracteres'),
  password: z.string().min(4, 'Palavra-passe é obrigatória'),
});

const LoginPage = () => {
  const { setAuth } = useAuth();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data) => {
    setIsLoading(true);
    try {
      const result = await authApi.login(data);
      
      // 2. Guardar no Zustand
      setAuth(result.user, result.access, result.refresh);
      
      Swal.fire({
        icon: 'success',
        title: 'Seja muito Bem-vindo ao FMS!',
        timer: 1500,
        showConfirmButton: false,
      });

      navigate('/'); 
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Falha na Autenticação',
        text: error.message || 'Verifica as tuas credenciais.',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 px-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-2xl p-8">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-slate-800">🚀 Fuel Management System</h2>
          <p className="text-blue-500 mt-2">Introduz as tuas credenciais de acesso</p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Campo Utilizador */}
          <div>
            <label className="block text-sm font-medium text-slate-700">Utilizador</label>
            <div className="mt-1 relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <User className="h-5 w-5 text-slate-400" />
              </div>
              <input
                {...register('username')}
                className={`block w-full pl-10 pr-3 py-2 border ${errors.username ? 'border-red-500' : 'border-slate-300'} rounded-lg focus:ring-blue-500 focus:border-blue-500`}
                placeholder="ex: admin_gestor"
              />
            </div>
            {errors.username && <p className="text-red-500 text-xs mt-1">{errors.username.message}</p>}
          </div>

          {/* Campo Password */}
          <div>
            <label className="block text-sm font-medium text-slate-700">Palavra-passe</label>
            <div className="mt-1 relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Lock className="h-5 w-5 text-slate-400" />
              </div>
              <input
                type="password"
                {...register('password')}
                className={`block w-full pl-10 pr-3 py-2 border ${errors.password ? 'border-red-500' : 'border-slate-300'} rounded-lg focus:ring-blue-500 focus:border-blue-500`}
                placeholder="••••••••"
              />
            </div>
            {errors.password && <p className="text-red-500 text-xs mt-1">{errors.password.message}</p>}
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-bold text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 transition-all"
          >
            {isLoading ? <Loader2 className="animate-spin h-5 w-5" /> : 'ENTRAR NO SISTEMA'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;

import { useAuthStore } from './authStore';

/**
 * Hook customizado para facilitar o acesso à lógica de Auth.
 * Centraliza as perguntas: "Quem sou eu?" e "O que posso fazer?".
 */
export const useAuth = () => {
  const { user, token, isAuthenticated, logout, setAuth } = useAuthStore();

  const isManager = user?.role === 'MANAGER';
  const isOperator = user?.role === 'OPERATOR';
  const isAdmin = user?.role === 'ADMIN';

  return {
    user,
    token,
    isAuthenticated,
    isManager,
    isOperator,
    isAdmin,
    logout,
    setAuth,
  };
};

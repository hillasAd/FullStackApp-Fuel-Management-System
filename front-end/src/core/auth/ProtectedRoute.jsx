import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from './useAuth';

/**
 * Componente de Alta Precisão: Protege rotas por Autenticação e Role.
 */
export const ProtectedRoute = ({ children, allowedRoles }) => {
  const { isAuthenticated, user } = useAuth();
  const location = useLocation();

  // 1. Se não está logado, manda para o Login, mas guarda onde ele tentou ir
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // 2. Se a rota exige papéis específicos e o user não os tem
  if (allowedRoles && !allowedRoles.includes(user?.role)) {
    return <Navigate to="/unauthorized" replace />;
  }

  // 3. Se passou em tudo, entra à vontade
  return children;
};

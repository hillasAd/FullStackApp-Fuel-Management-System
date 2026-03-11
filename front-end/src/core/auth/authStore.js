import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

/**
 * Store de Autenticação: Gere o estado global do utilizador.
 * Usamos o middleware 'persist' para que, se o user der F5, não perca o login.
 */
export const useAuthStore = create(
  persist(
    (set) => ({
      user: null,          // { id, username, email, role }
      token: null,         // JWT Access Token
      refreshToken: null,  // JWT Refresh Token
      isAuthenticated: false,

      // Ação: Define o estado após o login de sucesso
      setAuth: (user, token, refreshToken) => set({
        user,
        token,
        refreshToken,
        isAuthenticated: true,
      }),

      // Ação: Limpa tudo (Logout)
      logout: () => {
        localStorage.removeItem('auth-storage'); // Limpeza extra
        set({ user: null, token: null, refreshToken: null, isAuthenticated: false });
      },

      // Ação: Atualiza apenas o token (útil para o Refresh automático)
      updateToken: (newToken) => set({ token: newToken }),
    }),
    {
      name: 'auth-storage', // Chave no LocalStorage
      storage: createJSONStorage(() => localStorage),
    }
  )
);

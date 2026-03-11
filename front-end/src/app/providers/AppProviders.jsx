import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { I18nextProvider } from 'react-i18next';
import i18n from '../../i18n';

// Configuração de Elite do QueryClient
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,               // Se falhar, tenta apenas mais uma vez
      refetchOnWindowFocus: false, // Não faz refetch só porque mudaste de aba
      staleTime: 5 * 60 * 1000,    // Os dados são considerados "frescos" por 5 minutos
    },
  },
});

export const AppProviders = ({ children }) => {
  return (
    <I18nextProvider i18n={i18n}>
      <QueryClientProvider client={queryClient}>
        {children}
        {/* Ferramenta de Debug do Projecto - Apenas em desenvolvimento */}
        {/* <ReactQueryDevtools initialIsOpen={false} /> */}
      </QueryClientProvider>
    </I18nextProvider>
    
  );
};

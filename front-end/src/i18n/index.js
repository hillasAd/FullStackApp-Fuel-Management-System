import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

i18n.use(initReactI18next).init({
  resources: {
    pt: { translation: { "welcome": "Bem-vindo ao Sistema de Gestão de Combustível" } },
    en: { translation: { "welcome": "Welcome to Fuel Management System" } },
  },
  lng: 'pt', // Língua padrão
  fallbackLng: 'en',
  interpolation: { escapeValue: false },
});

export default i18n;

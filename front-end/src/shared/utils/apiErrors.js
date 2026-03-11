import Swal from 'sweetalert2';

export const notifyApiError = (error) => {
  const data = error.response?.data;
  const status = error.response?.status;

  const message = data?.message || "Erro de comunicação com o servidor.";
  const errorCode = data?.error_code || "UNKNOWN_ERROR";

  if (status === 401) {
     window.location.href = '/login';
     return;
  }

  const errorMap = {
    "invalid_fuel_state": { title: "Transição Proibida", icon: "warning" },
    "tank_capacity_exceeded": { title: "Capacidade Excedida", icon: "error" },
    "conflict": { title: "Conflito de Versão", icon: "info" },
    "vehicle_already_exists": { title: "Viatura Duplicada", icon: "info" },
    "not_found": { title: "Não Encontrado", icon: "question" },
  };

  const config = errorMap[errorCode] || { title: "Erro Operacional", icon: "error" };

  Swal.fire({
    title: config.title,
    text: message,
    icon: config.icon,
    confirmButtonColor: "#3085d6"
  });
};

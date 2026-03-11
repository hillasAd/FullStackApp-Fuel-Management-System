import { createBrowserRouter, Navigate } from "react-router-dom";
import { ProtectedRoute } from "../../core/auth/ProtectedRoute";
import MainLayout from "../../layout/MainLayout";
import LoginPage from "../../features/auth/pages/LoginPage";
import VehicleListPage from "../../features/vehicles/pages/VehicleListPage";
import BulkRequestPage from "../../features/fuelRequests/pages/BulkRequestPage";
import RequestV1ListPage from "../../features/fuelRequestV1/pages/RequestV1ListPage";
import BulkRequestListPage from "../../features/fuelRequests/pages/BulkRequestListPage";
import BulkRequestDetailPage from "../../features/fuelRequests/pages/BulkRequestDetailPage";
import Settings from "../../layout/Settings";
import Dashboard from "../../features/dashboard/pages/Dashboard";


const DummyUnauthorized = () => (
  <div className="p-10 text-center">
    <h1 className="text-4xl font-bold text-red-500">403</h1>
    <p className="text-xl">Acesso Negado.</p>
  </div>
);

export const router = createBrowserRouter([
  // 1. Rotas Públicas (Abertas)
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/unauthorized",
    element: <DummyUnauthorized />,
  },

  // 2. Rotas Protegidas (Exigem Login + MainLayout)
  {
    path: "/",
    element: (
      <ProtectedRoute>
        <MainLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        index: true, // Caminho padrão: "/"
        element: <Dashboard />,
      },
      {
        path: "vehicles", // Caminho: "/vehicles"
        element: <VehicleListPage />,
      },
      {
        path: "/requests/bulk/:id",
        element: <BulkRequestDetailPage />,
      },
      // V1
      {
        path: "requestsv1/",
        element: <RequestV1ListPage />,
      },
      // 2. Adicione ao array de children (dentro do MainLayout)
      {
        path: "requests/bulk", // A nova rota v2
        element: <BulkRequestPage />,
      },
      {
        path: "requestsv2/", // Caminho: "/requests"
        element: <BulkRequestListPage />,
      },
      {
        path: "settings/",
        element: <Settings />,
      },
      {
        path: "fuel-management", // Caminho: "/fuel-management"
        element: (
          <ProtectedRoute allowedRoles={["MANAGER", "ADMIN"]}>
            <Settings />
          </ProtectedRoute>
        ),
      },
    ],
  },

  // 3. Rota de Fuga (404 - Página não encontrada)
  {
    path: "*",
    element: <Navigate to="/" replace />,
  },
]);

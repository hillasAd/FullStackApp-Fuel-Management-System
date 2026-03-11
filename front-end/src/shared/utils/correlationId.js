/**
 * Gera um UUID v4 simples para rastreamento de requisições (Correlation ID).
 * Garante que o Frontend e o Backend falem a mesma língua nos logs.
 */
export const generateCorrelationId = () => {
  return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, (c) =>
    (c ^ (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))).toString(16)
  );
};

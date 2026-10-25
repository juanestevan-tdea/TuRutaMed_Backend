import { isAxiosError } from 'axios';

interface ErrorPayload {
  detail?: unknown;
  mensaje?: unknown;
  message?: unknown;
  detalles?: unknown;
}

function extraerTexto(valor: unknown): string | null {
  if (typeof valor === 'string' && valor.trim()) {
    return valor.trim();
  }

  if (Array.isArray(valor)) {
    const partes = valor
      .map((item) => {
        if (typeof item === 'string') return item;
        if (item && typeof item === 'object') {
          const detalle = item as { msg?: unknown; message?: unknown };
          const mensaje = detalle.msg ?? detalle.message;
          return typeof mensaje === 'string' ? mensaje : null;
        }
        return null;
      })
      .filter((parte): parte is string => Boolean(parte));

    return partes.length > 0 ? partes.join(' ') : null;
  }

  return null;
}

export function getApiErrorMessage(error: unknown, fallback: string): string {
  if (!isAxiosError(error)) {
    return error instanceof Error && error.message ? error.message : fallback;
  }

  const data = error.response?.data as ErrorPayload | undefined;
  const mensaje =
    extraerTexto(data?.detail) ??
    extraerTexto(data?.mensaje) ??
    extraerTexto(data?.detalles) ??
    extraerTexto(data?.message);

  if (mensaje) return mensaje;

  if (error.code === 'ERR_NETWORK') {
    return 'No se pudo conectar con el servidor. Verifica que el backend esté en línea.';
  }

  return error.message || fallback;
}

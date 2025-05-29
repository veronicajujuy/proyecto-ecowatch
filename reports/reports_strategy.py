from domain.models import Reporte


class PromedioPorMetricaReport(Reporte):
    def generar(self, datos, key):
        """Genera un reporte de estado metrica
        args:
            key: en este campo se espera un string como temperatura, humedad, etc

        returns:
            dataframe: el reporte
        """

        reporte = datos.groupby("sala")[key].mean().round(2).reset_index()

        # reporte.columns = [key, "promedio"]

        return reporte


class AlertasCriticasReports(Reporte):
    def generar(self, datos, key):
        """Genera un reporte de alertas criticas
        args:
            key: en este campo se espera un string como warning, error, etc

        returns:
            dataframe: el reporte
        """
        filtrado = datos[datos["estado"] == key]

        reporte = filtrado.groupby("sala").size().reset_index(name=f"Cantidad_{key}")

        return reporte

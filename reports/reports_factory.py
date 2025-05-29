from abc import ABC, abstractmethod

from reports.reports_strategy import PromedioPorMetricaReport, AlertasCriticasReports


class ReportsBase(ABC):
    @abstractmethod
    def generar_reporte(self, *args):
        pass


class PromedioPorMetricasVarias(ReportsBase):
    def generar_reporte(self, df, *args):
        reportes = []
        for key in args:
            reporte = PromedioPorMetricaReport().generar(df, key)
            reportes.append(reporte)

        # Combinar todos los dataframes usando merge progresivo
        reporte_final = reportes[0]
        for rep in reportes[1:]:
            reporte_final = reporte_final.merge(rep, on="sala", how="outer")

        reporte_final.fillna(0, inplace=True)
        return reporte_final


class AlertasCriticasVarias(ReportsBase):
    def generar_reporte(self, df, *args):
        reportes = []
        for key in args:
            reporte = AlertasCriticasReports().generar(df, key)
            reportes.append(reporte)

        # Combinar todos los dataframes usando merge progresivo
        reporte_final = reportes[0]
        for rep in reportes[1:]:
            reporte_final = reporte_final.merge(rep, on="sala", how="outer")

        reporte_final.fillna(0, inplace=True)
        return reporte_final


class ReporteFactory:
    """
    Clase que encapsula la creacion de reportes y aplica el patrón Factory para la eleccion de reportes
    """

    @staticmethod
    def elegir_reporte(tipo, *args):
        if tipo == "promedio":
            return PromedioPorMetricasVarias()
        elif tipo == "alertas":
            return AlertasCriticasVarias()
        else:
            raise ValueError("Tipo de reporte no reconocido")

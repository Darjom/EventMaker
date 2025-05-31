import json
from app import app
from datetime import datetime

from modules.inscriptions.application.ChartDataConverter import ChartDataConverter
from modules.inscriptions.application.StatisticsService import StatisticsService
from modules.inscriptions.infrastructure.PostgresInscriptionRepository import PostgresInscriptionRepository

def print_real_statistics_data(event_id: int = 1):
    """Obtiene y muestra datos reales de estadísticas para un evento específico"""
    # Crear instancias necesarias
    stats_repo = PostgresInscriptionRepository()
    service = StatisticsService(stats_repo)

    print("\n" + "=" * 70)
    print(f"DATOS ESTADÍSTICOS PARA EL EVENTO ID={event_id}")
    print("=" * 70)

    # Obtener todas las estadísticas para el evento
    print("\nOBTENIENDO ESTADÍSTICAS PARA EL EVENTO...")
    event_stats = service.get_event_statistics(event_id)

    # 1. Gráfico de barras (categorías)
    print("\n1. ESTUDIANTES POR CATEGORÍA")
    print("-" * 70)
    for category, count in event_stats["students_by_category"].items():
        print(f"  {category}: {count} estudiantes")

    # 2. Gráfico de barras (áreas)
    print("\n2. ESTUDIANTES POR ÁREA")
    print("-" * 70)
    for area, count in event_stats["students_by_area"].items():
        print(f"  {area}: {count} estudiantes")

    # 3. Gráfico de líneas
    print("\n3. EVOLUCIÓN DE INSCRIPCIONES")
    print("-" * 70)
    for date, count in event_stats["inscriptions_timeline"].items():
        print(f"  {date}: {count} inscripciones")

    # 4. Gráfico circular (completados)
    print("\n4. PROPORCIÓN DE COMPLETADOS")
    print("-" * 70)
    print(f"  Completados: {event_stats['completion_ratio']['completed']}")
    print(f"  Incompletos: {event_stats['completion_ratio']['incomplete']}")

    # 5. Distribución de pagos
    print("\n5. DISTRIBUCIÓN POR ESTADO DE PAGO")
    print("-" * 70)
    for status, count in event_stats["payment_status_distribution"].items():
        print(f"  {status}: {count}")

    # 6. Gráfico de embudo
    print("\n6. EMBUDO DE INSCRIPCIONES")
    print("-" * 70)
    print(f"  Registrados: {event_stats['inscription_funnel']['registered']}")
    print(f"  Pago iniciado: {event_stats['inscription_funnel']['payment_started']}")
    print(f"  Pago completado: {event_stats['inscription_funnel']['payment_completed']}")

    # 7. Gráfico de barras apiladas (por área y estado)
    print("\n7. ESTUDIANTES POR ÁREA Y ESTADO")
    print("-" * 70)
    for area, status_data in event_stats["stacked_bar_data"].items():
        print(f"\nÁrea: {area}")
        for status, count in status_data.items():
            print(f"  {status}: {count}")

    # Convertir a formatos de gráficos
    print("\n\nFORMATOS LISTOS PARA FRONTEND:")
    print("-" * 70)

    # Gráfico de barras (categorías)
    bar_chart_cat = ChartDataConverter.convert_bar_chart(
        event_stats["students_by_category"],
        "Estudiantes por Categoría"
    )
    print("\nGRÁFICO DE BARRAS (Categorías):")
    print(json.dumps(bar_chart_cat, indent=2))

    # Gráfico de barras (áreas)
    bar_chart_area = ChartDataConverter.convert_bar_chart(
        event_stats["students_by_area"],
        "Estudiantes por Área"
    )
    print("\nGRÁFICO DE BARRAS (Áreas):")
    print(json.dumps(bar_chart_area, indent=2))

    # Gráfico de líneas
    line_chart = ChartDataConverter.convert_line_chart(
        event_stats["inscriptions_timeline"]
    )
    print("\nGRÁFICO DE LÍNEAS:")
    print(json.dumps(line_chart, indent=2))

    # Gráfico circular
    pie_chart = ChartDataConverter.convert_pie_chart(
        event_stats["completion_ratio"]["completed"],
        event_stats["completion_ratio"]["incomplete"]
    )
    print("\nGRÁFICO CIRCULAR:")
    print(json.dumps(pie_chart, indent=2))

    # Gráfico de embudo
    funnel_chart = ChartDataConverter.convert_funnel_chart(
        event_stats["inscription_funnel"]
    )
    print("\nGRÁFICO DE EMBUDO:")
    print(json.dumps(funnel_chart, indent=2))

    # Gráfico de barras apiladas
    stacked_bar = ChartDataConverter.convert_stacked_bar(
        event_stats["stacked_bar_data"]
    )
    print("\nGRÁFICO DE BARRAS APILADAS:")
    print(json.dumps(stacked_bar, indent=2))


if __name__ == "__main__":
    with app.app_context():
        # ID del evento a analizar
        event_id = 1

        print("=" * 70)
        print(f"GENERANDO ESTADÍSTICAS PARA EVENTO ID={event_id}")
        print("=" * 70)

        print_real_statistics_data(event_id)
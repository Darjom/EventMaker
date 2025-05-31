class ChartDataConverter:
    @staticmethod
    def convert_bar_chart(data: dict, title: str) -> dict:
        return {
            "labels": list(data.keys()),
            "datasets": [{
                "label": title,
                "data": list(data.values()),
                "backgroundColor": "rgba(54, 162, 235, 0.5)",
                "borderColor": "rgba(54, 162, 235, 1)",
                "borderWidth": 1
            }]
        }

    @staticmethod
    def convert_line_chart(timeline: dict) -> dict:
        return {
            "labels": [date.strftime("%Y-%m-%d") for date in sorted(timeline.keys())],
            "datasets": [{
                "label": "Inscripciones",
                "data": [timeline[date] for date in sorted(timeline.keys())],
                "fill": False,
                "borderColor": "rgb(75, 192, 192)",
                "tension": 0.1
            }]
        }

    @staticmethod
    def convert_pie_chart(completed: int, incomplete: int) -> dict:
        return {
            "labels": ["Completados", "Incompletos"],
            "datasets": [{
                "data": [completed, incomplete],
                "backgroundColor": ["rgba(75, 192, 192, 0.5)", "rgba(255, 99, 132, 0.5)"],
                "borderColor": ["rgba(75, 192, 192, 1)", "rgba(255, 99, 132, 1)"],
                "borderWidth": 1
            }]
        }

    @staticmethod
    def convert_funnel_chart(funnel_data: dict) -> dict:
        stages = ["Registrados", "Pago Iniciado", "Pago Completado"]
        return {
            "stages": stages,
            "values": [funnel_data["registered"], funnel_data["payment_started"], funnel_data["payment_completed"]]
        }

    @staticmethod
    def convert_stacked_bar(stacked_data: dict) -> dict:
        events = list(stacked_data.keys())
        statuses = ["Pendiente", "En Proceso", "Confirmado"]
        colors = ["rgba(255, 99, 132, 0.5)", "rgba(255, 205, 86, 0.5)", "rgba(75, 192, 192, 0.5)"]

        datasets = []
        for i, status in enumerate(statuses):
            datasets.append({
                "label": status,
                "data": [stacked_data[event].get(status, 0) for event in events],
                "backgroundColor": colors[i]
            })

        return {
            "events": events,
            "datasets": datasets
        }
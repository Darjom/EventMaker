

from modules.Data.DatosColegios.colegios_beni import colegios_beni
from modules.Data.DatosColegios.colegios_chuquisaca import colegios_chuquisaca
from modules.Data.DatosColegios.colegios_cochabamba import colegios_cochabamba
from modules.Data.DatosColegios.colegios_laPaz import colegios_la_paz
from modules.Data.DatosColegios.colegios_oruro import colegios_oruro
from modules.Data.DatosColegios.colegios_pando import colegios_pando
from modules.Data.DatosColegios.colegios_potosi import colegios_potosi
from modules.Data.DatosColegios.colegios_santaCruz import colegios_santa_cruz
from modules.Data.DatosColegios.colegios_tarija import colegios_tarija
import logging
from modules.schools.application.SchoolCreator import SchoolCreator
from modules.schools.infrastructure.PostgresSchoolRepository import PostgresSchoolRepository
from modules.schools.application.dtos.SchoolDTO import SchoolDTO


class CargarColegios:
    def __init__(self):
        self.schools_por_departamento = {
            "Beni": colegios_beni,
            "Chuquisaca": colegios_chuquisaca,
            "Cochabamba": colegios_cochabamba,
            "La Paz": colegios_la_paz,
            "Oruro": colegios_oruro,
            "Pando": colegios_pando,
            "Potosí": colegios_potosi,
            "Santa Cruz": colegios_santa_cruz,
            "Tarija": colegios_tarija
        }

    def main(self):
        repository = PostgresSchoolRepository()
        creator = SchoolCreator(repository)

        for departamento, colegios in self.schools_por_departamento.items():

            for nombre in colegios.values():
                try:
                    dto = SchoolDTO(name=nombre)
                    creator.execute(dto)

                except ValueError as ve:

                    pass

                except Exception as e:

                    logging.error(f"Error inesperado en {nombre}: {e}")



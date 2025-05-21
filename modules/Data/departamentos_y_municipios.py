def obtenerDepartamentos(data: dict) -> list:
    return list(data.keys())

def obtenerProvinciasPorDepartamento(data: dict, departamento: str) -> list:
    return data.get(departamento.upper(), [])

departamentos_bolivia = {
    "LA PAZ": [
        "ABEL ITURRALDE",
        "AROMA",
        "BAUTISTA SAAVEDRA",
        "CARANAVI",
        "ELIODORO CAMACHO",
        "FRANZ TAMAYO",
        "GUALBERTO VILLARROEL",
        "INGAVI",
        "INQUISIVI",
        "JOSÉ MANUEL PANDO",
        "LARECAJA",
        "LOAYZA",
        "LOS ANDES",
        "MANCO KAPAC",
        "MUÑECAS",
        "NOR YUNGAS",
        "OMASUYOS",
        "PACAJES",
        "PEDRO DOMINGO MURILLO",
        "SUD YUNGAS"
    ],
    "COCHABAMBA": [
        "CERCADO",
        "ARANI",
        "ARQUE",
        "AYOPAYA",
        "BOLÍVAR",
        "CAPINOTA",
        "CARRASCO",
        "CHAPARE",
        "ESTEBAN ARCE",
        "GERMÁN JORDÁN",
        "MIZQUE",
        "CAMPERO",
        "PUNATA",
        "QUILLACOLLO",
        "TAPACARÍ",
        "TIRAQUE"
    ],
    "SANTA CRUZ": [
        "ANDRÉS IBÁÑEZ",
        "ÁNGEL SANDOVAL",
        "CHIQUITOS",
        "CORDILLERA",
        "FLORIDA",
        "GERMÁN BUSCH",
        "GUARAYOS",
        "ICHILO",
        "IGNACIO WARNES",
        "JOSÉ MIGUEL DE VELASCO",
        "MANUEL MARÍA CABALLERO",
        "ÑUFLO DE CHÁVEZ",
        "OBISPO SANTISTEVAN",
        "SARA",
        "VALLEGRANDE",
        "WARNES"
    ],
    "ORURO": [
        "CERCADO",
        "CARANGAS",
        "EDUARDO AVAROA",
        "LADISLAO CABRERA",
        "LITORAL",
        "NOR CARANGAS",
        "PANTALEÓN DALENCE",
        "POOPÓ",
        "SAJAMA",
        "SAN PEDRO DE TOTORA",
        "SAUCARÍ",
        "SEBASTIÁN PAGADOR",
        "SUD CARANGAS",
        "TOMÁS BARRÓN",
        "MEJILLONES",
        "CHALLAPATA"
    ],
    "POTOSÍ": [
        "TOMÁS FRÍAS",
        "ALONSO DE IBÁÑEZ",
        "ANTONIO QUIJARRO",
        "BERNARDINO BILBAO",
        "CHARCAS",
        "CHAYANTA",
        "CORNELIO SAAVEDRA",
        "DANIEL CAMPOS",
        "ENRIQUE BALDIVIESO",
        "JOSÉ MARÍA LINARES",
        "MODESTO OMISTE",
        "NOR CHICHAS",
        "NOR LÍPEZ",
        "RAFAEL BUSTILLO",
        "SUD CHICHAS",
        "SUD LÍPEZ"
    ],
    "TARIJA": [
        "CERCADO",
        "ANICETO ARCE",
        "BURDET O'CONNOR",
        "EUSTAQUIO MÉNDEZ",
        "GRAN CHACO",
        "JOSÉ MARÍA AVILÉS"
    ],
    "CHUQUISACA": [
        "OROPEZA",
        "AZURDUY",
        "BELISARIO BOETO",
        "HERNANDO SILES",
        "JAIME ZUDÁÑEZ",
        "JUANA AZURDUY DE PADILLA",
        "LUIS CALVO",
        "NOR CINTI",
        "SUD CINTI",
        "TOMINA"
    ],
    "BENI": [
        "CERCADO",
        "BALLIVIÁN",
        "GENERAL JOSÉ BALLIVIÁN",
        "ITÉNEZ",
        "MAMORÉ",
        "MARBÁN",
        "MOXOS",
        "VACA DÍEZ"
    ],
    "PANDO": [
        "NICOLÁS SUÁREZ",
        "MANURIPI",
        "MADRE DE DIOS",
        "FEDERICO ROMÁN",
        "ABUNÁ"
    ]
}






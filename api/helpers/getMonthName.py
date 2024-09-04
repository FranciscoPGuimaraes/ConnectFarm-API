from typing import Optional

# Mapeamento de número do mês para nome do mês em português
MONTH_NAMES = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}


def get_month_name(month: int) -> Optional[str]:
    return MONTH_NAMES.get(month)

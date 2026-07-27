"""Conta visitas à caixa a partir de uma sequência de presença na região."""

from dataclasses import dataclass
from pathlib import Path
import csv


PROJECT_DIR = Path("/home/mauro/Projetos/fastcamp-dados-sinteticos")
OUTPUT_CSV = PROJECT_DIR / "outputs" / "projeto_final" / "visitas_simuladas.csv"


@dataclass
class Visita:
    inicio: float
    fim: float

    @property
    def duracao(self):
        return self.fim - self.inicio


class ContadorVisitas:
    """Confirma entrada e saída para evitar contagens causadas por ruído."""

    def __init__(self, quadros_confirmacao=2):
        self.quadros_confirmacao = quadros_confirmacao
        self.dentro = False
        self.presencas = 0
        self.ausencias = 0
        self.inicio_atual = None
        self.visitas = []

    def atualizar(self, tempo, presente_na_caixa):
        if presente_na_caixa:
            self.presencas += 1
            self.ausencias = 0
            if not self.dentro and self.presencas >= self.quadros_confirmacao:
                self.dentro = True
                # A visita começou no primeiro quadro da sequência confirmada.
                self.inicio_atual = tempo - (self.quadros_confirmacao - 1)
        else:
            self.ausencias += 1
            self.presencas = 0
            if self.dentro and self.ausencias >= self.quadros_confirmacao:
                fim = tempo - (self.quadros_confirmacao - 1)
                self.visitas.append(Visita(self.inicio_atual, fim))
                self.dentro = False
                self.inicio_atual = None


def demonstracao():
    # False = gato fora da região; True = gato detectado dentro da região.
    sequencia = [
        False, False,
        True, True, True, True, True,
        False, False, False,
        True, False,  # ruído isolado: não deve virar visita
        False,
        True, True, True, True,
        False, False,
    ]
    contador = ContadorVisitas(quadros_confirmacao=2)
    for segundo, presente in enumerate(sequencia):
        contador.atualizar(segundo, presente)

    assert len(contador.visitas) == 2, "A demonstração deveria conter 2 visitas."
    assert [visita.duracao for visita in contador.visitas] == [5, 4]

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["visita", "inicio_s", "fim_s", "duracao_s"])
        for indice, visita in enumerate(contador.visitas, start=1):
            escritor.writerow([indice, visita.inicio, visita.fim, visita.duracao])

    print(f"Visitas contabilizadas: {len(contador.visitas)}")
    for indice, visita in enumerate(contador.visitas, start=1):
        print(
            f"Visita {indice}: início={visita.inicio:.0f}s, "
            f"fim={visita.fim:.0f}s, duração={visita.duracao:.0f}s"
        )
    print(f"Resumo salvo em: {OUTPUT_CSV}")


if __name__ == "__main__":
    demonstracao()

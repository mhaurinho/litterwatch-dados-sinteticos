# Projeto final — Monitor sintético de visitas à caixa de areia

## Título provisório

**LitterWatch: detecção e contagem de visitas de um gato à caixa de areia com
dados sintéticos**

## Problema

Mudanças na frequência e na duração das visitas à caixa de areia podem ser
informações úteis para o acompanhamento do comportamento de um gato. A
observação manual é difícil, pois as visitas podem ocorrer durante a noite ou
quando o responsável não está presente.

O projeto não realizará diagnóstico veterinário. Seu objetivo será detectar a
presença de um gato na região da caixa, registrar início e fim de cada visita e
produzir uma contagem. Uma alteração no padrão poderá gerar um aviso para que o
responsável observe o animal e, quando necessário, procure orientação
veterinária.

## Escopo mínimo viável

1. Importar ou criar no Blender um modelo 3D de gato e uma caixa de areia.
2. Randomizar posição e pose do gato, câmera, iluminação, fundo e materiais.
3. Gerar imagens sintéticas com o gato dentro, próximo e fora da caixa.
4. Criar automaticamente caixas delimitadoras YOLO para a classe `gato`.
5. Separar o dataset em treino, validação e teste.
6. Treinar um detector pequeno exclusivamente com os dados sintéticos.
7. Definir uma região de interesse correspondente à caixa de areia.
8. Considerar uma visita quando o centro da detecção entra na região e
   permanece pelo número mínimo de quadros.
9. Encerrar a visita quando o gato sai da região por um intervalo mínimo.
10. Apresentar contagem de visitas, duração e exemplos de predição.

## O que ficará fora do escopo

- diagnosticar doença urinária;
- afirmar se ocorreu micção ou defecação apenas pela presença;
- medir volume, pH ou composição da urina;
- identificar vários gatos individualmente;
- implantar câmera e processamento em tempo real;
- validar clinicamente limites de alerta.

Esses itens exigiriam dados reais, acompanhamento veterinário, sensores
adicionais e um projeto maior.

## Por que o projeto é adequado ao FastCamp

- resolve um problema de detecção de objeto;
- utiliza um objeto do mundo real;
- exige cena e automação no Blender;
- permite domain randomization;
- gera anotações automaticamente;
- produz dataset organizado;
- inclui treinamento, mAP, exemplos visuais e análise de domain gap;
- acrescenta uma regra simples de contagem de eventos.

## Dados sintéticos planejados

Para manter o projeto executável no computador disponível:

- resolução: 320 × 320;
- quantidade inicial: 90 a 120 imagens;
- uma classe: `gato`;
- divisão aproximada: 80% treino, 10% validação e 10% teste;
- renderização: Blender Eevee em CPU;
- variações: câmera, iluminação, cor do gato, cor da caixa, pose, posição,
  fundo e oclusão parcial.

## Lógica de contagem

Uma única detecção não será contada diretamente como visita. Será utilizada uma
máquina de estados:

1. `fora`: nenhum gato confirmado na região da caixa;
2. `entrando`: detecção aparece na região por alguns quadros;
3. `dentro`: visita confirmada e cronômetro iniciado;
4. `saindo`: detecção desaparece ou deixa a região;
5. retorno a `fora`: visita encerrada e armazenada.

Essa lógica evita contar muitos quadros consecutivos como visitas diferentes.

## Limitações previstas

- O modelo treinado somente com imagens sintéticas pode sofrer `domain gap`.
- A oclusão causada pelas paredes da caixa pode dificultar a detecção.
- Uma câmera não confirma que o gato urinou.
- Uma visita curta pode representar curiosidade, limpeza ou passagem.
- Limites de frequência variam entre indivíduos e não serão definidos como
  critérios médicos.

## Critério de sucesso acadêmico

O projeto será considerado funcional quando:

- o pipeline gerar imagens e anotações sem intervenção manual;
- o dataset passar pelas validações de estrutura;
- o modelo produzir métricas no teste sintético;
- a demonstração contar corretamente eventos simulados;
- o relatório discutir honestamente limitações e domain gap.


# LitterWatch: monitor de visitas à caixa de areia com dados sintéticos

**Aluno:** Mauro Andrade  
**Curso:** FastCamp de Dados Sintéticos para Inteligência Artificial e Visão Computacional  
**Instituição:** Universidade Federal de Goiás  

## Resumo

Este projeto apresenta uma prova de conceito para detectar e contar visitas de
um gato a uma caixa de areia. Um pipeline em Blender e Python cria cenas
sintéticas, gera caixas delimitadoras no formato YOLO e organiza os dados em
treino, validação e teste. Um detector YOLO26n é treinado por transferência de
aprendizado, e uma máquina de estados transforma detecções consecutivas em
eventos com início, fim e duração. O objetivo é monitorar comportamento, não
diagnosticar doenças.

## 1. Problema e objetivo

Observar manualmente a frequência de uso da caixa de areia é difícil,
principalmente durante a noite ou na ausência do responsável. Mudanças de
comportamento podem ser relevantes, mas uma câmera isolada não confirma
micção, defecação ou doença.

O objetivo técnico foi construir um pipeline completo que detectasse a classe
`gato` e demonstrasse uma lógica de contagem de visitas. O escopo excluiu
diagnóstico, múltiplos gatos, sensores e implantação em tempo real.

## 2. Cena e dados sintéticos

A cena foi criada programaticamente no Blender 3.6.23. O gato simplificado
possui 13 componentes geométricos; a caixa contém base, paredes e areia. Foram
randomizados posição e rotação do gato, cor, intensidade e posição da luz e
altura da câmera.

O dataset contém 60 imagens de 320 × 320 pixels:

| Divisão | Imagens |
|---|---:|
| Treino | 48 |
| Validação | 6 |
| Teste | 6 |

Os estados comportamentais foram balanceados em 20 cenas `dentro`, 20
`proximo` e 20 `fora`.

## 3. Anotação automática

Cada parte do gato possui uma caixa tridimensional. Seus vértices foram
projetados na câmera, combinados e convertidos para coordenadas YOLO
normalizadas. O validador confirmou 60 pares imagem/rótulo, valores entre zero e
um e caixas com área positiva.

## 4. Treinamento

Foi utilizado YOLO26n por transferência de aprendizado, escolhido pelo baixo
custo computacional. Os principais parâmetros foram:

- 8 épocas;
- resolução 320;
- batch 2;
- execução em CPU;
- semente 20260727;
- uma classe: `gato`.

O treinamento curto foi deliberado: o objetivo era validar o pipeline, não
produzir um sistema clínico ou comercial.

## 5. Resultados

O modelo atingiu mAP50 de 0,942 na validação e 0,636 no teste sintético
separado. A diferença indica que o conjunto reduzido não sustenta conclusões
fortes sobre generalização. Na demonstração com seis imagens de teste, houve
detecção em todas elas usando limiar de confiança reduzido.

A máquina de estados foi testada com uma sequência simulada. Ela contabilizou
duas visitas, com durações de cinco e quatro segundos, e ignorou uma presença
isolada como ruído.

## 6. Limitações e domain gap

O modelo foi treinado e avaliado apenas em imagens sintéticas. O gato 3D possui
formas simples e não representa toda a variedade de pelagens, poses, tamanhos,
oclusões e condições de câmeras reais. Portanto, um bom resultado sintético não
comprova desempenho no mundo real.

A detecção de presença também não determina se houve eliminação. Monitoramento
urinário exigiria dados reais autorizados, sensores adicionais e validação
veterinária. O projeto deve ser interpretado apenas como monitor comportamental
experimental.

## 7. Conclusão

O projeto integrou modelagem e scripting no Blender, domain randomization,
anotação automática, organização de dataset, treinamento YOLO, avaliação e
contagem de eventos. A prova de conceito demonstra a viabilidade acadêmica da
ideia dentro de um escopo pequeno. Trabalhos futuros podem incorporar imagens
reais, sensores de peso e identificação individual.

## Referências

- ULTRALYTICS. *Ultralytics YOLO Documentation*.
- BLENDER FOUNDATION. *Blender Python API Documentation*.
- DENG, P. et al. Quantification of Urine Elimination Behaviors in Cats with
  a Video Recording System. *Journal of Veterinary Internal Medicine*, 2017.
- SUNG, Y. et al. Multi-Cat Monitoring System Based on Concept Drift Adaptive
  Machine Learning Architecture. *Sensors*, 2023.


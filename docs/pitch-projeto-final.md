# Roteiro do pitch — LitterWatch - para simpels conferência

##  Abertura e problema

Olá,  esse projeto se chama LitterWatch. A proposta
surgiu da dificuldade de acompanhar quantas vezes um gato utiliza a caixa de
areia, especialmente durante a noite ou quando o responsável está ausente.

## limite responsável

O sistema não diagnostica doenças e não confirma se o animal urinou. Ele é uma
prova de conceito para detectar presença, contar visitas e registrar duração.
Uma mudança de comportamento seria apenas um sinal para observação.

## Solução

Criei no Blender uma caixa de areia e um gato 3D simplificado. Com Python,
automatizei variações de posição, rotação, cor, iluminação e câmera. O pipeline
gerou 60 imagens sintéticas e suas anotações YOLO automaticamente, divididas em
treino, validação e teste.

## Modelo e resultados

Treinei um YOLO26n por oito epochs em CPU. O modelo atingiu mAP50 de 0,942 na
validação e 0,636 no teste sintético. O resultado é suficiente para demonstrar
o pipeline, mas a queda no teste mostra que não devemos afirmar generalização.

##  Contagem

Depois da detecção, implementei uma máquina de estados. Ela exige dois quadros
consecutivos para confirmar entrada ou saída. Assim, vários quadros do mesmo
evento viram uma visita, e uma detecção isolada pode ser ignorada como ruído.

## Limitações e encerramento

A principal limitação é o domain gap, porque o treinamento utilizou somente
imagens sintéticas e um gato simplificado. Como próximos passos, seria
necessário testar imagens reais, incluir sensores e buscar validação
veterinária. O projeto demonstrou um pipeline completo e reprodutível de dados
sintéticos para visão computacional.


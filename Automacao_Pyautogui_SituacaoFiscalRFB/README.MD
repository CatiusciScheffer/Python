#### Automação com Python e Pyautogui

---
 Esta automação foi feita pois precisávamos baixar mensalmente mais de 100 relatórios de Situação Fiscal no portal **ecac da Receita Federal**.
---

O código foi criado utilizando a biblioteca de Pyautogui pois a receita federal tem alguns bloqueios para uso do Selenium então consegui burlar isso com uso do pyautogui, claro que assim terei que ter uma máquina parada executando o código e também uma máquina específica pra isso, mas com esses requisitos o código atende a necessidade de fazer todas as consultas para cada cliente, baixando o termo de exclusão e a relação das pendências, o que economiza no mínimo 4 horas de trabaho de um funcionário.

Para utilização deste código é necessário utilizar um certificado de procurador e acessar o perfil dos clientes por procuração.

Será solicitado uma lista em csv separado por ponto e vígula, conforme modeloListaCNPJ.csv.
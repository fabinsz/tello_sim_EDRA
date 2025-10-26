# tello_sim_EDRA

__tello_sim_EDRA__ é uma versão adaptada da biblioteca [tello_sim](https://github.com/Fireline-Science/tello_sim) , desenvolvida pela [Fireline Science](https://github.com/Fireline-Science) especialmente criada para o __processo trainee da equipe EDRA__ — uma equipe universitária de drones da Universidade de Brasília (UnB).

Esta versão foi modificada para permitir __simulações personalizadas de missões__, voltadas ao desenvolvimento de lógica de controle, planejamento de rotas e estratégias de voo autônomo.
O foco é proporcionar aos trainees um ambiente realista e seguro para testar seus códigos __sem depender de um drone físico__.



## Sobre o Projeto Original
A biblioteca original, tello_sim, foi criada para simular comandos do drone __DJI Tello EDU__, baseada na interface da __easyTello__.
Ela permite que estudantes testem comandos como __takeoff__, __land__, __forward__, __cw__, entre outros, e visualizem a trajetória simulada com gráficos em Python.

Essa base foi adaptada pela equipe EDRA para:

- Introduzir novos modos de simulação;

- Ampliar a interatividade do ambiente;

- Criar desafios voltados ao treinamento de lógica e controle de drones.

## Instalação
Para instalar o __tello_sim_EDRA__, siga os passos:
```
git clone https://github.com/edra-unb/tello_sim_EDRA
cd tello_sim_EDRA
pip install .
```
> __Note:__ É recomendado o uso do Python 3.8+ e a instalação das dependências __pandas__ e __matplotlib__.
Caso use o [Anaconda](https://www.anaconda.com/download), essas bibliotecas já vêm incluídas.




## Uso Básico

Exemplo simples de uso no Python:
```
from tello_sim_EDRA import Simulator

drone = Simulator()
drone.takeoff()
drone.forward(50)
drone.cw(90)
drone.forward(100)
drone.land()

```
A simulação exibirá:

- A trajetória percorrida pelo drone;

- As posições atuais em X, Y, Z;

- Um gráfico representando o voo.


## Versão EDRA - Funcionalidades Adicionais
A versão EDRA inclui:

- Campo de simulação 2D customizado.

- Objetivos (“tesouros”) aleatórios a serem coletados.

- Geração dinâmica de cenários a cada reinício.

- Campo de visão do drone (detecção por área, não apenas por posição exata).

- Interface simplificada para desenvolvimento de lógica autônoma (como tomada de decisão e path planning).

O drone pode detectar um tesouro ao passar próximo ou dentro da sua área de visão (70x70), o que incentiva soluções estratégicas para otimizar o percurso e cobrir o mapa com o menor tempo possível.



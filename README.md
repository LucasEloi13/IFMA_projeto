# Person-Following-Robot-using-Deep-Learning

Bem-vindo ao repositório do Byte, um robô que segue pessoas! O sistema detecta uma pessoa usando redes neurais de arquitetura MobileNet e depois a segue através de um mecanismo de rastreamento usando sua distância e deslocamento físico.

Para a montagem deste protótipo, utilizou-se uma placa Raspberry Pi Model 3b+, uma webcam genérica e um kit de montagem de robôs de baixo custo. 

Para entender melhor seu funcionamento, veja o seguinte vídeo:
https://www.youtube.com/watch?v=FpdGG5FnGKM


## ☕ Funcionamento do Projeto

O fluxograma completo para o robô que segue pessoas pode ser divido nas seguintes quatro partes:

![funcionamento flux](https://user-images.githubusercontent.com/73032733/156447319-aab5c2c4-e40c-4fe9-867c-e32a15418184.png)

A Rede Neural Convolucional MobileNet foi utilizada para detectar pessoas em um determinado quadro RGB. Ao passar a imagem RGB no modelo e uma pessoa ser detectada, é retornado a coordenada cartesiana da caixa delimitadora. Para que sejam feitas as estimativas e correções, é calculada a centroide com os valores obtidos.

O controle de movimento é feito a partir de um mecanismo de acionamento diferencial. Esse sistema é baseado em parâmetros definidos previamente, e que podem ser ajustados de acordo as necessidades do usuário, estes preceitos serão chamados de tolerância. 

Quando o usuário estiver fora do limite definido como tolerável, serão feitos ajustes no movimento do robô para que os valores da centroide esteja dentro dos parâmetros estabelecidos, para facilitar o entendimento esse processo foi ilustrado na figura abaixo, as linhas verdes são os limites determinados anteriormente.

![coordenadas](https://user-images.githubusercontent.com/73032733/156448650-f7f9643d-d7fc-457f-81ab-06cd15e304e3.png)

Para controle de quando seguir em frente ou parar, o Y final é utilizado como base. Quando esta coordenada estiver acima dos parâmetros estabelecidos, o robô andará até o Y final ficar a baixo da tolerância.

O manuseio de curvas é feito com base nos parâmetros relacionados ao eixo X. O posicionamento do usuário será estimado utilizando a média entre o X inicial e final, este valor será comparado com os parâmetros de tolerância, caso seja maior o robô virará à esquerda e caso seja menor o robô virará à direita, esses movimentos serão feitos até que a centroide esteja dentro da projeção estipulada.


## 🚀 Execute Localmente

Para execultar o projeto em sua placa, siga os seguintes passos utilizando o terminal: 

* Execute o comando `git clone https://github.com/LucasEloi13/Person-Following-Robot-using-Deep-Learning.git` 
* Vá na pasta bash do repositório usando `cd bash_install`
* Execute o comando `bash auto_install.sh` e logo após `bash get_pi_requirements.sh`

E por fim, entre na pasta `<human_follower_try>` e execulte o arquivo `<tflite_plus_motor.py>`. 

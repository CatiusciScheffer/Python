<h1 align="center">POO PYTHON</h1>

TUDO EM PYTHON É UM OBJETO

- CLASSE = OBJETO
  - métodos: O que podemos fazer!
  - atributo: características o objeto!

VANTAGENS DO USO DE CLASSES:
- **Aproveitamento de código**;

- **Encapsulamento**: protejer o código à mudanças indesejadas(como na classe TV() o botão de volume não pode desligar a tv);

- **Polimorfismo**: um método pode ter várias *'formas'* em diferentes classes ou subclasses (como o métodos falar da classe Animais() vai agir de forma diferente nas subclasses Gato() x Cachorro());

CRIANDO CLASSE:

```python
class TV:

  def __init__(self):
    self.cor = 'preta'
    self.ligada = False
    self.canal = 12
    self.volume = 10

#o método __init__ define o que deve acontecer quando a classe é instanciada.

# o "self" é obrigatório dentro da classe,para que os atributos possam ser acessados na instâncias da classe.
```

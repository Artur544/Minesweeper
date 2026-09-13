import pyxel

class Goal:
    def __init__(self,x1,y1,largura,altura):
        self.x1 = x1
        self.y1 = y1
        self.largura = largura
        self.altura = altura
        self.cor = 15
    def desenha(self):
        pyxel.rect(self.x1,self.y1,self.largura,self.altura,self.cor)

class Parede:
    # Construtor
    def __init__(self, x1,y1,largura,altura):
        # Atributos
        self.x1 = x1
        self.y1 = y1
        self.largura = largura
        self.altura = altura
        self.cor = 9
    def desenha(self):
        pyxel.rect(self.x1,self.y1,self.largura,self.altura,self.cor)

class Personagem:
    # Construtor
    def __init__(self, x,y):
        # Atributos
        self.x1 = x
        self.y1 = y
        self.colImagem = 0
        self.linImagem = 0
        # personagem.png
        self.largura = 14
        self.altura = 18
        
    # Métodos
    def move(self,dx,dy):
        # Se movimento é para baixo pega a primeira linha da imagem
        if dy > 0:
            self.linImagem = 0
        # Se movimento é para cima pega a segunda linha da imagem
        elif dy < 0:
            self.linImagem = 1
        # Se movimento é para esquerda pega a terceira linha da imagem
        elif dx < 0:
            self.linImagem = 2
        # Se movimento é para direita pega a último linha da imagem
        elif dx > 0:
            self.linImagem = 3

        # Escolhe a coluna da imagem. 
        self.colImagem = (self.colImagem + 1) % 4
        
        # Move a imagem
        self.x1 = self.x1 + dx
        self.y1 = self.y1 + dy

    def desenha(self):
        # Desenha o objeto personagem
        # Se o personagem fosse um retângulo:
        # pyxel.rect(self.personagem.x1,self.personagem.y1,self.personagem.largura,self.personagem.altura,7)
        # Desenhando a imagem (sprite) carregada no init
        # Desenha o sprite
        # Calcula a posição
          xImagem = self.colImagem * self.largura
          yImagem = self.linImagem * self.altura
          pyxel.blt( self.x1,          # x de onde desenhar a imagem na janela.
                     self.y1,          # y de onde desenhar a imagem na janela.
                     0,                # qual das imagens (matrizes) que pyxel disponibiliza: 0, 1 ou 2.
                     xImagem,          # x na matriz (memória) onde a imagem está armazenada.
                     yImagem,          # y na matriz (memória) onde a imagem está armazenada.
                     self.largura,     # largura da imagem na matriz (memória) e na tela.
                     self.altura,      # altura da imagem na matriz (memória) e na tela.
                     7				   # cor que deve ser tratada como transparente.
                     )

class Janela:
    # Construtor
    def __init__(self,largura, altura):
        self.largura = largura
        self.altura = altura

class Jogo:
    # Construtor
    def __init__(self):
        #Atributos
        self.janela = Janela(200,80)
        self.heroi  = Personagem(10,20)
                
        self.paredes = []
        #Borda superior
        self.paredes.append(Parede(0,0,self.janela.largura,1))
        #Borda inferior
        self.paredes.append(Parede(0,self.janela.altura-1,self.janela.largura,1))
        #Borda esquerda
        self.paredes.append(Parede(0,0,1,self.janela.altura))
        #Borda direita
        self.paredes.append(Parede(self.janela.largura-1,0,1,self.janela.altura))
        # Paredes centrais 
        self.paredes.append(Parede(self.janela.largura//3,0,1,50))
        self.paredes.append(Parede(self.janela.largura * 2/3,self.janela.altura-50,1,50))

        self.fim = Goal(self.janela.largura - 20,self.janela.altura - 20,10,10)

        # Cria Janela
        pyxel.init(self.janela.largura,self.janela.altura,fps=10)
        
        # Carregar imagens (entre pyxel.init e pyxel.run)
        pyxel.image(0).load(0, 0, 'personagem_56x72.png')
        
        ## Roda o Jogo (sempre última linha do __init__
        pyxel.run(self.update, self.draw)

    # Métodos
    def update(self):
        # Testa se Bola pode ser movida antes de mover
        dx = 0
        dy = 0
        
        # Verifica o botão pressionado e verifica qual deslocamento fazer
        if pyxel.btn(pyxel.KEY_UP):
            dy = -4
        if pyxel.btn(pyxel.KEY_DOWN):
            dy = 4
        if pyxel.btn(pyxel.KEY_LEFT):
            dx = -4
        if pyxel.btn(pyxel.KEY_RIGHT):
            dx = 4
        
        if dx!=0 or dy!=0:
            move = True
            for parede in self.paredes:
                if self.colisao(self.heroi,dx,dy,parede):
                    move = False
            if move:
                self.heroi.move(dx,dy)
            
    # Testa a colisão de um retângulo+(dx,dy) com outro retângulo
    def colisao(self,rect1,dx,dy,rect2):
        # Limites da bola
        rect1_esq = rect1.x1 + dx
        rect1_dir = rect1.x1 + rect1.largura + dx
        rect1_top = rect1.y1 + dy
        rect1_dow = rect1.y1 + rect1.altura + dy
        
        # Limites da parede
        rect2_esq = rect2.x1 
        rect2_dir = rect2.x1 + rect2.largura
        rect2_top = rect2.y1 
        rect2_dow = rect2.y1 + rect2.altura
        
        # Bola ultrapassa limites das paredes?
        if (rect1_dir >= rect2_esq and
            rect1_esq <= rect2_dir and
            rect1_top <= rect2_dow and
            rect1_dow >= rect2_top):
            return True

        return False
            
            


    def draw(self):
        # Pinta a janela de preto (limpa a tela)
        pyxel.cls(0)
        
        # Desenha o objeto heroi da classe Personagem
        self.heroi.desenha()
                
        # Desenha o objeto fim da classe Goal
        self.fim.desenha()

        
        # Desenha as paredes
        for parede in self.paredes:
            parede.desenha()
        
        # Testa se o jogador chegou ao fim do labirinto
        if self.colisao(self.heroi,0,0,self.fim):
            pyxel.text(self.janela.largura//3,self.janela.altura//2,"You Win",15)


Jogo()






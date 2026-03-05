# ============================================================
#  Calculadora Científica com Histórico — Kivy
# ============================================================

import math
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window

# ── Configuração inicial da janela ──────────────────────────
Window.size = (420, 760)
Window.clearcolor = (0.08, 0.08, 0.12, 1)


# ── Função auxiliar para estilizar botões ──────────────────
def make_button(text, bg_color, font_size=20):
    """
    Cria e retorna um botão já estilizado.
    Parâmetros:
        text      — rótulo exibido no botão
        bg_color  — cor de fundo no formato RGBA [r, g, b, a]
        font_size — tamanho da fonte (padrão 20)
    """
    btn = Button(
        text=text,
        font_size=font_size,
        background_normal="",
        background_color=bg_color,
        color=(1, 1, 1, 1),
        bold=True,
        size_hint=(1, 1),
    )
    return btn


# ── Classe principal da aplicação ──────────────────────────
class CalculadoraCientifica(App):

    # ── Método chamado automaticamente ao iniciar o app ────
    def build(self):

        # Paleta de cores usada nos botões
        COR_NUMERO   = [0.18, 0.18, 0.26, 1]   # Cinza-azulado escuro
        COR_OPERADOR = [0.13, 0.45, 0.72, 1]   # Azul médio
        COR_CIENCIA  = [0.20, 0.55, 0.45, 1]   # Verde-petróleo
        COR_ESPECIAL = [0.72, 0.28, 0.28, 1]   # Vermelho suave
        COR_IGUAL    = [0.85, 0.45, 0.10, 1]   # Laranja vibrante

        # Variáveis de estado da calculadora
        self.operadores        = ["/", "*", "+", "-", "%"]
        self.last_was_op       = False
        self.resultado_exibido = False


        root = BoxLayout(orientation="vertical", padding=10, spacing=8)

        # ── VISOR PRINCIPAL ─────────────────────────────────
        self.visor = TextInput(
            multiline=False,
            readonly=True,
            halign="right",
            font_size=48,
            foreground_color=(1, 1, 1, 1),
            background_color=(0.12, 0.12, 0.20, 1),
            size_hint=(1, None),
            height=90,
            padding=[15, 20],
        )
        root.add_widget(self.visor)


        self.visor_expr = Label(
            text="",
            font_size=16,
            color=(0.55, 0.65, 0.80, 1),
            halign="right",
            valign="middle",
            size_hint=(1, None),
            height=28,
        )
        self.visor_expr.bind(size=self.visor_expr.setter("text_size"))
        root.add_widget(self.visor_expr)


        grid_ciencia = GridLayout(
            cols=4,
            spacing=6,
            size_hint=(1, None),
            height=200,
        )

        # Lista de botões científicos: (rótulo, texto enviado ao visor, cor)
        botoes_cientificos = [
            ("sin",  "sin(",  COR_CIENCIA),
            ("cos",  "cos(",  COR_CIENCIA),
            ("tan",  "tan(",  COR_CIENCIA),
            ("log",  "log(",  COR_CIENCIA),
            ("ln",   "ln(",   COR_CIENCIA),
            ("sqrt", "sqrt(", COR_CIENCIA),
            ("x²",   "**2",   COR_CIENCIA),
            ("xʸ",   "**",    COR_CIENCIA),
            ("pi",   "pi",    COR_CIENCIA),
            ("e",    "e",     COR_CIENCIA),
            ("(",    "(",     COR_OPERADOR),
            (")",    ")",     COR_OPERADOR),
            ("1/x",  "1/(",   COR_CIENCIA),
            ("|x|",  "abs(",  COR_CIENCIA),
            ("%",    "%",     COR_OPERADOR),
            ("±",    "neg",   COR_ESPECIAL),
        ]

        for rotulo, valor, cor in botoes_cientificos:
            btn = make_button(rotulo, cor, font_size=17)
            btn.valor = valor
            btn.bind(on_release=self.pressionar_botao)
            grid_ciencia.add_widget(btn)

        root.add_widget(grid_ciencia)


        grid_principal = GridLayout(
            cols=4,
            spacing=6,
            size_hint=(1, 1),
        )


        linhas = [
            [("C", "C", COR_ESPECIAL), ("⌫", "⌫", COR_ESPECIAL), ("( )", "()", COR_OPERADOR), ("/", "/", COR_OPERADOR)],
            [("7", "7", COR_NUMERO),   ("8", "8", COR_NUMERO),    ("9", "9", COR_NUMERO),      ("*", "*", COR_OPERADOR)],
            [("4", "4", COR_NUMERO),   ("5", "5", COR_NUMERO),    ("6", "6", COR_NUMERO),      ("-", "-", COR_OPERADOR)],
            [("1", "1", COR_NUMERO),   ("2", "2", COR_NUMERO),    ("3", "3", COR_NUMERO),      ("+", "+", COR_OPERADOR)],
            [("0", "0", COR_NUMERO),   (".", ".", COR_NUMERO),     ("00","00",COR_NUMERO),      ("=", "=", COR_IGUAL)],
        ]

        for linha in linhas:
            for rotulo, valor, cor in linha:
                btn = make_button(rotulo, cor)
                btn.valor = valor
                btn.bind(on_release=self.pressionar_botao)
                grid_principal.add_widget(btn)

        root.add_widget(grid_principal)


        lbl_historico = Label(
            text="Histórico",
            font_size=14,
            color=(0.55, 0.65, 0.80, 1),
            size_hint=(1, None),
            height=22,
            halign="left",
        )
        lbl_historico.bind(size=lbl_historico.setter("text_size"))
        root.add_widget(lbl_historico)

        scroll = ScrollView(
            size_hint=(1, None),
            height=110,
        )


        self.historico_layout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=2,
        )
        self.historico_layout.bind(
            minimum_height=self.historico_layout.setter("height")
        )

        scroll.add_widget(self.historico_layout)
        root.add_widget(scroll)

        return root

    # ── Manipulador principal de botões ────────────────────
    def pressionar_botao(self, instance):
        """
        Chamado sempre que o usuário toca em qualquer botão.
        Decide o que fazer com base no valor do botão pressionado.
        """
        atual = self.visor.text
        valor = instance.valor
        # C: limpa tudo ──────────────────────────────────
        if valor == "C":
            self.visor.text        = ""
            self.visor_expr.text   = ""
            self.last_was_op       = False
            self.resultado_exibido = False

        #: apaga o último caractere ────────────────────
        elif valor == "⌫":
            self.visor.text = atual[:-1]

        #= : calcula o resultado ─────────────────────────
        elif valor == "=":
            self.calcular()                      # Chama o método de cálculo

        #neg: inverte o sinal do número atual ───────────
        elif valor == "neg":
            if atual and atual != "-":           # Só age se houver algo no visor
                try:
                    num = float(atual)
                    self.visor.text = str(-num)
                except ValueError:
                    pass

        #() inteligente: abre ou fecha parêntese ────────
        elif valor == "()":
            abertos = atual.count("(") - atual.count(")")
            if abertos <= 0 or atual.endswith(tuple(self.operadores)):
                self.visor.text += "("
            else:
                self.visor.text += ")"

        #Qualquer outro valor (número, operador, função) ─
        else:
            # Se um resultado foi exibido e o usuário digita um número > reinicia
            if self.resultado_exibido and valor not in self.operadores:
                self.visor.text        = ""
                self.visor_expr.text   = ""
                self.resultado_exibido = False

            # Bloqueia dois operadores seguidos
            if self.last_was_op and valor in self.operadores:
                return

            # Bloqueia começar com operador (exceto "-" para negativo)
            if atual == "" and valor in self.operadores and valor != "-":
                return

            self.visor.text    += valor
            self.last_was_op    = valor in self.operadores
            self.resultado_exibido = False

    #Método de cálculo ───────────────────────────────────
    def calcular(self):
        """
        Avalia a expressão exibida no visor e mostra o resultado.
        Salva a operação no histórico.
        """
        expressao = self.visor.text

        if not expressao:
            return

        expressao_original = expressao

        try:
            # Substitui constantes e funções pelo equivalente Python/math
            expressao = expressao.replace("pi",    str(math.pi))
            expressao = expressao.replace("e",     str(math.e))
            expressao = expressao.replace("sin(",  "math.sin(math.radians(")
            expressao = expressao.replace("cos(",  "math.cos(math.radians(")
            expressao = expressao.replace("tan(",  "math.tan(math.radians(")
            expressao = expressao.replace("log(",  "math.log10(")
            expressao = expressao.replace("ln(",   "math.log(")
            expressao = expressao.replace("sqrt(", "math.sqrt(")
            expressao = expressao.replace("abs(",  "abs(")

            # Para sin/cos/tan adiciona ) extra para fechar o math.radians(
            for fn in ["math.sin(math.radians(",
                       "math.cos(math.radians(",
                       "math.tan(math.radians("]:
                while fn in expressao:
                    idx        = expressao.find(fn) + len(fn)
                    profund    = 1
                    pos        = idx
                    while pos < len(expressao) and profund > 0:
                        if expressao[pos]   == "(": profund += 1
                        elif expressao[pos] == ")": profund -= 1
                        pos += 1

                    expressao = expressao[:pos-1] + ")" + expressao[pos-1:]
                    break

            resultado = eval(expressao)


            if isinstance(resultado, float) and resultado.is_integer():
                resultado_str = str(int(resultado))
            else:
                resultado_str = f"{resultado:.10g}"

            self.visor_expr.text   = expressao_original + " ="
            self.visor.text        = resultado_str
            self.resultado_exibido = True
            self.last_was_op       = False

            self.adicionar_historico(expressao_original, resultado_str)

        except ZeroDivisionError:
            self.visor.text = "Erro: Div/0"      # Erro específico de divisão por zero
        except Exception:
            self.visor.text = "Erro"             # Qualquer outro erro de cálculo

    # ── Método que registra no histórico ───────────────────
    def adicionar_historico(self, expressao, resultado):
        """
        Cria um Label com a operação realizada e adiciona
        ao topo do histórico (mais recente primeiro).
        """
        entrada = Label(
            text=f"{expressao}  =  {resultado}",
            font_size=13,
            color=(0.75, 0.85, 1.0, 1),
            size_hint=(1, None),
            height=26,
            halign="right",
        )
        entrada.bind(size=entrada.setter("text_size"))


        self.historico_layout.add_widget(
            entrada,
            index=len(self.historico_layout.children)
        )


        if len(self.historico_layout.children) > 20:
            ultimo = self.historico_layout.children[-1]
            self.historico_layout.remove_widget(ultimo)



if __name__ == "__main__":
    CalculadoraCientifica().run()
PROMPT = """
Sua tarefa é APENAS realizar OCR.
Leia todos os caracteres visíveis da imagem.
Copie o texto exatamente como aparece.

Não escreva frases de complementares, me entregue somente o que foi lido da imagem!!!

Preserve:
- quebras de linha
- ordem do texto

Se uma palavra estiver difícil de ler:
- escreva sua melhor interpretação
- Nunca pule palavras.
- A quantidade de linhas retornadas deve ser semelhante à quantidade de linhas visíveis na imagem.
- Dê atenção especial ao texto manuscrito.
- Textos manuscritos são mais importantes que cabeçalhos, rodapés, telefones ou informações institucionais.

Mesmo quando a escrita for difícil:

- tente transcrever
- não resuma
- não substitua por explicações

Retorne APENAS a transcrição.
"""
from search import search_prompt


def main():
    """
    Interface de linha de comando (CLI) para fazer perguntas sobre o documento PDF.

    O usuário pode fazer perguntas e receber respostas baseadas apenas no conteúdo
    do PDF que foi previamente ingerido no banco de dados vetorial.
    """
    print("=" * 80)
    print("CHAT - Busca Semântica sobre o PDF")
    print("=" * 80)
    print("\nInicializando o sistema de busca...")

    try:
        # Inicializar a chain de busca
        chain = search_prompt()

        if not chain:
            print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
            return

        print("✓ Sistema inicializado com sucesso!")
        print("\nDigite 'sair' ou 'exit' para encerrar o chat.\n")
        print("=" * 80)

        # Loop principal do chat
        while True:
            # Solicitar pergunta do usuário
            print("\nFaça sua pergunta:")
            pergunta = input("PERGUNTA: ").strip()

            # Verificar se o usuário quer sair
            if pergunta.lower() in ['sair', 'exit', 'quit', 'q']:
                print("\nEncerrando o chat. Até logo!")
                break

            # Verificar se a pergunta não está vazia
            if not pergunta:
                print("⚠ Por favor, digite uma pergunta válida.")
                continue

            # Executar a busca e obter a resposta
            try:
                print("\nProcessando sua pergunta...\n")
                resposta = chain.invoke(pergunta)
                print(f"RESPOSTA: {resposta}")
                print("\n" + "-" * 80)

            except Exception as e:
                print(f"\n❌ ERRO ao processar a pergunta: {str(e)}")
                print("Por favor, tente novamente.\n")

    except Exception as e:
        print(f"\n❌ ERRO ao inicializar o chat: {str(e)}")
        print("\nCertifique-se de que:")
        print("1. O banco de dados PostgreSQL está rodando (docker-compose up -d)")
        print("2. Você executou o script de ingestão (python src/ingest.py)")
        print("3. As variáveis de ambiente estão configuradas corretamente no arquivo .env")
        import traceback
        traceback.print_exc()
        return


if __name__ == "__main__":
    main()
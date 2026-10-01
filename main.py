#======================
# BIBLIOTECAS
#======================
import os
import subprocess
import discord
from discord.ext import commands
from dotenv import load_dotenv

#======================
# CLASSES  
#======================

class DiscordShell: # Removido o underline inicial (melhor prática de nomenclatura)
    def __init__(self):
        pass

    async def commandExec(self, command: str) -> str:
        if not command: # Forma mais pythônica de checar string vazia ou None
            print("Parâmetro [command] veio vazio, coloque um dado válido")
            return "Nenhum comando fornecido."
        
        # Executa o comando no terminal do sistema
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )
        
        # Retorna a saída padrão ou o erro caso o comando falhe
        if result.returncode == 0:
            return result.stdout if result.stdout else "Comando executado com sucesso (sem saída)."
        else:
            return result.stderr if result.stderr else f"Erro desconhecido. Código: {result.returncode}"

#======================
# INIT 
#======================
if __name__ == "__main__":
    load_dotenv()
    BOT_PREFIX: str = ";"
    BOT_TOKEN: str = "MTU1NDk5Mzk0MTM5MTM1MTgyOA.GD1fqG.7UyjgmGVaSdtqp1vmkVTWSFGstCKNDAResJO-I"

    cShell = DiscordShell()
    
    intents = discord.Intents.all()

    Bot = commands.Bot(
        command_prefix=BOT_PREFIX,
        intents=intents
    )
    
    @Bot.command(name="ping") # Corrigida a sintaxe do decorador
    async def ping(ctx):
        await ctx.send("pong :)")

    @Bot.command(name="shell") # Corrigida a sintaxe do decorador
    async def shell(ctx, *, command: str = None): # Definido default None para evitar erro se o usuário não digitar nada
        if command is None:
            await ctx.send("Por favor, digite o argumento comando! Exemplo: `!shell ping 8.8.8.8`")
            return

        # Adicionado o await obrigatório para funções assíncronas
        result_text = await cShell.commandExec(command)
        
        # Limita a resposta para não estourar o limite de 2000 caracteres do Discord
        if len(result_text) > 1900:
            result_text = result_text[:1900] + "\n...[Saída muito longa cortada]..."

        # Envia formatado como bloco de código para melhor leitura
        await ctx.send(f"```bash\n{result_text}\n```")
        
    Bot.run(token=BOT_TOKEN)

import discord


from discord.ext import commands
from util import coliru


class Eval:
    """Evaluation Command(s) using the Coliru API."""
    def __init__(self, bot):
        self.bot = bot

    def __unload(self):
        pass

    @commands.command(name='eval')
    @commands.cooldown(rate=1, per=60., type=commands.BucketType.user)
    async def eval_(self, ctx, *, code_block: str):
        """Evaluate the given Codeblock. The language must be specified in the highlighter."""
        lang = code_block[3:6].replace(' ', '').replace('\n', '')
        if lang not in coliru.LANGS:
            await ctx.send(embed=discord.Embed(
                title='Eval: Unknown Language',
                description=f'Known laanguages: {", ".join(coliru.LANGS)}',
                colour=discord.Colour.blue()
            ))
        else:
            code = code_block.strip('`')[len(lang):]
            result = await coliru.evaluate(lang, code)
            await ctx.send(embed=discord.Embed(
                title='Eval Results'
            ).add_field(
                name='Output',
                value=f'```{lang}\n{result}```'
            ))


def setup(bot):
    bot.add_cog(Eval(bot))

# 쿨다운과 동시 실행 제한

명령어가 지나치게 자주 호출되거나, 동시에 여러 사용자가 실행하면 봇이 과부하를 겪을 수 있습니다. `discord.py`는 이러한 상황을 대비해 **쿨다운(cooldown)** 기능과 **동시 실행 제한(max_concurrency)** 데코레이터를 제공합니다. 이 장에서는 각 기능을 사용해 스팸을 방지하고 자원을 보호하는 방법을 설명합니다.

## 쿨다운 데코레이터

`commands.cooldown(rate, per, type)` 데코레이터를 사용하면 명령어를 일정 횟수 이상 호출하지 못하도록 제한할 수 있습니다. `rate`는 허용 횟수, `per`는 기간(초), `type`은 제한 범위(사용자/서버/채널)를 정의합니다. 예를 들어, 한 사용자가 10초당 한 번만 실행할 수 있는 명령은 다음과 같이 작성합니다:

```python
@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command()
async def hello(ctx):
    await ctx.send("안녕하세요!")

@hello.error
async def hello_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"잠시만 기다려 주세요. {error.retry_after:.1f}초 후에 다시 시도하세요.")
```

위 예제에서는 쿨다운에 걸렸을 때 사용자에게 남은 시간을 알려줍니다. `BucketType`은 `default`(명령 전체), `user`, `guild`, `channel` 등 다양한 범위를 지정할 수 있습니다.

## 동시 실행 제한

어떤 명령은 동시에 여러 인스턴스가 실행되면 충돌을 일으킬 수 있습니다. `commands.max_concurrency(number, per)` 데코레이터를 사용해 동시에 실행할 수 있는 개수를 제한할 수 있습니다. 예를 들어, 투표 명령을 한 서버에서 한 번만 실행하도록 하고 싶다면:

```python
@commands.max_concurrency(1, per=commands.BucketType.guild)
@bot.command()
async def vote(ctx):
    # 투표 진행 로직
    await ctx.send("투표를 시작합니다!")
```

`max_concurrency`를 지정하면 명령이 이미 실행 중인 경우 `MaxConcurrencyReached` 예외가 발생하며, 이를 `on_command_error`에서 처리할 수 있습니다.

## 요약

쿨다운과 동시 실행 제한을 적절히 설정하면 명령어 남용을 방지하고 봇의 안정성을 높일 수 있습니다. 사용자가 쿨다운에 걸렸을 때 안내 메시지를 제공하면 불필요한 혼란을 줄일 수 있습니다.


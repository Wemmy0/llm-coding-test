# llm-coding-test

Results of a coding test given to a range of LLMs

### Prompt used:

```
Give me a python program of a spinning hexagon in the center of the screen with a red ball bouncing
around realisticly inside. The ball should be affected by gravity and its physics should be realistic
```

## Results:

|                    | DeepSeek R1 8b    | DeepSeek R1 14b   | DeepSeek R1 32b | DeepSeek R1 70b | DeepSeek R1 671b | ChatGPT o3-mini | Gemini 2.0 Flash (4000 output tok) | Gemini 2.0 Flash (8192 output tok) | Claude 3.5 Sonnet |
|--------------------|-------------------|-------------------|-----------------|-----------------|------------------|-----------------|------------------------------------|------------------------------------|-------------------|
| Runs?              | ❌ - Syntax Errors | ❌ - Syntax Errors | 🔶              | ✅               | ✅                | ✅               | ✅                                  | ✅                                  | ✅                 |
| Realistic Physics? | -                 | -                 | ❌               | ❌               | ✅                | ✅               | ✅                                  | ❌                                  | ✅                 |

Realistically, I wasn't expecting DeepSeek R1 8b & 14b a good result, but still disapointing they
don't produce valid python code

### DeepSeek R1 32b

Produced valid python code, however I wouldn't class this as "running" as there is no hexagon and
the ball just falls away.

![](https://raw.githubusercontent.com/Wemmy0/llm-coding-test/master/GIFs/DeepSeek%20R1%2032b.gif)

### DeepSeek R1 70b

Again, produced valid python code, and there is a hexagon this time but when the ball comes to a rest
it just stays still not colliding with the hexagon.

![](https://raw.githubusercontent.com/Wemmy0/llm-coding-test/master/GIFs/DeepSeek%20R1%2070b.gif)

### DeepSeek R1 (671b)

DeepSeek wasn't great, getting beat by its distilled 70b model. It also spent ages reasoning and
took a large number of attempts to get past the "The server is busy. Please try again later."

Eventually after getting an answer, the result was still disappointing.
Physics works fine for a few seconds until the ball interacts with a vertex of the hexagon - at this
point the ball glitches out of the hexagon and falls into the void.

![](https://raw.githubusercontent.com/Wemmy0/llm-coding-test/master/GIFs/DeepSeek%20R1.gif)

### ChatGPT o3-mini

I don't have ChatGPT Plus so ChatGPT o3-mini is the best I can get
It produced decent physics however a bit bouncy. But overall, the result is very good.

![](https://raw.githubusercontent.com/Wemmy0/llm-coding-test/master/GIFs/ChatGPT%20o3-mini.gif)

### Gemini 2.0 Flash

Gemini had very realistic physics - despite it's lack of reasoning making it one of the fastest
models to answer
It also successfully answered a followup prompt to add keyboard hotkeys to change the hexagon speed
and more. (included)

However, ONLY if you limit it's output tokens to 4000. I tried 8192, and it was significantly worse

![](https://raw.githubusercontent.com/Wemmy0/llm-coding-test/master/GIFs/Gemini%202.0%20Flash.gif)

### Gemini 2.0 Flash 8192 tok

I have no idea why but this produces a very disappointing result. The ball clips through the hexagon
and falls out of the hexagon

![](https://raw.githubusercontent.com/Wemmy0/llm-coding-test/master/GIFs/Gemini%202.0%20Flash%208192%20tok.gif)

### Claude 3.5 Sonnet

Like ChatGPT o3-mini, result was very good and unlike o3-mini, it produces the result much faster

![](https://raw.githubusercontent.com/Wemmy0/llm-coding-test/master/GIFs/Claude%203.5%20Sonnet.gif)

## Conclusion - some weird results

As expected, Claude Sonnet and ChatGPT o3-mini preformed consistently the best. However, Gemini 2.0 Flash
is a surprising underdog. But the issue with a larger `Max Output Tokens` causing the output quality
to decrease is confusing. This could be to Gemini 2.0 Flash's attention span.

I think it's a good idea to use Claude or ChatGPT for their top tier responses, however when rate limits
start getting in the way, use Gemini 2.0 Flash with a smaller maximum output tokens.

## Tools used

I used [Msty](https://msty.app/) to run a lot of these models, with the exception of ChatGPT, Claude
and DeepSeek R1 671b.

[Openrouter](https://openrouter.ai/) was used for DeepSeek R1 70b and  Gemini 2.0 Flash.
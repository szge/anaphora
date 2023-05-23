## Anaphora Resolution Experimentation Results

1. One downside of GPT for text classification/regression is that it outputs text/strings, and it's hard to modify to output numerical values since we don't have access to fine-tuning or weights or hidden layers.
2. For anaphora resolution, if you give GPT the whole article, and ask it to figure out the antecedent, it does a decent job.
    - Prompt: "In the sentence "...", who does the pronoun "X" refer to? Output only the name, without a period at the end."
    - Works for simple sentences and articles (not too many subjects in article, only one pronoun)
3. For multiple pronouns, this process is trickier.
    - GPT doesn't do to well when asked to list every pronoun in rows.
    - A better attempt is to go through each pronoun one-by-one with a little bit of context.
    - Example: "In the sentence "He continued: 'I didn't know there were a bunch of people, thousands in my city that were convening in the basements of churches and random old halls and talking about this disease that I had. I didn't even know it was a disease at the beginning.", who does the pronoun "I" in "I didn't know..." refer to? Output only the name, without a period at the end."

[Article](https://www.dailymail.co.uk/tvshowbiz/article-9203047/Macklemore-37-says-dead-father-not-spent-10K-send-rehab.html)

[Playground](https://platform.openai.com/playground?mode=chat), go to History
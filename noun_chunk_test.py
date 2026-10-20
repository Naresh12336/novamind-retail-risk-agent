from engine.text_preprocessor import TextPreprocessor

preprocessor = TextPreprocessor()

result = preprocessor.process(
    "John did not authorize the transfer."
)

print("Result type:", type(result))
print("Noun chunks:", result.noun_chunks)
print("Negations:", result.negations)
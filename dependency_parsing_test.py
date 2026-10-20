from engine.text_preprocessor import TextPreprocessor

preprocessor = TextPreprocessor()

result = preprocessor.process(
    "Priya received money from John yesterday."
)

for relation in result.dependency_relations:
    print(relation)

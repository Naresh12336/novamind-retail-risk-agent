from collections import defaultdict

# ==========================================
# ENTITY REGISTRY
# ==========================================
entity_registry = defaultdict(set)


def register_entity(
    entity_type,
    entity_value
):

    if not entity_value:
        return

    entity_registry[
        entity_type
    ].add(
        entity_value
    )
feedback_store = []


def record_feedback(
    case_id,
    analyst,
    verdict,
    notes=""
):

    feedback_store.append({

        "case_id":
            case_id,

        "analyst":
            analyst,

        "verdict":
            verdict,

        "notes":
            notes
    })

    return True
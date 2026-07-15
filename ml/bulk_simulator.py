from engine.processor import process_transaction

from ml.synthetic_data_generator import (
    generate_dataset
)

# ==========================================
# CONFIGURATION
# ==========================================
SIMULATION_SIZE = 5000

PROGRESS_INTERVAL = 100


# ==========================================
# MAIN SIMULATION
# ==========================================
def run_simulation():

    print("\n==========================================")
    print("GENERATING SYNTHETIC TRANSACTIONS")
    print("==========================================\n")

    transactions = generate_dataset(
        size=SIMULATION_SIZE
    )

    print(
        f"Generated {len(transactions)} transactions.\n"
    )

    print("==========================================")
    print("RUNNING FRAUD ENGINE")
    print("==========================================\n")

    success = 0
    failures = 0

    risk_distribution = {
        "Low": 0,
        "Medium": 0,
        "High": 0
    }

    action_distribution = {}

    for index, transaction in enumerate(
        transactions,
        start=1
    ):

        try:

            result = process_transaction(
                transaction
            )

            success += 1

            # ----------------------------------
            # RISK DISTRIBUTION
            # ----------------------------------
            risk = result.get(
                "risk_category",
                "Unknown"
            )

            risk_distribution[risk] = (
                risk_distribution.get(risk, 0)
                + 1
            )

            # ----------------------------------
            # ACTION DISTRIBUTION
            # ----------------------------------
            action = result.get(
                "recommended_action",
                "Unknown"
            )

            action_distribution[action] = (
                action_distribution.get(
                    action,
                    0
                ) + 1
            )

            # ----------------------------------
            # PROGRESS
            # ----------------------------------
            if index % PROGRESS_INTERVAL == 0:

                print(
                    f"\nProcessed {index}/{SIMULATION_SIZE}"
                )

                print(
                    "Risk:",
                    risk
                )

                print(
                    "Action:",
                    action
                )

                print(
                    "Infrastructure Score:",
                    result.get(
                        "infrastructure_score",
                        0
                    )
                )

                print(
                    "Merchant Score:",
                    result.get(
                        "merchant_score",
                        0
                    )
                )

                print(
                    "Trust Score:",
                    result.get(
                        "trust_score",
                        0
                    )
                )

                print(
                    "Threat Score:",
                    result.get(
                        "threat_score",
                        0
                    )
                )

                print(
                    "ASN Signals:",
                    result.get(
                        "asn_signals",
                        []
                    )
                )

                print(
                    "Geo Signals:",
                    result.get(
                        "geo_signals",
                        []
                    )
                )

                print(
                    "Merchant Signals:",
                    result.get(
                        "merchant_signals",
                        []
                    )
                )

                print(
                    "ML Probability:",
                    result.get(
                        "ml_probability",
                        0
                    )
                )

        except Exception as e:

            failures += 1

            print(
                "\nSIMULATION ERROR:",
                str(e)
            )

    # ======================================
    # SUMMARY
    # ======================================
    print("\n==========================================")
    print("SIMULATION COMPLETE")
    print("==========================================")

    print(
        f"\nSuccessful Transactions : {success}"
    )

    print(
        f"Failed Transactions     : {failures}"
    )

    print("\nRisk Distribution")

    for risk, count in risk_distribution.items():

        print(
            f"  {risk:<8}: {count}"
        )

    print("\nAction Distribution")

    for action, count in sorted(
        action_distribution.items()
    ):

        print(
            f"  {action:<32}: {count}"
        )


# ==========================================
# ENTRYPOINT
# ==========================================
if __name__ == "__main__":

    run_simulation()
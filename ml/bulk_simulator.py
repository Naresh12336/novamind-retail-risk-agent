from engine.processor import process_transaction

from ml.synthetic_data_generator import (
    generate_dataset
)

# ==========================================
# CONFIG
# ==========================================
SIMULATION_SIZE = 5000

# ==========================================
# MAIN SIMULATION
# ==========================================
def run_simulation():

    print("\nGENERATING TRANSACTIONS...\n")

    transactions = generate_dataset(
        size=SIMULATION_SIZE
    )

    print(
        f"{len(transactions)} transactions generated"
    )

    print("\nRUNNING FRAUD ENGINE...\n")

    success = 0
    failures = 0

    for i, tx in enumerate(transactions):

        try:

            result = process_transaction(tx)

            success += 1

            # ----------------------------------
            # PROGRESS
            # ----------------------------------
            if i % 100 == 0:

                print(
                    f"\nProcessed: {i}"
                )

                print(
                    "Risk:",
                    result.get(
                        "risk_category"
                    )
                )

                print(
                    "Action:",
                    result.get(
                        "recommended_action"
                    )
                )

                print(
                    "ASN:",
                    result.get(
                        "asn_signals"
                    )
                )

                print(
                    "Geo:",
                    result.get(
                        "geo_signals"
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
    print("\nSIMULATION COMPLETE")

    print(
        f"\nSuccessful: {success}"
    )

    print(
        f"Failed: {failures}"
    )


# ==========================================
# ENTRYPOINT
# ==========================================
if __name__ == "__main__":

    run_simulation()
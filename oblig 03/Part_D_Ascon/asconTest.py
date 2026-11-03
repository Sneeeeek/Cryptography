import ascon
import base64

# Liste med filnavn
filenames = ["test1", "test2", "test3", "test4", "test5"]

print("Test av ascon hash:")

# For hver filnavn
for filename in filenames:

    # Les fila
    with open(f"oblig 03/Part_D_Ascon/{filename}.txt", "rb") as f:
        data = f.read()

        # Hash med ascon
        hash = ascon.ascon_hash(data, variant="Ascon-Hash256", hashlength=32)

        # Base64 encode det
        base64_output = base64.b64encode(hash).decode('utf-8')

    # Les asig fila som hører til
    with open(f"oblig 03/Part_D_Ascon/{filename}.txt.asig", "r", encoding="utf-8") as f:

        # Sjekk til vi finner linja med signaturen
        for line in f:
            if line.startswith("Base64-sig:"):

                # Split opp og trim slik at får bare signaturen 
                signature = line.split(":", 1)[1].strip()
                break

    # Skriv ut begge
    print(f"\n{filename}")
    print("Hash:",base64_output)
    print("Sig: ",signature)
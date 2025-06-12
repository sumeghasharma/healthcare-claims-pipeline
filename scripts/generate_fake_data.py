from faker import Faker
import pandas as pd
import random
from datetime import timedelta

fake = Faker()

# Generate Patients
def generate_patients(n):
    patients = []
    for i in range(n):
        patients.append({
            'patient_id': i + 1,
            'name': fake.name(),
            'dob': fake.date_of_birth(minimum_age=0, maximum_age=90),
            'gender': random.choice(['Male', 'Female', 'Other']),
            'insurance_id': fake.uuid4()
        })
    return pd.DataFrame(patients)

# Generate Providers
def generate_providers(n):
    providers = []
    for i in range(n):
        providers.append({
            'provider_id': i + 1,
            'name': fake.company(),
            'specialty': random.choice(['Cardiology', 'Dermatology', 'General Practice', 'Oncology']),
            'npi_number': fake.unique.random_number(digits=10)
        })
    return pd.DataFrame(providers)

# Generate Claims
def generate_claims(n, patient_df, provider_df):
    claims = []
    for i in range(n):
        patient = patient_df.sample().iloc[0]
        provider = provider_df.sample().iloc[0]
        claim_date = fake.date_between(start_date='-1y', end_date='today')
        amount = round(random.uniform(50, 1000), 2)

        claims.append({
            'claim_id': i + 1,
            'patient_id': patient['patient_id'],
            'provider_id': provider['provider_id'],
            'claim_date': claim_date,
            'procedure_code': fake.random_element(elements=('99213', '99214', '93000', '87070', '80050')),
            'diagnosis_code': fake.random_element(elements=('E11.9', 'I10', 'J45.909', 'K21.9')),
            'paid_amount': amount
        })
    return pd.DataFrame(claims)

# Generate and save to CSV
def main():
    patient_df = generate_patients(100)
    provider_df = generate_providers(10)
    claims_df = generate_claims(500, patient_df, provider_df)

    patient_df.to_csv('data/patients.csv', index=False)
    provider_df.to_csv('data/providers.csv', index=False)
    claims_df.to_csv('data/claims.csv', index=False)

    print("Data generated and saved to data/ folder.")

if __name__ == "__main__":
    main()
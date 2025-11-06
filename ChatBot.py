





from vanna.ollama import Ollama
from vanna.chromadb import ChromaDB_VectorStore



class MyVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)

vn = MyVanna(config={'model': 'sqlcoder'})



vn.connect_to_sqlite('medical.db')

# vn.train(documentation="""
#  "Generate a synthetic dataset of realistic medical patient records with the following properties:

# 1. **Patient Demographics**:
#    - First name (common Western names)
#    - Last name (common Western surnames)
#    - Date of birth (ages 18-90, normal distribution)
#    - Gender (Male/Female/Other)
#    - Race/Ethnicity (White, Black, Asian, Hispanic, Other)
#    - Address (realistic street addresses)
#    - City/State/Zip (geographically consistent US locations)
#    - Phone (valid US formats: ###-###-####)
#    - Email (name-based patterns)

# 2. **Medical Profile**:
#    - Primary diagnosis (from: [Type 2 Diabetes, Hypertension, Hyperlipidemia, Coronary Artery Disease, Asthma, COPD, Osteoarthritis, Depression, Anxiety Disorder, Hypothyroidism, GERD, Chronic Kidney Disease])
#    - Insurance provider (from: [Medicare, Medicaid, Blue Cross, Aetna, UnitedHealthcare, Cigna, Kaiser Permanente])
#    - BMI (18-40, with 30% >30 for obesity)
#    - Smoking status (Current/Former/Never)
#    - Alcohol use (None/Moderate/Heavy)

# 3. **Clinical Data**:
#    - Visit records (1-5 per patient)
#      - Visit date (last 2 years)
#      - Visit type (Routine, Follow-up, Emergency, Consultation, Procedure)
#      - Diagnosis codes (simplified ICD-10 style: 2 letters + 2 numbers)
#      - Physician name
#      - Clinical notes (1-2 realistic sentences)
   
#    - Lab results (1-3 per visit):
#      - Test type (from: [HbA1c, Glucose, LDL, HDL, Triglycerides, Creatinine, TSH, WBC, Hemoglobin])
#      - Result value (within medically plausible ranges)
#      - Reference range (standard for each test)
#      - Abnormal flag (20% abnormal)
#      - Units (%, mg/dL, mIU/L, etc.)
   
#    - Medications (1-4 per visit):
#      - Drug name (from common formulary)
#      - Dosage (realistic amounts)
#      - Frequency (Daily, BID, TID, QHS, PRN)
#      - Route (PO, IV, SubQ, Inhalation)
#      - Prescription dates
#      - Prescribing physician

# **Data Requirements**:
# - Generate 100 complete patient records
# - Maintain referential integrity (patient→visits→labs/meds)
# - 20% abnormal lab results
# - 15% patients with multiple chronic conditions
# - 10% medication interactions
# - Temporal consistency (meds prescribed after diagnosis)
# - Geographic distribution (urban/rural mix)
# - Insurance type correlated with diagnosis prevalence

# **Format Specifications**:
# - SQLite compatible schema
# - DATE fields as YYYY-MM-DD
# - BOOLEAN as 0/1 integers
# - TEXT fields for all strings
# - Proper NULL handling for optional fields

# **Keywords**: 
# synthetic data, healthcare, HIPAA-compliant, realistic distributions, clinical variability, temporal patterns, comorbidity, polypharmacy, lab abnormalities, demographic diversity, insurance coverage, treatment protocols

# **Special Instructions**:
# 1. Ensure medically plausible correlations:
#    - Higher HbA1c in diabetic patients
#    - Elevated LDL in CAD patients
#    - Antidepressants for depression diagnoses
# 2. Create realistic progressions:
#    - Worsening lab values over time for non-compliant patients
#    - Medication adjustments after abnormal labs
# 3. Include data quirks:
#    - 5% missing values in optional fields
#    - 2% data entry errors (typos in notes)
#    - 1% duplicate records

# Output the complete SQLite database file with all tables populated."
# """)

# vn.train(
#     question='Show all diabetic patients with poorly controlled HbA1c levels (>9%)',
#     sql="""
#     SELECT p.patient_id, p.first_name, p.last_name, 
#            l.test_type, l.result_value, l.reference_range
#     FROM patients p
#     JOIN lab_results l ON p.patient_id = l.patient_id
#     WHERE p.primary_diagnosis LIKE '%Diabetes%'
#       AND l.test_type = 'HbA1c'
#       AND l.result_value > 9.0
#     ORDER BY l.result_value DESC;
#     """
# )

# vn.train(
#     question='Identify patients on dangerous combinations of opioids and benzodiazepines',
#     sql="""
#     SELECT DISTINCT p.patient_id, p.first_name, p.last_name
#     FROM patients p
#     JOIN medications m1 ON p.patient_id = m1.patient_id
#     JOIN medications m2 ON p.patient_id = m2.patient_id
#     WHERE m1.drug_name LIKE '%opioid%'
#       AND m2.drug_name LIKE '%benzodiazepine%'
#       AND (m1.end_date IS NULL OR m1.end_date > CURRENT_DATE)
#       AND (m2.end_date IS NULL OR m2.end_date > CURRENT_DATE);
#     """
# )

# vn.train(
#     question='Find hypertensive patients with uncontrolled blood pressure in the last 3 months',
#     sql="""
#     SELECT p.patient_id, p.first_name, p.last_name,
#            MAX(CASE WHEN l.test_type = 'SBP' THEN l.result_value END) as last_SBP,
#            MAX(CASE WHEN l.test_type = 'DBP' THEN l.result_value END) as last_DBP
#     FROM patients p
#     JOIN lab_results l ON p.patient_id = l.patient_id
#     WHERE p.primary_diagnosis LIKE '%Hypertension%'
#       AND l.test_type IN ('SBP', 'DBP')
#       AND l.result_date >= date('now', '-3 months')
#     GROUP BY p.patient_id
#     HAVING last_SBP >= 140 OR last_DBP >= 90;
#     """
# )

# vn.train(
#     question='List patients who may be non-adherent to medications (no refills in 6 months)',
#     sql="""
#     SELECT p.patient_id, p.first_name, p.last_name, 
#            m.drug_name, MAX(m.end_date) as last_fill_date
#     FROM patients p
#     JOIN medications m ON p.patient_id = m.patient_id
#     WHERE m.drug_name IN ('Atorvastatin', 'Lisinopril', 'Metformin')
#       AND m.end_date < date('now', '-6 months')
#     GROUP BY p.patient_id, m.drug_name;
#     """
# )

# vn.train(
#     question='Find patients overdue for their annual physical exam',
#     sql="""
#     SELECT p.patient_id, p.first_name, p.last_name, 
#            MAX(v.visit_date) as last_physical_date
#     FROM patients p
#     LEFT JOIN visits v ON p.patient_id = v.patient_id 
#       AND v.visit_type = 'Routine'
#     GROUP BY p.patient_id
#     HAVING last_physical_date < date('now', '-1 year') 
#        OR last_physical_date IS NULL;
#     """
# )

# vn.train(
#     question='Identify abnormal lab results that need follow-up visits',
#     sql="""
#     SELECT p.patient_id, p.first_name, p.last_name,
#            l.test_type, l.result_value, l.reference_range,
#            l.result_date, v.physician
#     FROM patients p
#     JOIN lab_results l ON p.patient_id = l.patient_id
#     LEFT JOIN visits v ON l.visit_id = v.visit_id
#     WHERE l.abnormal_flag = 1
#       AND NOT EXISTS (
#         SELECT 1 FROM visits v2 
#         WHERE v2.patient_id = p.patient_id
#           AND v2.visit_date > l.result_date
#           AND v2.visit_type = 'Follow-up'
#       )
#     ORDER BY l.result_date DESC;
#     """
# )

# vn.train(
#     question='Find patients with polypharmacy (5+ active medications)',
#     sql="""
#     SELECT p.patient_id, p.first_name, p.last_name,
#            COUNT(m.medication_id) as active_meds_count
#     FROM patients p
#     JOIN medications m ON p.patient_id = m.patient_id
#     WHERE (m.end_date IS NULL OR m.end_date > CURRENT_DATE)
#     GROUP BY p.patient_id
#     HAVING active_meds_count >= 5
#     ORDER BY active_meds_count DESC;
#     """
# )

# vn.train(
#     question='Identify frequent ER visitors (3+ visits in last 6 months)',
#     sql="""
#     SELECT p.patient_id, p.first_name, p.last_name,
#            COUNT(v.visit_id) as er_visits
#     FROM patients p
#     JOIN visits v ON p.patient_id = v.patient_id
#     WHERE v.visit_type = 'Emergency'
#       AND v.visit_date >= date('now', '-6 months')
#     GROUP BY p.patient_id
#     HAVING er_visits >= 3
#     ORDER BY er_visits DESC;
#     """
# )

# vn.train(
#     question='Find patients using brand-name drugs that have generic alternatives',
#     sql="""
#     SELECT p.patient_id, p.first_name, p.last_name,
#            m.drug_name, m.dosage, m.start_date
#     FROM patients p
#     JOIN medications m ON p.patient_id = m.patient_id
#     WHERE (m.end_date IS NULL OR m.end_date > CURRENT_DATE)
#       AND m.drug_name IN (
#         'Lipitor', 'Zestril', 'Zocor', 'Prozac'
#       );
#     """
# )

# vn.train(
#     question='Identify CAD patients overdue for LDL screening (>2 years)',
#     sql="""
#     SELECT p.patient_id, p.first_name, p.last_name,
#            MAX(l.result_date) as last_ldl_date
#     FROM patients p
#     LEFT JOIN lab_results l ON p.patient_id = l.patient_id
#       AND l.test_type = 'LDL'
#     WHERE p.primary_diagnosis LIKE '%Coronary Artery Disease%'
#     GROUP BY p.patient_id
#     HAVING last_ldl_date < date('now', '-2 years') 
#        OR last_ldl_date IS NULL;
#     """
#)
from vanna.flask import VannaFlaskApp
app = VannaFlaskApp(vn,allow_llm_to_see_data=True)
app.run()







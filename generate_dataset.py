"""
generate_dataset.py
Creates a synthetic legal_stories.csv dataset with REALISTIC legal documents.
Includes case filings, lawyer notes, evidence summaries, email exchanges, etc.
Labels: 0 = Civil, 1 = Criminal
"""

import pandas as pd
import random

# Names for variety
NAMES = [
    "Raj Sharma", "Priya Singh", "Amit Verma", "Kavita Gupta", "Suresh Kumar",
    "Anita Reddy", "Vikram Patel", "Deepa Nair", "Sanjay Mehta", "Sunita Rao",
    "Rahul Khanna", "Meera Iyer", "Anil Kapoor", "Pooja Malhotra", "Manoj Tiwari",
    "Rekha Joshi", "Vijay Saxena", "Neha Agarwal", "Ashok Bansal", "Ritu Sharma",
    "John D'Souza", "Sarah Thomas", "Michael Fernandes", "Emily Brown", "David Wilson",
    "Kiran Desai", "Arjun Nath", "Divya Menon", "Rohit Bhatia", "Swati Pillai"
]

COURTS = [
    "Saket District Court, New Delhi", "Patiala House Courts, New Delhi",
    "Tis Hazari Courts, Delhi", "Karkardooma District Court, Delhi",
    "Mumbai City Civil Court", "Sessions Court Mumbai", "Bangalore City Civil Court",
    "Chennai Metropolitan Magistrate Court", "Kolkata High Court", "Hyderabad District Court"
]

ADDRESSES = [
    "123 Main Street, Central Delhi", "456 Park Avenue, South Delhi",
    "789 Green Road, Dwarka", "234 Lake View, Vasant Kunj",
    "567 Hill Side, Saket", "890 River Lane, Rohini",
    "101 Market Street, Karol Bagh", "202 Garden Path, Lajpat Nagar"
]

# =============================================================================
# CIVIL CASE TEMPLATES (Label = 0)
# =============================================================================

def generate_civil_money_recovery():
    """Generate a money recovery case (Civil)"""
    plaintiff = random.choice(NAMES)
    defendant = random.choice([n for n in NAMES if n != plaintiff])
    amount = random.choice([25000, 50000, 75000, 100000, 150000, 200000, 500000])
    court = random.choice(COURTS)
    case_num = f"CIV-2025-{random.randint(1000, 9999)}"
    
    templates = [
        f"""CASE INFORMATION - CIVIL SUIT

Court: {court}
Case Number: {case_num}
Case Type: Civil Case (Recovery of Money)
Filing Date: {random.choice(['January', 'February', 'March', 'April', 'May'])} {random.randint(1,28)}, 2025

Parties:
Plaintiff: Mr./Ms. {plaintiff}
Defendant: Mr./Ms. {defendant}

Case Summary: The plaintiff, {plaintiff}, has filed a suit for the recovery of ₹{amount:,} from the defendant, {defendant}. The plaintiff alleges that the loan was extended via a written promissory note with a repayment deadline that has passed. The defendant has failed to repay the amount by the stipulated date.

Current Status: Pending - Summons issued to the defendant.""",

        f"""LAWYER NOTES - CONFIDENTIAL

Client: {plaintiff} (Plaintiff)
Matter: Recovery of ₹{amount:,} from {defendant}

Case Strategy:
Primary evidence is the signed promissory note. Very strong documentation.
The witness is reliable and willing to testify about the loan agreement.
Email chain shows {defendant} acknowledging the debt and failure to pay.
Our primary argument is a straightforward breach of contract.

Client Position: Firm on recovering the full amount. Not interested in settlement for a lesser sum at this stage. Feels betrayed as it was a personal loan to a friend.""",

        f"""PROMISSORY NOTE

Loan Amount: ₹{amount:,}

FOR VALUE RECEIVED, the undersigned, {defendant} (the "Borrower"), promises to pay to the order of {plaintiff} (the "Lender") the principal sum of ₹{amount:,}.

TERMS OF REPAYMENT: The full amount is to be repaid within six months from the date of this note. No interest shall be accrued if paid by the due date.

Signature of Borrower: {defendant}

Note: The borrower has not repaid the amount despite multiple reminders. This matter is being taken to civil court for recovery.""",

        f"""EMAIL CORRESPONDENCE - EVIDENCE

From: {plaintiff}
To: {defendant}
Subject: Reminder: Loan Repayment Overdue

Hi {defendant.split()[0]},
Hope you're well. I'm following up on the ₹{amount:,} loan. The due date has passed. Please let me know when I can expect the payment.

---
Reply from {defendant}:
I know, I'm sorry. Things have been difficult financially. Can you give me more time?

---
This constitutes civil matter for recovery of debt. No criminal elements present."""
    ]
    return random.choice(templates)


def generate_civil_property_dispute():
    """Generate a property dispute case (Civil)"""
    plaintiff = random.choice(NAMES)
    defendant = random.choice([n for n in NAMES if n != plaintiff])
    location = random.choice(ADDRESSES)
    court = random.choice(COURTS)
    
    templates = [
        f"""CIVIL SUIT - PROPERTY DISPUTE

Court: {court}
Case Type: Property/Land Dispute

Plaintiff: {plaintiff}
Defendant: {defendant}

Facts of the Case:
The plaintiff owns a residential property at {location}. The defendant, who is the neighbor, has unlawfully constructed a boundary wall that encroaches approximately 3 feet onto the plaintiff's land.

Despite multiple requests for removal of the encroachment, the defendant has refused to comply. The plaintiff seeks a mandatory injunction directing the defendant to demolish the encroaching construction and restore the land.

Relief Sought: Mandatory injunction for removal of encroachment and damages for illegal possession.""",

        f"""LAWYER NOTES - PROPERTY MATTER

Client: {plaintiff}

Issue: Boundary dispute with neighbor {defendant}. Client's property survey shows encroachment of approximately 100 sq. ft. by the defendant's new construction.

Evidence Available:
1. Original sale deed showing clear boundaries
2. Recent survey report by licensed surveyor
3. Photographs showing encroachment
4. Witness statements from other neighbors

Strategy: File civil suit for mandatory injunction. This is purely a civil matter - no criminal trespass as there's a genuine boundary dispute. Seek removal of encroachment plus compensation.""",

        f"""PROPERTY OWNERSHIP DISPUTE

Parties involved: {plaintiff} vs {defendant}

The dispute concerns ancestral property that was divided among family members. {plaintiff} claims that {defendant} has occupied a portion of land that was allocated to the plaintiff in the family settlement deed.

Documents examined:
- Family settlement deed from 2010
- Property registration documents
- Revenue records

Opinion: This is a civil dispute regarding interpretation of family settlement. Recommend filing civil suit for partition and specific performance. No criminal elements involved."""
    ]
    return random.choice(templates)


def generate_civil_contract_breach():
    """Generate a contract breach case (Civil)"""
    plaintiff = random.choice(NAMES)
    defendant = random.choice([n for n in NAMES if n != plaintiff])
    amount = random.choice([100000, 250000, 500000, 750000, 1000000])
    service = random.choice([
        "interior design work", "construction project", "software development",
        "wedding photography", "catering services", "home renovation"
    ])
    
    templates = [
        f"""CIVIL SUIT FOR BREACH OF CONTRACT

Plaintiff: {plaintiff}
Defendant: {defendant}
Amount in Dispute: ₹{amount:,}

Statement of Claim:
The plaintiff entered into a contract with the defendant for {service} on agreed terms. The total contract value was ₹{amount:,}, of which the plaintiff has already paid 60% as advance.

The defendant has failed to complete the work as per the agreed specifications and timeline. Despite multiple reminders, the defendant has neither completed the work nor refunded the advance amount.

The plaintiff seeks recovery of ₹{int(amount*0.6):,} paid as advance, along with damages for mental harassment and legal costs.

This is a civil matter arising from breach of commercial contract.""",

        f"""DEMAND NOTICE - BREACH OF CONTRACT

To: {defendant}

Subject: Legal Notice for Recovery of ₹{amount:,}

This notice is being sent on behalf of my client {plaintiff}.

My client had engaged your services for {service}. A written contract was executed and advance payment of ₹{int(amount*0.6):,} was made.

You have failed to deliver the services as agreed. My client demands:
1. Immediate refund of advance payment
2. Compensation for losses suffered

If we do not receive satisfactory response within 15 days, we shall be constrained to initiate civil proceedings against you. This is a civil dispute - treat this notice seriously."""
    ]
    return random.choice(templates)


def generate_civil_landlord_tenant():
    """Generate landlord-tenant dispute (Civil)"""
    landlord = random.choice(NAMES)
    tenant = random.choice([n for n in NAMES if n != landlord])
    rent = random.choice([15000, 20000, 25000, 30000, 35000, 50000])
    months = random.randint(3, 8)
    
    templates = [
        f"""CIVIL SUIT - EVICTION AND RENT RECOVERY

Plaintiff/Landlord: {landlord}
Defendant/Tenant: {tenant}
Monthly Rent: ₹{rent:,}
Outstanding Rent: ₹{rent * months:,} ({months} months)

Statement of Facts:
The plaintiff is the owner of the residential premises. The defendant has been a tenant since 2023 at a monthly rent of ₹{rent:,}. 

The defendant has defaulted on rent payments for the last {months} months. Multiple verbal and written reminders have been ignored. The defendant has also caused damage to the property.

Relief Sought:
1. Eviction of the defendant from the premises
2. Recovery of outstanding rent of ₹{rent * months:,}
3. Compensation for property damage
4. Future rent until actual eviction

This is a civil landlord-tenant dispute under the Rent Control Act.""",

        f"""LAWYER NOTES - EVICTION MATTER

Client: {landlord} (Landlord)
Opponent: {tenant} (Tenant)

Facts:
- Tenancy since 2023, rent ₹{rent:,}/month
- Non-payment of rent for {months} months = ₹{rent * months:,}
- Tenant not vacating despite notice

Documents:
- Rent agreement (registered)
- Rent receipts showing default
- Legal notice sent (with acknowledgment)

Strategy: File eviction suit in Rent Controller court. This is purely civil in nature. Seek eviction + rent arrears + damages. Estimated timeline: 6-12 months.""",

        f"""TENANT DISPUTE SUMMARY

{tenant} has been occupying the property owned by {landlord} and has failed to pay rent for {months} consecutive months, totaling ₹{rent * months:,}.

The tenant also refuses to vacate the premises despite the lease agreement having expired. This constitutes a civil dispute regarding rental arrears and unlawful occupation.

Recommended action: File civil suit for eviction and recovery. No criminal element as this is a contractual tenancy matter."""
    ]
    return random.choice(templates)


def generate_civil_employment():
    """Generate employment dispute (Civil)"""
    employee = random.choice(NAMES)
    employer = random.choice([
        "ABC Technologies Pvt Ltd", "XYZ Solutions Inc", "Global Services Ltd",
        "Tech Innovations Corp", "Business Systems Pvt Ltd", "Digital Dreams Inc"
    ])
    salary = random.choice([50000, 75000, 100000, 125000, 150000])
    months = random.randint(2, 5)
    
    templates = [
        f"""LABOR DISPUTE - UNPAID WAGES

Petitioner: {employee}
Respondent: {employer}

Claim Details:
The petitioner was employed with the respondent company as a senior professional. The monthly salary was ₹{salary:,}. 

The respondent has failed to pay salary for the last {months} months amounting to ₹{salary * months:,}. Additionally, the respondent has not deposited the PF contributions.

The petitioner was asked to resign without any dues being cleared. This constitutes a civil labor dispute for recovery of unpaid wages and statutory dues.

Relief Sought: Recovery of ₹{salary * months:,} as unpaid salary plus PF dues and interest.""",

        f"""WRONGFUL TERMINATION CASE

Employee: {employee}
Employer: {employer}

The employee was terminated without following due process. No show-cause notice was issued. The termination letter cited "performance issues" but no performance improvement plan was ever discussed.

Outstanding Dues:
- Unpaid salary: ₹{salary * months:,}
- Notice period pay: ₹{salary:,}
- Earned leave encashment: ₹{int(salary * 0.5):,}

This is a civil matter for wrongful termination and recovery of dues. To be filed before the Labor Commissioner."""
    ]
    return random.choice(templates)


def generate_civil_consumer():
    """Generate consumer dispute (Civil)"""
    consumer = random.choice(NAMES)
    company = random.choice([
        "Best Electronics Store", "Quality Home Appliances", "Super Gadgets Ltd",
        "Prime Furniture House", "Metro Auto Dealers", "City Medical Center"
    ])
    product = random.choice([
        "refrigerator", "washing machine", "laptop", "air conditioner",
        "car", "mobile phone", "television"
    ])
    amount = random.choice([25000, 45000, 75000, 150000, 500000])
    
    templates = [
        f"""CONSUMER COMPLAINT

Complainant: {consumer}
Opposite Party: {company}
Product: {product}
Amount: ₹{amount:,}

Complaint:
The complainant purchased a {product} from the opposite party for ₹{amount:,}. Within weeks of purchase, the product developed a major defect. Despite multiple complaints, neither repair nor replacement was provided.

The opposite party's service center has been unresponsive. The warranty claim was rejected citing frivolous reasons.

This is a consumer dispute under the Consumer Protection Act. The complainant seeks replacement of the defective product, compensation for mental agony, and litigation costs.

Prayer: Replacement/refund of ₹{amount:,} plus ₹50,000 as compensation.""",

        f"""DEFICIENCY IN SERVICE - CONSUMER MATTER

Consumer: {consumer}
Service Provider: {company}
Amount Paid: ₹{amount:,}

The consumer availed services from the opposite party but the services rendered were grossly deficient. The opposite party failed to meet the promised standards and specifications.

Multiple complaints were made but no satisfactory resolution was provided. This constitutes deficiency in service under consumer law.

This is a civil consumer dispute. Seeking refund and compensation through Consumer Forum."""
    ]
    return random.choice(templates)


def generate_civil_divorce():
    """Generate matrimonial/family dispute (Civil)"""
    spouse1 = random.choice([n for n in NAMES if any(x in n for x in ['Priya', 'Kavita', 'Anita', 'Deepa', 'Sunita', 'Meera', 'Pooja', 'Rekha', 'Neha', 'Ritu', 'Sarah', 'Emily', 'Divya', 'Swati'])])
    spouse2 = random.choice([n for n in NAMES if n != spouse1 and not any(x in n for x in ['Priya', 'Kavita', 'Anita', 'Deepa', 'Sunita', 'Meera', 'Pooja', 'Rekha', 'Neha', 'Ritu', 'Sarah', 'Emily', 'Divya', 'Swati'])])
    
    templates = [
        f"""MATRIMONIAL DISPUTE - DIVORCE PETITION

Petitioner: {spouse1}
Respondent: {spouse2}

Type: Divorce Petition under Hindu Marriage Act

Facts:
The parties were married in 2019. Due to irreconcilable differences and temperamental incompatibility, the marriage has irretrievably broken down. The parties have been living separately for over two years.

There are disputes regarding:
1. Division of matrimonial property
2. Custody of minor child
3. Maintenance/alimony

This is a civil family matter. The petitioner seeks dissolution of marriage and fair settlement of matrimonial property. Mediation has been attempted but failed.""",

        f"""FAMILY COURT MATTER - MAINTENANCE

Applicant: {spouse1}
Respondent: {spouse2}

Application for interim maintenance under Section 125 CrPC.

The applicant and respondent are legally married. The respondent has deserted the applicant and is not providing any financial support. The applicant has no independent source of income.

Prayer: Monthly maintenance of ₹50,000 pending divorce proceedings.

Note: This is a civil matrimonial dispute regarding maintenance and not a criminal matter."""
    ]
    return random.choice(templates)


# =============================================================================
# CRIMINAL CASE TEMPLATES (Label = 1)
# =============================================================================

def generate_criminal_assault():
    """Generate assault/violence case (Criminal)"""
    accused = random.choice(NAMES)
    victim = random.choice([n for n in NAMES if n != accused])
    location = random.choice(ADDRESSES)
    
    templates = [
        f"""FIR - FIRST INFORMATION REPORT

Police Station: Central Police Station
FIR Number: {random.randint(100, 999)}/2025
Sections: 323, 324, 506 IPC (Assault, Causing Hurt, Criminal Intimidation)

Complainant: {victim}
Accused: {accused}

Statement:
On the evening of {random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])}, at approximately 8 PM, the accused {accused} attacked me near {location}. 

The accused attacked me with a wooden stick causing injuries to my head and arms. He also threatened to kill me if I report to the police. I sustained bleeding injuries and was taken to the hospital.

This is a criminal case of assault and criminal intimidation. The accused should be arrested and prosecuted.""",

        f"""CHARGE SHEET - CRIMINAL CASE

Accused: {accused}
Victim: {victim}
Sections: 325, 506 IPC (Grievous Hurt, Criminal Intimidation)

Investigation Summary:
Based on the FIR and investigation, it is established that the accused {accused} brutally assaulted the victim {victim} with an iron rod, causing multiple fractures.

Evidence Collected:
1. Medical report confirming grievous injuries
2. Weapon recovered (iron rod with blood stains)
3. Eyewitness statements from two persons
4. CCTV footage from nearby shop

Conclusion: Prima facie criminal case established. Recommend prosecution of accused for grievous hurt under IPC.""",

        f"""CRIMINAL COMPLAINT - ASSAULT

Complainant/Victim: {victim}
Accused Person: {accused}

Details of Crime:
The accused {accused} physically assaulted the complainant {victim} with a sharp weapon inflicting serious injuries. The attack was premeditated and the accused had been making threats for several weeks.

Injuries Sustained:
- Deep cut on the left arm requiring 15 stitches
- Bruises on face and chest
- Psychological trauma

This is a serious criminal offense of assault causing grievous bodily harm. Request immediate arrest of the accused and criminal prosecution."""
    ]
    return random.choice(templates)


def generate_criminal_theft():
    """Generate theft/robbery case (Criminal)"""
    accused = random.choice(NAMES)
    victim = random.choice([n for n in NAMES if n != accused])
    items = random.choice([
        "gold jewelry worth ₹5,00,000", "cash amounting to ₹2,00,000",
        "laptop and mobile phones worth ₹1,50,000", "vehicle (car) worth ₹8,00,000",
        "diamond necklace worth ₹10,00,000"
    ])
    
    templates = [
        f"""FIR - THEFT/ROBBERY

Police Station: City Police Station
FIR Number: {random.randint(100, 999)}/2025
Sections: 379, 380 IPC (Theft, Theft in dwelling house)

Complainant: {victim}
Accused: {accused} (identified)

Incident:
On the night of the incident, unknown persons broke into my residence while I was away. Upon returning, I found the lock broken and the house ransacked.

Items Stolen:
{items}

During investigation, the accused {accused} was identified based on CCTV footage. This is a criminal case of theft/burglary. Request immediate action and recovery of stolen property.""",

        f"""INVESTIGATION REPORT - ROBBERY CASE

Case: Robbery at residence of {victim}
Accused: {accused}
Sections: 392, 397 IPC (Robbery, Dacoity with attempt to cause death)

Investigation Findings:
The accused {accused} along with two others broke into the victim's house while the family was asleep. They threatened the family members with weapons and robbed {items}.

Evidence:
- Victim's statement recorded
- Stolen items recovered from accused's possession
- Weapons recovered
- Confession statement of accused

This is a criminal case of robbery. The accused has been arrested. Charge sheet being filed for trial.""",

        f"""CRIMINAL CASE - HOUSE BREAKING AND THEFT

Victim: {victim}
Accused: {accused}

The accused {accused} criminally trespassed into the locked house of the victim at night and committed theft of valuable items including {items}.

This constitutes criminal offenses under IPC Sections 454 (House trespass), 457 (Lurking house-trespass by night), and 380 (Theft in dwelling house).

The accused has previous criminal history. Request stringent action. This is a serious criminal matter, not a civil dispute."""
    ]
    return random.choice(templates)


def generate_criminal_fraud():
    """Generate fraud/cheating case (Criminal)"""
    accused = random.choice(NAMES)
    victim = random.choice([n for n in NAMES if n != accused])
    amount = random.choice([500000, 1000000, 2500000, 5000000, 10000000])
    scheme = random.choice([
        "fake investment scheme promising 50% returns",
        "fraudulent property sale with forged documents",
        "ponzi scheme disguised as trading platform",
        "fake job placement agency collecting registration fees",
        "fraudulent loan approval scheme"
    ])
    
    templates = [
        f"""FIR - CRIMINAL FRAUD AND CHEATING

Sections: 420, 406, 468, 471 IPC (Cheating, Criminal Breach of Trust, Forgery)

Complainant: {victim}
Accused: {accused}

Criminal Complaint:
The accused {accused} cheated me of ₹{amount:,} through a {scheme}. The accused made false promises and representations to induce me to invest/pay money.

After receiving the money, the accused absconded. Upon investigation, I found that the entire scheme was fraudulent and the documents provided by the accused were forged.

This is a clear case of criminal fraud and cheating. The accused has deliberately deceived me with dishonest intention. Request registration of FIR and arrest of the accused.""",

        f"""CYBER CRIME COMPLAINT - ONLINE FRAUD

Sections: 420 IPC, Section 66D IT Act

Victim: {victim}
Accused/Suspect: {accused}
Amount Defrauded: ₹{amount:,}

Details of Cyber Fraud:
The accused operated a {scheme}. The victim was contacted through social media and convinced to transfer money with promises of high returns.

Multiple transactions were made to the accused's bank account. After collecting ₹{amount:,}, the accused blocked all communication and disappeared.

Evidence: Bank statements, WhatsApp chats, Email correspondence

This is a criminal case of cyber fraud under IPC and IT Act. Request urgent action.""",

        f"""CRIMINAL INVESTIGATION - FINANCIAL FRAUD

Accused: {accused}
Victims: {victim} and others
Total Amount: ₹{amount:,}+

Investigation established that the accused ran a {scheme}, collecting money from multiple victims with false promises. 

The accused used fake identity documents and opened bank accounts for laundering the defrauded money. This is a case of organized financial crime.

Sections: 420 (Cheating), 406 (Criminal breach of trust), 34 (Common intention) IPC

The accused is a habitual offender. Criminal prosecution recommended."""
    ]
    return random.choice(templates)


def generate_criminal_murder():
    """Generate murder/attempt to murder case (Criminal)"""
    accused = random.choice(NAMES)
    victim = random.choice([n for n in NAMES if n != accused])
    
    templates = [
        f"""FIR - MURDER CASE

Police Station: Crime Branch
FIR Number: {random.randint(100, 999)}/2025
Sections: 302, 201 IPC (Murder, Causing disappearance of evidence)

Deceased: {victim}
Accused: {accused}

Case Summary:
The body of {victim} was found at the outskirts of the city. Post-mortem report confirms death due to stab wounds and strangulation. The victim was last seen with the accused {accused}.

Investigation reveals the accused had ongoing disputes with the deceased over financial matters. Mobile records and witnesses place the accused at the crime scene.

This is a case of premeditated murder. The accused {accused} has been arrested. Charge sheet being prepared for trial in Sessions Court.""",

        f"""CHARGE SHEET - ATTEMPT TO MURDER

Sections: 307, 324 IPC (Attempt to Murder, Voluntarily causing hurt by dangerous weapon)

Accused: {accused}
Victim: {victim}

Facts:
The accused {accused} made a deliberate attempt on the life of {victim} by attacking with a knife. The victim sustained life-threatening injuries and was hospitalized for weeks.

Evidence:
- Medical report confirming injuries could have been fatal
- Murder weapon recovered
- Eyewitness testimony
- Motive established (property dispute)

This constitutes attempted murder under Section 307 IPC. The accused acted with clear intention to kill. Trial in Sessions Court recommended.""",

        f"""CRIMINAL CASE - HOMICIDE

Case Type: Murder (Section 302 IPC)
Accused: {accused}
Victim/Deceased: {victim}

The accused {accused} has been charged with the murder of {victim}. Investigation reveals the accused poisoned the victim's food over several days, leading to death.

Forensic Evidence:
- Poison traces found in victim's body
- Purchase records linking accused to poison
- Life insurance policy naming accused as beneficiary

This is a case of planned criminal homicide for financial gain. The accused should be prosecuted for murder."""
    ]
    return random.choice(templates)


def generate_criminal_kidnapping():
    """Generate kidnapping/abduction case (Criminal)"""
    accused = random.choice(NAMES)
    victim = random.choice([n for n in NAMES if n != accused])
    ransom = random.choice([1000000, 2500000, 5000000, 10000000])
    
    templates = [
        f"""FIR - KIDNAPPING FOR RANSOM

Sections: 364A, 365 IPC (Kidnapping for ransom, Abduction)

Complainant: Family of {victim}
Accused: {accused} and unknown others
Victim: {victim}

Complaint:
{victim} was abducted by armed men while returning home from office. The family received a ransom call demanding ₹{ransom:,} for the victim's release.

The callers threatened to kill {victim} if police is informed. The voice in the ransom call was identified as that of {accused}, who had previous enmity with the victim's family.

This is a serious criminal case of kidnapping for ransom. Request immediate action to rescue the victim and arrest the perpetrators.""",

        f"""INVESTIGATION REPORT - ABDUCTION CASE

Case: Kidnapping of {victim}
Prime Accused: {accused}
Sections: 364, 368 IPC (Kidnapping, Wrongfully concealing abducted person)

Investigation Summary:
The victim {victim} was kidnapped from outside their residence. The accused {accused} was part of the kidnapping gang that held the victim captive for 5 days.

Ransom of ₹{ransom:,} was demanded. Through technical surveillance, the hideout was located and the victim was rescued. The accused was arrested from the spot.

This is a criminal case of kidnapping and wrongful confinement. Charge sheet prepared for trial."""
    ]
    return random.choice(templates)


def generate_criminal_drugs():
    """Generate drug offense case (Criminal)"""
    accused = random.choice(NAMES)
    drug = random.choice(["cocaine", "heroin", "MDMA", "methamphetamine", "cannabis/ganja"])
    quantity = random.choice(["500 grams", "2 kilograms", "5 kilograms", "100 grams", "10 kilograms"])
    
    templates = [
        f"""FIR - NDPS ACT VIOLATION

Sections: 21, 22, 29 NDPS Act (Possession, Sale, Conspiracy)

Accused: {accused}
Substance: {drug}
Quantity: {quantity}

Case Details:
Acting on intelligence input, a raid was conducted at the residence of the accused {accused}. During search, {quantity} of {drug} was recovered along with packaging material and weighing scales.

The accused was caught red-handed in possession of commercial quantity of contraband. Mobile records reveal the accused was involved in drug distribution network.

This is a serious criminal offense under the NDPS Act. The accused has been arrested and produced before the Special Court.""",

        f"""CHARGE SHEET - DRUG TRAFFICKING

Accused: {accused}
Sections: 21(c), 29 NDPS Act (Commercial quantity, Conspiracy)

Investigation established that the accused {accused} was running a drug trafficking operation. {quantity} of {drug} was seized from the accused.

Evidence:
- Contraband recovered and sealed
- Chemical analysis report confirming substance
- Financial trail showing drug money
- Statements of buyers identifying accused

This is a criminal case involving commercial quantity narcotic substances. Recommend prosecution in Special NDPS Court."""
    ]
    return random.choice(templates)


def generate_criminal_domestic_violence():
    """Generate domestic violence case (Criminal)"""
    victim = random.choice([n for n in NAMES if any(x in n for x in ['Priya', 'Kavita', 'Anita', 'Deepa', 'Sunita', 'Meera', 'Pooja', 'Rekha', 'Neha', 'Ritu', 'Sarah', 'Emily', 'Divya', 'Swati'])])
    accused = random.choice([n for n in NAMES if n != victim])
    
    templates = [
        f"""FIR - DOMESTIC VIOLENCE

Sections: 498A, 323, 506 IPC (Cruelty, Assault, Criminal Intimidation)
Protection of Women from Domestic Violence Act

Complainant: {victim}
Accused: {accused} (Husband)

Complaint:
The complainant {victim} has been subjected to continuous physical and mental torture by husband {accused}. The accused regularly beats the complainant, often under the influence of alcohol.

Injuries: Multiple bruises, burn marks on arms, psychological trauma

The accused demands additional dowry and threatens to kill if family doesn't pay. This has been ongoing for the past two years. The complainant fears for her life.

This is a criminal case of domestic violence and marital cruelty. Request arrest of accused and protection for complainant.""",

        f"""DOMESTIC VIOLENCE CASE - INVESTIGATION REPORT

Victim: {victim}
Accused: {accused}
Sections: 498A IPC, DV Act Sections 3, 12, 18

Investigation Findings:
Medical examination confirms multiple old and new injury marks on the victim consistent with physical abuse. Neighbors confirmed hearing sounds of beating from the house regularly.

The accused has been habitually cruel to the victim demanding dowry. Text messages threatening dire consequences recovered from accused's phone.

This is a criminal domestic violence case. Accused arrested. Protection order issued for victim. Criminal trial to proceed."""
    ]
    return random.choice(templates)


def generate_criminal_threat():
    """Generate criminal threat/extortion case (Criminal)"""
    accused = random.choice(NAMES)
    victim = random.choice([n for n in NAMES if n != accused])
    amount = random.choice([500000, 1000000, 2000000])
    
    templates = [
        f"""FIR - CRIMINAL INTIMIDATION AND EXTORTION

Sections: 384, 506, 507 IPC (Extortion, Criminal Intimidation, Anonymous Threats)

Complainant: {victim}
Accused: {accused}

Complaint:
The accused {accused} has been threatening me and my family, demanding ₹{amount:,}. The accused has sent threatening messages saying he will kill my children if I don't pay.

The accused is known to have criminal connections. I am under constant fear. The accused has also threatened to destroy my business if I approach the police.

Threat messages and call recordings are available as evidence. This is a criminal case of extortion and criminal intimidation. Request urgent action and protection for my family.""",

        f"""CRIMINAL EXTORTION CASE

Accused: {accused}
Victim: {victim}
Sections: 384, 385 IPC (Extortion, Attempt to Extort)

The accused {accused} has been running an extortion racket. Multiple victims including {victim} have been threatened and forced to pay money.

Evidence:
- Recorded threatening phone calls
- WhatsApp messages with death threats
- Bank transfers under duress
- Multiple victim statements

This is organized criminal extortion. The accused has prior criminal records. Recommend arrest and prosecution."""
    ]
    return random.choice(templates)


def generate_criminal_sexual_offense():
    """Generate sexual harassment/offense case (Criminal)"""
    victim = random.choice([n for n in NAMES if any(x in n for x in ['Priya', 'Kavita', 'Anita', 'Deepa', 'Sunita', 'Meera', 'Pooja', 'Rekha', 'Neha', 'Ritu', 'Sarah', 'Emily', 'Divya', 'Swati'])])
    accused = random.choice([n for n in NAMES if n != victim])
    location = random.choice(["workplace", "public transport", "office premises", "college campus"])
    
    templates = [
        f"""FIR - SEXUAL HARASSMENT

Sections: 354, 354A, 509 IPC (Assault/Criminal force with intent to outrage modesty, Sexual Harassment)

Complainant: {victim}
Accused: {accused}
Location: {location}

Complaint:
The accused {accused} has been sexually harassing me at {location}. The harassment includes inappropriate touching, obscene remarks, and unwanted advances.

Despite clear rejection, the accused continued the harassment. The accused also threatened consequences if I reported the matter.

Statement of a witness has been recorded. This is a criminal case of sexual harassment under IPC. Request arrest of accused and appropriate protection measures.""",

        f"""POSH COMMITTEE TO POLICE COMPLAINT

Complaint Transfer: Internal Committee to Police Station
Sections: 354A IPC (Sexual Harassment)

Accused Employee: {accused}
Victim: {victim}

The Internal Complaints Committee (ICC) investigated allegations of sexual harassment at {location}. The Committee found prima facie case of severe sexual harassment warranting criminal action.

Evidence examined:
- Email and message evidence
- Testimony of complainant and witnesses
- CCTV footage

This criminal matter is being forwarded to police for FIR registration and prosecution under appropriate IPC sections."""
    ]
    return random.choice(templates)


def generate_criminal_forgery():
    """Generate forgery/document fraud case (Criminal)"""
    accused = random.choice(NAMES)
    victim = random.choice([n for n in NAMES if n != accused])
    document_type = random.choice([
        "property registration documents",
        "educational certificates",
        "power of attorney",
        "bank documents/cheques",
        "company shares transfer deed"
    ])
    
    templates = [
        f"""FIR - FORGERY AND FRAUD

Sections: 465, 467, 468, 471 IPC (Forgery, Forgery of valuable security, Using forged document as genuine)

Complainant: {victim}
Accused: {accused}

Criminal Complaint:
The accused {accused} has forged {document_type} pretending to be me/act on my behalf. Using these forged documents, the accused fraudulently transferred property/funds.

The signature on the documents is not mine - this can be verified through handwriting analysis. The accused took advantage of my absence from the country to commit this fraud.

This is a case of criminal forgery and fraud. The accused should be arrested and the fraudulent transactions reversed.""",

        f"""INVESTIGATION REPORT - DOCUMENT FORGERY

Accused: {accused}
Victim: {victim}
Sections: 467, 468, 471, 420 IPC

Investigation Findings:
The accused {accused} created forged {document_type} to illegally transfer assets belonging to {victim}. Forensic examination of documents confirms:

1. Signature is forged - expert opinion obtained
2. Documents printed on backdated stamp paper
3. Witnesses listed are fictitious

The accused has committed criminal forgery for financial gain. Evidence is conclusive. Recommend arrest and prosecution in criminal court."""
    ]
    return random.choice(templates)


# =============================================================================
# DATASET GENERATION
# =============================================================================

# All civil generators
CIVIL_GENERATORS = [
    generate_civil_money_recovery,
    generate_civil_property_dispute,
    generate_civil_contract_breach,
    generate_civil_landlord_tenant,
    generate_civil_employment,
    generate_civil_consumer,
    generate_civil_divorce,
]

# All criminal generators
CRIMINAL_GENERATORS = [
    generate_criminal_assault,
    generate_criminal_theft,
    generate_criminal_fraud,
    generate_criminal_murder,
    generate_criminal_kidnapping,
    generate_criminal_drugs,
    generate_criminal_domestic_violence,
    generate_criminal_threat,
    generate_criminal_sexual_offense,
    generate_criminal_forgery,
]


def generate_dataset(target_size: int = 600, output_file: str = "legal_stories.csv") -> pd.DataFrame:
    """
    Generate a balanced dataset of legal documents.
    
    Args:
        target_size: Approximate number of examples to generate
        output_file: Name of the output CSV file
    
    Returns:
        DataFrame with the generated dataset
    """
    examples = []
    per_class = target_size // 2
    
    # Generate civil examples
    print("Generating CIVIL case documents...")
    for i in range(per_class):
        generator = random.choice(CIVIL_GENERATORS)
        text = generator()
        examples.append({"text": text, "label": 0})
        if (i + 1) % 50 == 0:
            print(f"  Generated {i + 1}/{per_class} civil cases")
    
    # Generate criminal examples
    print("\nGenerating CRIMINAL case documents...")
    for i in range(per_class):
        generator = random.choice(CRIMINAL_GENERATORS)
        text = generator()
        examples.append({"text": text, "label": 1})
        if (i + 1) % 50 == 0:
            print(f"  Generated {i + 1}/{per_class} criminal cases")
    
    # Shuffle the dataset
    random.shuffle(examples)
    
    # Create DataFrame
    df = pd.DataFrame(examples)
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    
    # Print statistics
    print(f"\n{'='*60}")
    print(f"Dataset Generated Successfully!")
    print(f"{'='*60}")
    print(f"Total examples: {len(df)}")
    print(f"  Criminal (label=1): {len(df[df['label'] == 1])}")
    print(f"  Civil (label=0): {len(df[df['label'] == 0])}")
    print(f"Saved to: {output_file}")
    
    # Show document type distribution
    print(f"\n{'='*60}")
    print("Sample Documents:")
    print(f"{'='*60}")
    
    print("\n--- SAMPLE CIVIL CASE ---")
    sample_civil = df[df['label'] == 0].iloc[0]['text']
    print(sample_civil[:500] + "..." if len(sample_civil) > 500 else sample_civil)
    
    print("\n--- SAMPLE CRIMINAL CASE ---")
    sample_criminal = df[df['label'] == 1].iloc[0]['text']
    print(sample_criminal[:500] + "..." if len(sample_criminal) > 500 else sample_criminal)
    
    return df


if __name__ == "__main__":
    # Set seed for reproducibility
    random.seed(42)
    
    # Generate the dataset
    df = generate_dataset(target_size=600, output_file="legal_stories.csv")

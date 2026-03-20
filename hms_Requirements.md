
# Hospital Management System – Requirements Document

---

## 1. Messaging & Notification System

### 1.1 Referral → Admission Flow

When a patient is referred and admitted into the hospital, the system must trigger notifications to all relevant stakeholders.

Patient Notification
- Confirmation of admission  
- Must include date and time  
- Example:  
  “You have been successfully admitted to [Hospital Name] on [Date] at [Time].”

Doctor Notification
- Sent to the assigned doctor  
- Includes:
  - Patient details  
  - Referral source  
- Purpose: Ensure the doctor is aware that the patient is under their care  

Referrer Notification (Doctor / External Person)
- Acknowledgment message  
- Example:  
  “Thank you for referring a patient to us. We appreciate your trust.”  
- Objective:
  - Maintain strong relationships  
  - Encourage future referrals  

Managing Person (Internal Monitoring Role)
- Receives notifications for:
  - Referral creation  
  - Patient admission  
  - Doctor assignment  
- Purpose:
  - Monitor workflow in real-time  
- Example:  
  “A referred patient has been admitted and assigned to a doctor. Process is in progress.”

---

### 1.2 Discharge & Follow-Up Messaging

- Upon discharge:
  - For instance -- A Patient is automatically assigned a 15-day follow-up consultation  

Reminder System (1 Day Before Appointment)

Patient Notification
- Example:  
  “Reminder: You have a follow-up appointment tomorrow for your post-operation check-up.”

Doctor Notification
- Includes:
  - Patient details  
  - Appointment schedule  
  - Visit type (post-op / OPD)

---

### 1.3 OPD & IPD Messaging
- Messaging applies to:
  - OPD (Outpatient Department)  
  - IPD (Inpatient Department) – Primary focus  

---

## 2. Prescription Templates (Reusable System)

### 2.1 Purpose
- Reduce repetitive prescription entry  
- Improve consultation efficiency  

### 2.2 Functionality
- Doctors can create predefined templates for common diseases  
- Example:
  - Disease: Fever  
  - Prescription: Dolo 650 mg  

- During consultation:
  - Doctor searches template  
  - Selects and applies it  
  - Modifies if needed  
  - Saves to patient record  

### 2.3 Requirements
- Templates must be:
  - Reusable  
  - Editable  
  - Searchable  

- Must support:
  - Multiple medicines  
  - Dosage instructions  
  - Duration  

---

## 3. Billing System Requirements

### 3.1 Editing Rules
- Editing allowed only for:
  - Amount fields  

- Applies to all sections except:
  - Pharmacy (non-editable)  

- After payment:
  - Bill is locked  
  - No further edits allowed  

---

### 3.2 Automatic Calculations
- All billing totals must be auto-calculated  
- Manual calculation should not be required  

Includes:
- Room charges  
- Doctor fees  
- Lab tests  
- Procedures  
- Pharmacy  
- Admission fees  

---

### 3.3 Bill Structure

Page 1: Summary Bill
- Table format  
- Includes:
  - Admission fee  
  - Advance payment  
  - Room charges  
  - Operation charges  
  - Pharmacy charges  
  - Lab charges  
  - Other services  

Purpose: Quick overview of total charges  

---

Page 2 onwards: Detailed Breakdown
- Separate sections for:
  - Room Bill  
  - Pharmacy Bill  
  - Lab Test Bill  
  - Procedure / Operation Charges  
  - Additional services  

- Continues until all billing components are covered  

---

## 4. Room & Bed Management

### Room Types
- ICU  
- Special Single A/C  
- Special Single Non-A/C  
- Deluxe Room  
- Day Care  
- Emergency  

### Requirements
- Bed availability must be dynamic (real-time)  

- Pricing:
  - Controlled by Admin  
  - Editable across system  

---

## 5. Referral & Advisory System

- Maintain:
  - Referral records  
  - Referral count list  

- Advisory:
  - For doctor recommendations  

- WhatsApp Integration:
  - Communication between:
    - Doctor  
    - Patient  
    - Referrer  

---

## 6. Organisation / Department

### Medical Departments
- Neuro Surgery  
- General Surgery (Laser & LAP)  
- Obstetrics & Gynaecology  
- Emergency Medicine  
- Orthopedics  
- Endocrinology  
- Pulmonology  
- Neurology  
- Nephrology  
- Cardiology  
- ENT  
- Physiotherapy  
- OT (Operation Theatre)  
- Ward Staff or Ward boy and others

### Support Departments 
        -- are nothing but additional department that are to be added in the departments section

- Pharmacy  
- Nursing  
- Reception  
- Lab  
- Marketing  
- Office  
- Housekeeping  

---

## 7. Employee Registry

- During employee registration:
  - Remove Specialty field (not required)  
  - Remove Salary field (not required)  

---

## 8. Additional Considerations

- System contains multiple mandatory fields  
- This may make appointment booking:
  - Complex  
  - Time-consuming  

- Requires careful UI/UX design to ensure ease of use  

---

## 9. Summary

The system is designed to achieve:

- Strong communication between patient, doctor, referrer, and management  
- Real-time process visibility through notifications  
- Efficient prescription handling using reusable templates  
- Automated and transparent billing system  
- Structured hospital operations  
- A referral-driven engagement model  

---
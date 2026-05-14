BAD_STATUS=['Charged Off',
            'Default',
            'Does not meet the credit policy. Status:Charged Off',
            'Late (31-120 days)'
                   ]
TARGET_COL='good_bad'

purpose_grp_dict = {
   # HIGH RISK
    'small_business': 'high_risk',
    'educational': 'high_risk',
    'moving': 'high_risk',
    'renewable_energy': 'high_risk',
    'house': 'high_risk',
    'medical': 'high_risk',
    'other': 'high_risk',

    # MEDIUM RISK
    'vacation': 'medium_risk',
    'wedding': 'medium_risk',
    'debt_consolidation': 'medium_risk',

    # LOW RISK
    'home_improvement': 'low_risk',
    'major_purchase': 'low_risk',
    'car': 'low_risk',
    'credit_card': 'low_risk'

    }

addr_state_grp_dict={
    'NE': 'OTHER',
    'IA': 'OTHER',
    'ID': 'OTHER',
    'NV': 'HIGH_RISK',
    'FL': 'HIGH_RISK',
    'HI': 'HIGH_RISK',
    'AL': 'HIGH_RISK',
    'LA': 'HIGH_RISK',
    'OK': 'HIGH_RISK',
    'NY': 'HIGH_RISK',
    'NM': 'HIGH_RISK',
    'NC': 'HIGH_RISK',
    'MD': 'HIGH_RISK',
    'CA': 'MEDIUM_RISK',
    'MO': 'MEDIUM_RISK',
    'VA': 'MEDIUM_RISK',
    'AZ': 'MEDIUM_RISK',
    'TN': 'MEDIUM_RISK',
    'NJ': 'MEDIUM_RISK',
    'RI': 'MEDIUM_RISK',
    'UT': 'MEDIUM_RISK',
    'MI': 'MEDIUM_RISK',
    'PA': 'MEDIUM_RISK',
    'AR': 'MEDIUM_RISK',
    'DE': 'MEDIUM_RISK',
    'OH': 'MEDIUM_RISK',
    'KY': 'MEDIUM_RISK',
    'IN': 'MEDIUM_RISK',
    'MN': 'MEDIUM_RISK',
    'MA': 'MEDIUM_RISK',
    'SD': 'OTHER',
    'WA': 'MEDIUM_RISK',
    'GA': 'MEDIUM_RISK',
    'OR': 'MEDIUM_RISK',
    'WI': 'MEDIUM_RISK',
    'ME': 'OTHER',
    'TX': 'LOW_RISK',
    'IL': 'LOW_RISK',
    'SC': 'LOW_RISK',
    'CO': 'LOW_RISK',
    'MT': 'LOW_RISK',
    'CT': 'LOW_RISK',
    'AK': 'OTHER',
    'KS': 'LOW_RISK',
    'VT': 'OTHER',
    'MS': 'OTHER',
    'NH': 'LOW_RISK',
    'WV': 'LOW_RISK',
    'DC': 'LOW_RISK',
    'WY': 'OTHER'
    }

home_ownership_grp_dict = {
    'RENT': 'RENT',
    'OWN': 'OWN',
    'MORTGAGE': 'MORTGAGE',
    'ANY': 'OTHER',
    'NONE': 'OTHER',
    'OTHER': 'OTHER'}

DISCRETE_VARS = [
     'grade',
    'home_ownership',
    'addr_state',
    'verification_status',
    'purpose',
    'initial_list_status'
    ]

CONTINUOUS_VARS = [
    'term_int',
    'emp_length_int',
    'credit_age_months',
    'int_rate',
    'funded_amnt',
    'delinq_2yrs',
    'inq_last_6mths',
    'open_acc',
    'pub_rec',
    'total_acc',
    'acc_now_delinq',
    'total_rev_hi_lim',
    'installment',
    'annual_inc',
    'mths_since_last_delinq',
    'dti',
    'mths_since_last_record'
]

BIN_RULES = {
    'int_rate': [0, 10, 13, 16, 20, 30],
    'dti': [0,7,12,17,24,40,100],
    'annual_inc': [0, 55000, 80000, 120000, 200000],
    'installment': [0, 250, 450, 700, 1500],
    'delinq_2yrs': [-1,0, 3,50],
    'inq_last_6mths': [-1,0,1,3,35],
    'credit_age_months': [0, 125, 160, 200, 260, 320, 900],
    'open_acc':[0, 5, 10, 15, 25, 85],
    'total_acc':[0,10, 20, 30,45, 160]
}
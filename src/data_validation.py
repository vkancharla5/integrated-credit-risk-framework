def validate_input(df):
    required_columns = ['emp_length','term','loan_status','earliest_cr_line','issue_d']

    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")

    return True
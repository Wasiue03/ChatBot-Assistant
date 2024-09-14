import pandas as pd

data = {
    'Student': ['Alice', 'Bob', 'Charlie'],
    'English': [85, 78, 92],
    'Math': [90, 88, 95],
    'Science': [78, 82, 85]
}

df = pd.DataFrame(data)

df['Average'] = df[['English', 'Math', 'Science']].mean(axis=1)

def subject_analysis(row):
    max_subject = row[['English', 'Math', 'Science']].idxmax()
    min_subject = row[['English', 'Math', 'Science']].idxmin()
    return max_subject, min_subject

df['Strength'], df['Weakness'] = zip(*df.apply(subject_analysis, axis=1))

def generate_report(row):
    report = f"Student {row['Student']} has an average score of {row['Average']:.2f}.\n"
    report += f"They performed best in {row['Strength']} with a score of {row[row['Strength']]}, "
    report += f"and need to improve in {row['Weakness']} where they scored {row[row['Weakness']]}. "
    if row['Average'] > 90:
        report += "Overall, they did an excellent job!"
    elif row['Average'] > 75:
        report += "Overall, they did well, but there's room for improvement."
    else:
        report += "They need to work harder to improve their scores."
    
    return report

df['Report'] = df.apply(generate_report, axis=1)

for index, row in df.iterrows():
    print(row['Report'])
    print("\n" + "="*50 + "\n")


df['Report'].to_csv('student_reports.csv', index=False)



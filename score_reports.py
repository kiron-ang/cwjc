score_report = open('data/0.pdf', 'r', encoding='utf-8', errors='ignore')
score_report_lines = score_report.readlines()
for line in score_report_lines:
  if "Study" in line:
    print(line)
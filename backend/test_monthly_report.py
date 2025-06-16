from tasks.monthly_report import send_monthly_reports
send_monthly_reports.delay()
print("📨 Monthly report task triggered.")

#Config files containing the URL and directory

DOMAIN_NAME = "https://uibank.uipath.com"

URL = {
    "register": DOMAIN_NAME + "/register-account",
    "login": DOMAIN_NAME + "/login",
    "status": DOMAIN_NAME + "/loans/lookup",
    "forgot_password": DOMAIN_NAME + "/password-request",
    "main": DOMAIN_NAME + "/accounts",
    "transfer_money": DOMAIN_NAME + "/transfer-money",
    "transfer_result": DOMAIN_NAME + "/transfer-result",
}

allure_results_path = "allure-results"
csv_reports_path = "csv-reports"
excel_report_path = "excel-report"

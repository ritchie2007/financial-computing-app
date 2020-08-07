# sin,prefix,last_name,first_name,middle_name,other_name,phone1,phone2,
# address1,address2,mail_address,wechat,
# cra_sole_proprietor,cra_hst_report,cra_payroll,cra_withhold_tax,cra_wsib,cra_other,
# oversea_asset_t1135,
# oversea_corp_t1134,tslip,tax_personal_info,specific_info,engage_account,engage_leading,note,
# contact_corp,director_corp,sharehold_corp,spouse,parent,child,timemark

filters = ['','','']

if filters[0] != '' and filters[1] == '' and filters[2] == '':
    list_data = CorporationReport.query.filter(CorporationReport.periodend >= filters[0]).all()
elif filters[0] != '' and filters[1] != '' and filters[2] == '':
    list_data = CorporationReport.query.filter(CorporationReport.periodend >= filters[0], CorporationReport.periodend <= filters[1]).all()
elif filters[0] != '' and filters[1] == '' and filters[2] != '':
    list_data = CorporationReport.query.filter(CorporationReport.periodend >= filters[0], CorporationReport.corp == filters[2]).all()
elif filters[0] != '' and filters[1] != '' and filters[2] != '':
    list_data = CorporationReport.query.filter(CorporationReport.periodend >= filters[0], CorporationReport.periodend <= filters[1], CorporationReport.corp == filters[2]).all()
elif filters[0] == '' and filters[1] != '' and filters[2] == '':
    list_data = CorporationReport.query.filter(CorporationReport.periodend <= filters[1]).all()
elif filters[0] == '' and filters[1] != '' and filters[2] != '':
    list_data = CorporationReport.query.filter(CorporationReport.periodend <= filters[1], CorporationReport.corp == filters[2]).all()
elif filters[0] == '' and filters[1] == '' and filters[2] != '':
    list_data = CorporationReport.query.filter(CorporationReport.corp == filters[2]).all()
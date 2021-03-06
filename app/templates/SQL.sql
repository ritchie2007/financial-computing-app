--create table staff_daily_sum (id integer primary key, name varchar(80), date varchar(12), hour varchar(5));
--insert into staff_daily_sum (name, date, hour) values (
--select name, date, max(workhour) from staff group by date, name order by name asc, date desc)
--where date in (SELECT DISTINCT [date] FROM [staff] ORDER  BY [date] desc);

--select * from administrator
--insert into administrator (username, password_hash) values('admin02', '123456')
--create table tbl_corpname_number (id integer, category varchar(20), name varchar(80));

--Insert into tbl_corpname_number (id, category, name, rule) values
--(56, "Engagement ", "Accounting Service ", "最多字符 背景信息"),
--(57, "Engagement", "Accounting Service Type", "120个字符"),
--(58, "Engagement", "Leading ", "150个字符"),
--(59, "Contact", "contact id", "1,2,3,4"), 
--(60, "Director", "Director id", "1,2,3,4"), 
--(61, "Shareholder", "Shareholder id", "1,2,3,4")

Create table tbl_Corporation(
corp_id integer primary key, corp1 varchar(10), corp2 varchar(150), corp3 varchar(50), 
corp4 varchar(50), corp5 varchar(20), corp6 varchar(20), corp7 varchar(20), corp8 varchar(20), 
corp9 varchar(20), corp10 varchar(20), corp11 varchar(10), corp12 varchar(10), corp13 varchar(10), 
corp14 varchar(10), corp15 varchar(10), corp16 varchar(150), corp17 varchar(150), corp18 varchar(100), 
corp19 varchar(100), corp20 varchar(20), corp21 varchar(20), corp22 varchar(100), corp23 varchar(200), 
corp24 varchar(150), corp25 varchar(20), corp26 varchar(20), corp27 varchar(20), corp28 varchar(20), 
corp29 varchar(150), corp30 varchar(20), corp31 varchar(150), corp32 varchar(150), corp33 varchar(150), 
corp34 varchar(20), corp35 varchar(150), corp36 varchar(50), corp37 varchar(150), corp38 varchar(20), 
corp39 varchar(80), corp40 varchar(20), corp41 varchar(80), corp42 varchar(50), corp43 varchar(150), 
corp44 varchar(150), corp45 varchar(150), corp46 varchar(80), corp47 varchar(200), corp48 varchar(200), 
corp49 varchar(120), corp50 varchar(120), corp51 varchar(120), corp52 varchar(80), corp53 varchar(30), 
corp54 varchar(80), corp55 varchar(30), corp56 varchar(200), corp57 varchar(120), corp58 varchar(150), 
corp59 varchar(20), corp60 varchar(20),corp61 varchar(20))

Create table tbl_Contacts(
contact_id integer primary key, corp_no varchar(20), corp_contact_no integer, 
position varchar(40), first_name varchar(100), last_name varchar(100), phone varchar(20), 
wechat varchar(150), email varchar(100))

Create table tbl_Directors(
director_id integer primary key, corp_no varchar(20), corp_director_no integer,
first_name varchar(100), last_name varchar(100), sin varchar(20), address varchar(150),
phone varchar(20), email varchar(100))

Create table tbl_Shareholders(
shareholder_id integer primary key, corp_no varchar(20), corp_share_no integer,
shares varchar(80), shares_percent varchar(10), first_name varchar(100), last_name varchar(100),
sin varchar(20), address varchar(150), phone varchar(20), email varchar(100))

create table tbl_Individual(
indiv_id integer primary key, sin integer, prefix varchar(10), last_name varchar(80), first_name varchar(80), middle_name varchar(80), other_name varchar(80),
phone1 varchar(15), phone2 varchar(15), address1 varchar(150), address2 varchar(150), mail_address varchar(150), wechat varchar(150),
cra_sole_proprietor varchar(100), cra_hst_report  varchar(100), cra_payroll varchar(100), cra_withhold_tax  varchar(100),
cra_wsib varchar(50), cra_other varchar(100), 
oversea_asset_t1135 varchar(200), oversea_corp_t1134 varchar(200),
tslip varchar(50), tax_personal_info varchar(200), specific_info varchar(200), engage_account varchar(200), engage_leading varchar(200),
note varchar(200), 
contact_corp1 integer, contact_corp2 integer, contact_corp3 integer, 
director_corp1 integer, director_corp2 integer,director_corp3 integer,
sharehold_corp1 integer, sharehold_corp2 integer,sharehold_corp3 integer,
spouse1 integer, spouse2 integer,
parent10 integer, parent11 integer,parent20 integer,parent21 integer,
child01 integer, child02 integer, child03 integer, child04 integer
)

CREATE TABLE tbl_jobType (job_id integer primary key, short_code varchar(20), 
name varchar(100), descrtiption varchar(250))

INSERT INTO tbl_jobType (short_code, name, descrtiption) VALUES
("Regular", "Regular Service to client", "Services provided for the routine work,like change registration,consulting"),
("AR", "Annual Return", "Services provided for the submission of the Annual Information Return."),
("T2FS", "T2/Financial Statement", "Preparation of corporate income tax returns, including relevant attachments, for the {PeriodEndedText} taxation year. Preparation of unaudited financial statements, including analysis of accounts and preparation of adjustments where necessary, for the year ended {PeriodEndedText}.   Meetings with management to review all of the above as well as other financing and tax matters."),
("BKKPN", "Bookkeeping", "For bookkeeping assistance provided for the period ended {PeriodEndedText}."),
("PR", "Payroll", "Attending to administration and calculation of payroll."),
("HST", "GST/HST/PST Services", "For taxation services rendered on GST/HST/PST matters during the period ended {PeriodEndedText}."),
("T1", "T1", "Preparation of your personal income tax return(s), including all required schedules and attachments, for the year ended {PeriodEndedText}."),
("T1135", "T1135", "Foreign income verification statement"),
("NRWT", "NR Withholding Tax", "Foreign tax related services (details of work completed here)."),
("S216", "S216 NonResident Ren", ""),
("S217", "S217 NRSale", ""),
("GstReb", "GST Rebate", ""),
("NRSP", "NR Speculation Tax-ON", ""),
("TrainClt", "Training to client", ""),
("Adm", "General Administration inner", "General Administration/HR/Personnel/Recruiting"),
("FundAp", "Fund Application", ""),
("Tax related", "Tax related ", ""),
("Other", "Other Task", "")

class Task(db.Model):
    ''' Task detail information'''
    __tablename__ = 'tbl_Task'
    id = db.Column(db.Integer, primary_key=True)
    client_corp = db.Column(db.String(150))
    client_indiv = db.Column(db.String(100))
    jobtype = db.Column(db.String(20))
    periodend = db.Column(db.String(20))
    responsible = db.Column(db.String(100))
    startdate = db.Column(db.String(20))
    enddate = db.Column(db.String(20))
    status = db.Column(db.String(10))
    details = db.Column(db.String(400))
    recurrence = db.Column(db.String(10))
    priority = db.Column(db.String(10))
    worktime = db.Column(db.Float())
    renewperiod = db.Column(db.String(20))
    renewstartdate = db.Column(db.String(20))
    renewenddate = db.Column(db.String(20))
    createdate = db.Column(db.String(20))
    serialno = db.Column(db.Float())
    def __init__(self, client_corp, client_indiv, jobtype, periodend, responsible, startdate, enddate, \
        status, details, recurrence, priority, worktime, renewperiod, renewstartdate, \
        renewenddate, createdate, serialno):
        self.client_corp = client_corp
        self.client_indiv = client_indiv
        self.jobtype = jobtype
        self.periodend = periodend
        self.responsible = responsible
        self.startdate = startdate
        self.enddate = enddate
        self.status = status
        self.details = details
        self.recurrence = recurrence
        self.priority = priority
        self.worktime = worktime
        self.renewperiod = renewperiod
        self.renewstartdate = renewstartdate
        self.renewenddate = renewenddate
        self.createdate = createdate
        self.serialno = serialno

INSERT INTO tbl_Task (client_corp, client_indiv, jobtype, periodend, responsible, startdate, enddate, status, details, recurrence, priority, worktime, renewperiod, renewstartdate, renewenddate, createdate, serialno)
VALUES ('Corporation company 01', '', 'GST', '2020-02-29', 'Ms. Sumart', '2020-03-01', '2020-03-25', 'A', 'prepare GST form', 'm', 'normal', '62.37', '','','','','0.65011864'),
('Corporation 02', '', 'HSTs', '2019-12-31', 'Ms. copr2', '2020-01-01', '2020-12-31', 'A', 'filling HST form', 'y', 'normal', '42.03', '','','','','0.90487503'), 
('Corporation company 02', '', 'HST', '2021-12-31', 'Ms. copr2', '2022-01-01', '2022-12-31', 'A', 'filling HST form', 'y', 'normal', '60.09', '','','','','0.37234043'), 
('Corporation company 03', '', 'PST', '2020-03-31', 'Mr. copr3', '2020-04-01', '2020-06-30', 'Done', 'filling PST decsription', 'q', 'high', '58.07', '','','','','0.35312989'), 
('Corporation company 01', '', 'GST', '2020-05-31', 'Ms. Sumart', '2020-06-01', '2020-06-30', 'A', 'prepare GST form', 'm', 'normal', '56.64', '','','','','0.39156281'), 
('Corporation company 03', '', 'PST', '2020-06-30', 'Mr. copr3', '2020-07-01', '2020-10-31', 'to do', 'filling PST decsription', 'q', 'normal', '47.55', '','','','','0.90996344'), 
('Corporation company 01', '', 'GST', '2020-10-31', 'Ms. Sumart', '2020-11-01', '2020-11-30', 'A', 'prepare GST form', 'm', 'normal', '0', '','','','','0.29747986'), 
('Corporation 02', '', 'HSTs', '2020-12-31', 'Ms. copr2', '2021-01-01', '2021-12-31', 'A', 'filling HST form', 'y', 'normal', '81.36', '2021-12-31', '2022-01-01', '2022-12-31', '','0.49164207'), 
('Corporation company 01', '', 'GST', '2020-03-29', 'Ms. Sumart', '2020-04-01', '2020-04-25', 'A', 'prepare GST form', 'm', 'normal', '77.41', '2020-04-29', '2020-05-01', '2020-05-25', '','0.30110901'), 
('Corporation company 01', '', 'GST', '2020-04-29', 'Ms. Sumart', '2020-05-01', '2020-05-25', 'A', 'prepare GST form', 'm', 'normal', '0', '2020-05-29', '2020-06-01', '2020-06-25', '','0.28644173'), 
('Corporation company 03', '', 'PST', '2020-06-30', 'Mr. copr3', '2020-07-01', '2020-09-30', 'Done', 'filling PST decsription', 'q', 'high', '77.48', '2020-09-30', '2020-10-01', '2020-12-30', '','0.45293206'), 
('Corporation company 01', '', 'GST', '2020-05-29', 'Ms. Sumart', '2020-06-01', '2020-06-25', 'A', 'prepare GST form', 'm', 'normal', '87.36', '2020-06-29', '2020-07-01', '2020-07-25', '','0.09838818'), 
('Corporation company 01', '', 'GST', '2020-06-29', 'Ms. Sumart', '2020-07-01', '2020-07-25', 'A', 'prepare GST form', 'm', 'normal', '0', '2020-07-29', '2020-08-01', '2020-08-25', '','0.20160286'), 
('Corporation company 04', '', 'TAX', '2020-03-29', 'Ms. Sumart', '2020-04-01', '2020-04-25', 'A', 'prepare GST form', 'm', 'normal', '0', '2020-04-29', '2020-05-01', '2020-05-25', '','0.20208304'), 
('Corporation company 04', '', 'TAX', '2020-04-29', 'Ms. Sumart', '2020-05-01', '2020-05-25', 'A', 'prepare GST form', 'm', 'normal', '0', '2020-05-29', '2020-06-01', '2020-06-25', '','0.17101974'), 
('Corporation company 04', '', 'TAX', '2020-05-29', 'Ms. Sumart', '2020-06-01', '2020-06-25', 'A', 'prepare GST form', 'm', 'normal', '0', '2020-06-29', '2020-07-01', '2020-07-25', '','0.13727884'), 
('Corporation 02', '', 'HSTs', '2020-12-31', 'Ms. copr2', '2021-01-01', '2021-12-31', 'A', 'filling HST form', 'y', 'normal', '35.49', '2021-12-31', '2022-01-01', '2022-12-31', '','0.99324109')

update tbl_Task set client_corp_name = (select client_corp_id from tbl_Task where task_id = 4) where task_id = 4;

cursor = db.execute("SELECT ...")
if cursor.empty:
    db.execute("INSERT ...")
else:
    db.execute("UPDATE ...")

CREATE TABLE tbl_Timesheet (timesheet_id Integer primary key, startdate VARCHAR(10), calhour VARCHAR(10), adjhour VARCHAR(4), 
    adjmin VARCHAR(4), workhour Float, entryname VARCHAR(80), entrycontent Text, activitytype VARCHAR(80), 
    corp1 VARCHAR(100), corp2 VARCHAR(100), corp3 VARCHAR(100), corp4 VARCHAR(100), staff VARCHAR(80), 
    timemark Integer, avgtime Float, jobid1 Integer, jobid2 Integer, jobid3 Integer, jobid4 Integer,
    starttime VARCHAR(5), serialno VARCHAR(20))

CREATE TABLE tbl_Corporation_report (corp_report_id Integer primary key, corp VARCHAR(100), startdate VARCHAR(20),
    entryname VARCHAR(80), activitytype VARCHAR(80), entrycontent Text, workhour Float, timemark Integer,
    jobid Integer, serialno VARCHAR(20))

CREATE TABLE tbl_Staff (staff_id Integer primary key, name VARCHAR(80), startdate VARCHAR(15), job VARCHAR(80),
    calendarhour VARCHAR(10), adjhour VARCHAR(5), adjmin VARCHAR(5), workhour Float,timemark Integer, serialno VARCHAR(20))


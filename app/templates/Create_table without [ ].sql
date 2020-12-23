CREATE TABLE account (id INTEGER NOT NULL, username VARCHAR(256), PRIMARY KEY (id))
CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL, CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num))
CREATE TABLE tbl_Contacts(contact_id integer primary key, corp_no varchar(20), corp_contact_no integer, position varchar(40), first_name varchar(100), last_name varchar(100), phone varchar(20), wechat varchar(150), email varchar(100))
CREATE TABLE tbl_Corporation(corp_id integer PRIMARY KEY, corp1 varchar(10), corp2 varchar(150), corp3 varchar(50),corp4 varchar(50),corp5 varchar(20), corp6 varchar(20), corp7 varchar(20),corp8 varchar(20),corp9 varchar(20),corp10 varchar(20),corp11 varchar(10),corp12 varchar(10),corp13 varchar(10),corp14 varchar(10),corp15 varchar(10),corp16 varchar(150),corp17 varchar(150),corp18 varchar(100),corp19 varchar(100),corp20 varchar(20),corp201 VARCHAR(20),corp21 varchar(20),corp211 VARCHAR(20),corp22 varchar(100),corp23 varchar(200),corp24 varchar(150),corp25 varchar(20),corp26 varchar(20),corp27 varchar(20),corp28 varchar(20),corp29 varchar(150),corp30 varchar(20),corp31 varchar(150),corp32 varchar(150),corp33 varchar(150),corp34 varchar(20),corp35 varchar(150),corp36 varchar(50),corp37 varchar(150),corp38 varchar(20),corp39 varchar(80),corp40 varchar(20),corp41 varchar(80),corp42 varchar(50),corp43 varchar(150),corp44 varchar(150),corp45 varchar(150),corp46 varchar(80),corp47 varchar(200),corp48 varchar(200),corp49 varchar(120),corp50 varchar(120),corp51 varchar(120),corp52 varchar(80),corp53 varchar(30),corp54 varchar(80),corp55 varchar(30),corp56 varchar(200),corp57 varchar(120),corp58 varchar(150),contact varchar(20),director varchar(20),shareholder varchar(20),task INTEGER,recent_update VARCHAR(50),contact_position VARCHAR(200),shareholder_info VARCHAR(400),shareholder_corp VARCHAR(20),shareholder_corp_info VARCHAR(400),corp_as_shareholder VARCHAR(20),timemark VARCHAR(26))

max(length(corp1)), max(length(corp2)), max(length(corp3)), max(length(corp4)), max(length(corp5)), max(length(corp6)), max(length(corp7)), max(length(corp8)), max(length(corp9)), max(length(corp10)), max(length(corp11)), max(length(corp12)), max(length(corp13)), max(length(corp14)), max(length(corp15)), max(length(corp16)), max(length(corp17)), max(length(corp18)), max(length(corp19)), max(length(corp20)), max(length(corp201)), max(length(corp21)), max(length(corp211)), max(length(corp22)), max(length(corp23)), max(length(corp24)), max(length(corp25)), max(length(corp26)), max(length(corp27)), max(length(corp28)), max(length(corp29)), max(length(corp30)), max(length(corp31)), max(length(corp32)), max(length(corp33)), max(length(corp34)), max(length(corp35)), max(length(corp36)), max(length(corp37)), max(length(corp38)), max(length(corp39)), max(length(corp40)), max(length(corp41)), max(length(corp42)), max(length(corp43)), max(length(corp44)), max(length(corp45)), max(length(corp46)), max(length(corp47)), max(length(corp48)), max(length(corp49)), max(length(corp50)), max(length(corp51)), max(length(corp52)), max(length(corp53)), max(length(corp54)), max(length(corp55)), max(length(corp56)), max(length(corp57)), max(length(corp58)), max(length(contact)), max(length(director)), max(length(shareholder)), max(length(task)), max(length(recent_update)), max(length(contact_position)), max(length(shareholder_info)), max(length(shareholder_corp)), max(length(shareholder_corp_info)), max(length(corp_as_shareholder)), max(length(timemark))


CREATE TABLE tbl_Corporation_report(corp_report_id Integer PRIMARY KEY,corp VARCHAR(100),startdate VARCHAR(20),entryname VARCHAR(80),activitytype VARCHAR(80),entrycontent Text,workhour Float,timemark Integer,jobid Integer,serialno VARCHAR(20));
CREATE TABLE tbl_Directors(director_id integer primary key, corp_no varchar(20), corp_director_no integer, first_name varchar(100), last_name varchar(100), sin varchar(20), address varchar(150), phone varchar(20), email varchar(100));
CREATE TABLE tbl_Individual(indiv_id integer PRIMARY KEY,sin integer,prefix varchar(10),last_name varchar(80),first_name varchar(80),other_name varchar(80),email varchar(80),phone1 varchar(15),phone1digit VARCHAR(15),phone2 varchar(15),phone2digit VARCHAR(15),address1 varchar(150),address2 varchar(150),mail_address varchar(150),wechat varchar(150),cra_sole_proprietor varchar(100),cra_hst_report varchar(100),cra_payroll varchar(100),cra_withhold_tax varchar(100),cra_wsib varchar(50),cra_other varchar(100),oversea_asset_t1135 varchar(200),oversea_corp_t1134 varchar(200),tslip varchar(50),tax_personal_info varchar(200),specific_info varchar(200),engage_account varchar(200),engage_leading varchar(200),note varchar(200),contact_corp VARCHAR(30),director_corp VARCHAR(30),sharehold_corp VARCHAR(30),spouse VARCHAR(20),parent VARCHAR(40),child VARCHAR(40),timemark VARCHAR(26));
CREATE TABLE tbl_Shareholders(shareholder_id integer primary key, corp_no varchar(20), corp_share_no integer, shares varchar(80), shares_percent varchar(10), first_name varchar(100), last_name varchar(100), sin varchar(20), address varchar(150), phone varchar(20), email varchar(100));
CREATE TABLE tbl_Staff (staff_id Integer primary key, name VARCHAR(80), startdate VARCHAR(15), job VARCHAR(80), calendarhour VARCHAR(10), adjhour VARCHAR(5), adjmin VARCHAR(5), workhour Float,timemark Integer, serialno VARCHAR(20));
CREATE TABLE tbl_Task(task_id Integer PRIMARY KEY,client_corp_id INT,client_corp_name VARCHAR(150),client_corp_bussi_no VARCHAR(20),client_indiv_id INT,client_indiv_name VARCHAR(100),client_indiv_sin VARCHAR(10),jobtype_id INT,jobtype_code VARCHAR(20),periodend VARCHAR(20),responsible VARCHAR(100),startdate VARCHAR(20),enddate VARCHAR(20),status VARCHAR(10),details text, recurrence VARCHAR(10), priority VARCHAR(10),worktime DECIMAL(2),renewperiod VARCHAR(20),renewstartdate VARCHAR(20),renewenddate VARCHAR(20),createdate VARCHAR(20),serialno FLOAT);
CREATE TABLE tbl_Timesheet(timesheet_id Integer PRIMARY KEY,startdate VARCHAR(10),calhour VARCHAR(10),adjhour VARCHAR(4),adjmin VARCHAR(4),workhour Float,entryname VARCHAR(80),entrycontent Text,activitytype VARCHAR(80),corp1 VARCHAR(100),corp2 VARCHAR(100),corp3 VARCHAR(100),corp4 VARCHAR(100),staff VARCHAR(80),timemark Integer,avgtime Float,jobid1 Integer,jobid2 Integer,jobid3 Integer,jobid4 Integer,starttime VARCHAR(5),serialno VARCHAR(20));
CREATE TABLE tbl_activity_code (id Integer PRIMARY KEY, name text);
CREATE TABLE tbl_corpname_number(id integer,category varchar(20),name varchar(80),rule VARCHAR(80));
CREATE TABLE tbl_jobType(job_id integer PRIMARY KEY,short_code VARCHAR(20),name VARCHAR(100),description TEXT);
CREATE TABLE tbl_log(log_id Integer PRIMARY KEY,username VARCHAR(50),email VARCHAR(50),password VARCHAR(50),ip VARCHAR(20),datadate VARCHAR(30),datatime INTEGER,badfield VARCHAR(10),hourlock INTEGER,daylock INTEGER,status VARCHAR(10),attemptafterlock INTEGER);
CREATE TABLE users( id INTEGER PRIMARY KEY NOT NULL, username VARCHAR(64), email VARCHAR(120), password_hash VARCHAR(128), about_me VARCHAR(140), last_seen DATETIME, identification INTEGER)
CREATE TABLE learning_data_table (id INTEGER NOT NULL, name VARCHAR(100), email VARCHAR(100), phone VARCHAR(100), PRIMARY KEY (id))
CREATE TABLE mulform (id Integer PRIMARY KEY, name text)
CREATE TABLE num1 (id integer primary key, num1 float)
CREATE TABLE num2(id integer PRIMARY KEY, num2 float)
CREATE TABLE tt(timesheet_id Integer PRIMARY KEY, startdate VARCHAR(10), calhour VARCHAR(10), adjhour VARCHAR(4), adjmin VARCHAR(4), workhour Float, entryname VARCHAR(80), entrycontent Text, activitytype VARCHAR(80), corp1 VARCHAR(100), corp2 VARCHAR(100), corp3 VARCHAR(100), corp4 VARCHAR(100), staff VARCHAR(80), timemark Integer, avgtime Float, jobid1 Integer, jobid2 Integer, jobid3 Integer, jobid4 Integer, starttime VARCHAR(5), serialno VARCHAR(20))
CREATE TABLE timesheettempdata(t0 varchar(15) PRIMARY KEY, t1 varchar(20), t2 varchar(10), t3 varchar(4), t4 varchar(4), t5 varchar(10), t6 varchar(100), t7 varchar(200), t8 varchar(80), t9 varchar(100), t10 varchar(100), t11 varchar(100), t12 varchar(100), t13 varchar(2))

CREATE TRIGGER del_empty_row AFTER INSERT ON tbl_Corporation_report BEGIN DELETE FROM tbl_Corporation_report WHERE corp = ''; END

CREATE TRIGGER del_num1 BEFORE DELETE ON num2 BEGIN DELETE FROM num1 WHERE id = old.id; END

CREATE TRIGGER trig_corporation_report_insert1 AFTER INSERT ON tbl_Timesheet
BEGIN
  INSERT INTO tbl_Corporation_report (corp,  startdate,  entryname,  activitytype,  entrycontent,  workhour,  timemark,  jobid,  serialno)
    VALUES (new.corp1, new.startdate, new.entryname, new.activitytype, new.entrycontent, new.avgtime, new.timemark, new.jobid1, new.serialno);
  INSERT INTO tbl_Corporation_report (corp,  startdate,  entryname,  activitytype,  entrycontent,  workhour,  timemark,  jobid,  serialno)
    VALUES (new.corp2, new.startdate, new.entryname, new.activitytype, new.entrycontent, new.avgtime, new.timemark, new.jobid2, new.serialno);
  INSERT INTO tbl_Corporation_report (corp,  startdate,  entryname,  activitytype,  entrycontent,  workhour,  timemark,  jobid,  serialno)
    VALUES (new.corp3, new.startdate, new.entryname, new.activitytype, new.entrycontent, new.avgtime, new.timemark, new.jobid3, new.serialno);
  INSERT INTO tbl_Corporation_report (corp,  startdate,  entryname,  activitytype,  entrycontent,  workhour,  timemark,  jobid,  serialno)
    VALUES (new.corp4, new.startdate, new.entryname, new.activitytype, new.entrycontent, new.avgtime, new.timemark, new.jobid4, new.serialno);
END

CREATE TRIGGER trig_delete_corp_report_after_timesheetdelete1 AFTER DELETE ON tbl_Timesheet
BEGIN 
DELETE FROM tbl_Corporation_report WHERE (timemark = old.timemark AND jobid = old.jobid1 AND EXISTS (SELECT 1 FROM  tbl_Corporation_report WHERE (timemark = old.timemark AND jobid = old.jobid1)));
DELETE FROM tbl_Corporation_report WHERE (timemark = old.timemark AND jobid = old.jobid2 AND EXISTS (SELECT 1 FROM tbl_Corporation_report WHERE (timemark = old.timemark AND jobid = old.jobid2)));
DELETE FROM tbl_Corporation_report WHERE (timemark = old.timemark AND jobid = old.jobid3 AND EXISTS (SELECT 1 FROM tbl_Corporation_report WHERE (timemark = old.timemark AND jobid = old.jobid3)));
DELETE FROM tbl_Corporation_report WHERE (timemark = old.timemark AND jobid = old.jobid4 AND EXISTS (SELECT 1 FROM tbl_Corporation_report WHERE (timemark = old.timemark AND jobid = old.jobid4)));
END

CREATE TRIGGER trig_delete_staff_after_timesheetdel1 AFTER DELETE ON tbl_Timesheet
BEGIN
  DELETE FROM tbl_Staff WHERE (timemark = old.timemark AND EXISTS (SELECT 1 FROM tbl_Staff WHERE (timemark = old.timemark)));
END

CREATE TRIGGER trig_staff_insert1 AFTER INSERT ON tbl_Timesheet
BEGIN
  INSERT INTO tbl_Staff (name, startdate, job, calendarhour, adjhour, adjmin, workhour, timemark, serialno)
    VALUES (new.staff, new.startdate, new.entryname, new.calhour, new.adjhour, new.adjmin, new.workhour, new.timemark, new.serialno);
END

CREATE TRIGGER trig_task_worktime_after_insertion AFTER INSERT ON tbl_Corporation_report
BEGIN
  UPDATE tbl_Task SET worktime = ROUND ((worktime + new.workhour), 2) WHERE task_id = new.jobid;
END

CREATE TRIGGER trig_tbl_task_worktiem_after_update AFTER UPDATE ON tbl_Corporation_report
BEGIN
  UPDATE tbl_Task SET worktime = CASE WHEN worktime > old.workhour THEN ROUND ((worktime - old.workhour + new.workhour), 2) ELSE ROUND ((new.workhour), 2) END WHERE task_id = new.jobid;
END

CREATE TRIGGER trig_tbl_task_worktime_after_delete AFTER DELETE ON tbl_Corporation_report
BEGIN
  UPDATE tbl_Task SET worktime = CASE WHEN worktime > old.workhour THEN ROUND ((worktime - old.workhour), 2) ELSE 0 END WHERE task_id = old.jobid;
END

CREATE TRIGGER trig_update_staff_after_timesheetedit1 AFTER UPDATE ON tbl_Timesheet
BEGIN
  UPDATE tbl_Staff SET name = new.staff, startdate = new.startdate, job = new.entryname, calendarhour = new.calhour, adjhour = new.adjhour, adjmin = new.adjmin, workhour = new.workhour, serialno = new.serialno WHERE timemark = old.timemark;
END

CREATE TRIGGER update_num1 AFTER UPDATE ON num2
BEGIN
  UPDATE num1 SET num1 = CASE WHEN num1 > old.num2 THEN (num1 - old.num2 + new.num2) ELSE new.num2 END WHERE id = new.id;
END

CREATE TRIGGER user_number AFTER INSERT ON users
BEGIN
  DELETE FROM users WHERE id NOT IN (SELECT id FROM users ORDER  BY id LIMIT 10);
END
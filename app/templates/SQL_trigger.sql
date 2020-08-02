--  tbl_Timesheet
-- name: trig_corporation_report_insert AFTER INSERT
CREATE TRIGGER [IF NOT EXISTS] trig_corporation_report_insert 
   AFTER INSERT 
   ON tbl_Timesheet
BEGIN
 INSERT INTO "tbl_Corporation_report" (corp, startdate, entryname, activitytype, entrycontent, workhour, timemark, jobid, serialno) 
  VALUES (new.corp1, new.startdate, new.entryname, new.activitytype, new.entrycontent, new.avgtime, new.timemark, new.jobid1, new.serialno);
INSERT INTO "tbl_Corporation_report" (corp, startdate, entryname, activitytype, entrycontent, workhour, timemark, jobid, serialno) 
  VALUES (new.corp2, new.startdate, new.entryname, new.activitytype, new.entrycontent, new.avgtime, new.timemark, new.jobid1, new.serialno);
INSERT INTO "tbl_Corporation_report" (corp, startdate, entryname, activitytype, entrycontent, workhour, timemark, jobid, serialno) 
  VALUES (new.corp3, new.startdate, new.entryname, new.activitytype, new.entrycontent, new.avgtime, new.timemark, new.jobid1, new.serialno);
INSERT INTO "tbl_Corporation_report" (corp, startdate, entryname, activitytype, entrycontent, workhour, timemark, jobid, serialno) 
  VALUES (new.corp4, new.startdate, new.entryname, new.activitytype, new.entrycontent, new.avgtime, new.timemark, new.jobid1, new.serialno);
END;

INSERT INTO "tbl_Corporation_report"
  (
  [corp], 
  [startdate], 
  [entryname], 
  [activitytype], 
  [entrycontent], 
  [workhour], 
  [timemark], 
  [jobid], 
  [serialno])
  VALUES ([new].[corp1], [new].[startdate], [new].[entryname], [new].[activitytype], [new].[entrycontent], [new].[avgtime], [new].[timemark], [new].[jobid1], [new].[serialno]);
INSERT INTO "tbl_Corporation_report"
  (
  [corp], 
  [startdate], 
  [entryname], 
  [activitytype], 
  [entrycontent], 
  [workhour], 
  [timemark], 
  [jobid], 
  [serialno])
  VALUES ([new].[corp2], [new].[startdate], [new].[entryname], [new].[activitytype], [new].[entrycontent], [new].[avgtime], [new].[timemark], [new].[jobid2], [new].[serialno]);
INSERT INTO "tbl_Corporation_report"
  (
  [corp], 
  [startdate], 
  [entryname], 
  [activitytype], 
  [entrycontent], 
  [workhour], 
  [timemark], 
  [jobid], 
  [serialno])
  VALUES ([new].[corp3], [new].[startdate], [new].[entryname], [new].[activitytype], [new].[entrycontent], [new].[avgtime], [new].[timemark], [new].[jobid3], [new].[serialno]);
INSERT INTO "tbl_Corporation_report"
  (
  [corp], 
  [startdate], 
  [entryname], 
  [activitytype], 
  [entrycontent], 
  [workhour], 
  [timemark], 
  [jobid], 
  [serialno])
  VALUES ([new].[corp4], [new].[startdate], [new].[entryname], [new].[activitytype], [new].[entrycontent], [new].[avgtime], [new].[timemark], [new].[jobid4], [new].[serialno]);


-- name: trig_staff_insert AFTER INSERT
INSERT INTO "tbl_Staff"
  (
  [name], 
  [startdate], 
  [job], 
  [calendarhour], 
  [adjhour], 
  [adjmin], 
  [workhour], 
  [timemark], 
  [serialno])
  VALUES ([new].[staff], [new].[startdate], [new].[entryname], [new].[calhour], [new].[adjhour], [new].[adjmin], [new].[workhour], [new].[timemark], [new].[serialno]);

-- tbl_Corporation_report
-- name: trig_tbl_task_worktiem_after_update
UPDATE
  "tbl_Task"
SET
  [worktime] = CASE WHEN [worktime] > [old].[workhour] THEN ROUND (([worktime] - [old].[workhour] + [new].[workhour]), 2) ELSE ROUND (([new].[workhour]), 2) END
WHERE
  [task_id] = [new].[jobid];

-- trig_tbl_task_worktime_after_delete
UPDATE
  "tbl_Task"
SET
  [worktime] = CASE WHEN [worktime] > [old].[workhour] THEN ROUND (([worktime] - [old].[workhour]), 2) ELSE 0 END
WHERE
  [task_id] = [old].[jobid];

-- trig_task_worktime_after_insertion
UPDATE
  "tbl_Task"
SET
  [worktime] = ROUND (([worktime] + [new].[workhour]), 2)
WHERE
  [task_id] = [new].[jobid];



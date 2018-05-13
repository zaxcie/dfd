/*
Start with batting tables
 */

/*
Query column that are not part of _additional_ table
 */
SELECT A.COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS A
WHERE A.TABLE_NAME = 'away_batting' AND
  A.COLUMN_NAME NOT IN (SELECT A.COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS A
WHERE A.TABLE_NAME = 'away_additional_batting');

/*
Create temp table for batting
 */
SELECT aa.*, h.s_h, h.bo, h.slg, h.s_rbi, h.s_bb, h.obp, h.s_r, h.s_hr, h.s_so, h.avg, h.ops INTO TempAwayBatting
  FROM away_additional_batting as aa
  FULL JOIN away_batting as h ON (aa.name_display_first_last = h.name_display_first_last AND
      h.game_id = aa.game_id);

SELECT aa.*, h.s_h, h.bo, h.slg, h.s_rbi, h.s_bb, h.obp, h.s_r, h.s_hr, h.s_so, h.avg, h.ops INTO TempHomeBatting
  FROM home_additional_batting as aa
  FULL JOIN home_batting as h ON (aa.name_display_first_last = h.name_display_first_last AND
      h.game_id = aa.game_id);

/*
Find problematic columns
 */
SELECT column_name, data_type
FROM information_schema.columns
WHERE (information_schema.columns.table_name = 'tempawaybatting') OR
(information_schema.columns.table_name = 'temphomebatting');

/*
Change column type for batting tables
# TODO fix in the python extraction
 */
ALTER TABLE public.tempawaybatting ALTER COLUMN bam_s_d TYPE INTEGER USING bam_s_d::INTEGER;
ALTER TABLE public.tempawaybatting ALTER COLUMN bis_s_d TYPE INTEGER USING bis_s_d::INTEGER;
ALTER TABLE public.tempawaybatting ALTER COLUMN first_gidp TYPE INTEGER USING first_gidp::INTEGER;
ALTER TABLE public.tempawaybatting ALTER COLUMN gidp TYPE INTEGER USING gidp::INTEGER;
ALTER TABLE public.tempawaybatting ALTER COLUMN go TYPE INTEGER USING go::INTEGER;
ALTER TABLE public.tempawaybatting ALTER COLUMN cs TYPE INTEGER USING cs::INTEGER;

ALTER TABLE public.temphomebatting ALTER COLUMN bam_s_d TYPE INTEGER USING bam_s_d::INTEGER;
ALTER TABLE public.temphomebatting ALTER COLUMN bis_s_d TYPE INTEGER USING bis_s_d::INTEGER;
ALTER TABLE public.temphomebatting ALTER COLUMN first_gidp TYPE INTEGER USING first_gidp::INTEGER;
ALTER TABLE public.temphomebatting ALTER COLUMN gidp TYPE INTEGER USING gidp::INTEGER;
ALTER TABLE public.temphomebatting ALTER COLUMN go TYPE INTEGER USING go::INTEGER;
ALTER TABLE public.temphomebatting ALTER COLUMN cs TYPE INTEGER USING cs::INTEGER;

/*
Add side to a record, then union between away and home games
 */
ALTER TABLE public.tempawaybatting ADD side TEXT DEFAULT 'away' NULL;
ALTER TABLE public.temphomebatting ADD side TEXT DEFAULT 'home' NULL;

SELECT b.* INTO Batting
FROM (SELECT a.* FROM TempAwayBatting AS a
  UNION
  SELECT h.* FROM TempHomeBatting AS h) AS b;

DROP TABLE tempawaybatting;
DROP TABLE temphomebatting;

SELECT to_date(SUBSTR(game_id, 1, 10), 'YYYY_MM_DD') AS date
  FROM batting;

ALTER TABLE public.batting ADD date DATE;
UPDATE public.batting SET date = to_date(SUBSTR(game_id, 1, 10), 'YYYY_MM_DD');

/*
Pitching
 */
/*
Query column that are not part of _additional_ table
 */
SELECT A.COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS A
WHERE A.TABLE_NAME = 'away_pitching' AND
  A.COLUMN_NAME NOT IN (SELECT A.COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS A
WHERE A.TABLE_NAME = 'away_additional_pitching');

/*
Create temp table for batting
 */
SELECT aa.*, h.era, h.note, h.s_bb, h.w, h.l, h.s_r, h.s_er, h.sv, h.hld, h.s_so, bs, s_ip INTO TempAwayPitching
  FROM away_additional_pitching as aa
  FULL JOIN away_pitching as h ON (aa.name_display_first_last = h.name_display_first_last AND
      h.game_id = aa.game_id);

SELECT aa.*, h.era, h.note, h.s_bb, h.w, h.l, h.s_r, h.s_er, h.sv, h.hld, h.s_so, bs, s_ip INTO TemphomePitching
  FROM home_additional_pitching as aa
  FULL JOIN home_pitching as h ON (aa.name_display_first_last = h.name_display_first_last AND
      h.game_id = aa.game_id);

/*
Find problematic columns
 */
SELECT column_name, data_type
FROM information_schema.columns
WHERE (information_schema.columns.table_name = 'tempawaypitching') OR
(information_schema.columns.table_name = 'temphomepitching');

ALTER TABLE public.TempAwayPitching ADD side TEXT DEFAULT 'away' NULL;
ALTER TABLE public.TemphomePitching ADD side TEXT DEFAULT 'home' NULL;

SELECT b.* INTO Pitching
FROM (SELECT a.* FROM TempAwayPitching AS a
  UNION
  SELECT h.* FROM TemphomePitching AS h) AS b;

ALTER TABLE public.pitching ADD date DATE;
UPDATE public.pitching SET date = to_date(SUBSTR(game_id, 1, 10), 'YYYY_MM_DD');


DROP TABLE TempAwayPitching;
DROP TABLE TemphomePitching;
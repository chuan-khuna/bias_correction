# bias_correction

## `/observed`
ไฟล์ csv มาจาก repository `climate simple plot/station_data`

## `/observed_qc`
folder สำหรับเก็บการพล็อต missing value ของ observed data ที่มาจากการรันไฟล์ `missing_plot.py`
```
/observed_qc
|- box_dist
  |- prcp (*.jpg)
  |- temperature (*.jpg)
|- error_val (เก็บ *.csv ไม่สอดคล้อง)
|- missing_value
  |- month
  |- monthly
|- outlier
  |- TAVG (*.csv)
  |- TMAX (*.csv)
  |- TMIN (*.csv)
  |- Visualization  (*.jpg)
```


## `/RCM`
```
RCM
|- MPI-ESM-MR (เก็บ dataset มี 3 folder ย่อย)
|- export_rcm_to_csv.py (สำหรับแปลงข้อมูลรอบๆประเทศไทยจาก nc ไฟล์มาเป็น csv)
```

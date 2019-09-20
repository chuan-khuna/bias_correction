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
|- inconsistency (เก็บ *.csv ไม่สอดคล้อง)
|- missing_value
  |- month (*.jpg)
  |- monthly (*.jpg)
|- outlier
  |- TAVG (*.csv)
  |- TMAX (*.csv)
  |- TMIN (*.csv)
  |- Visualization  (*.jpg)
|- summary_qc (เก็บไฟล์ pdf, csv แบบสรุปทุกสถานี)
```

## `/RCM`

```
RCM
|- MPI-ESM-MR (เก็บ dataset มี 3 folder ย่อย)
|- export_rcm_to_csv.py (สำหรับแปลงข้อมูลรอบๆประเทศไทยจาก nc ไฟล์มาเป็น csv)
```

## `data_qc_visualization.py`

พล็อตกราฟทำความเข้าใจข้อมูลและดูคุณภาพของข้อมูล เช่น outlier, inconsistency(เช่น TMIN > TMAX)

## `concat_img_to_pdf.py`

รวมรูปภาพ output จาก `data_qc_visualization.py` ให้เป็นไฟล์ pdf

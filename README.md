# bias_correction

## Data
### `/observed`

ไฟล์ csv มาจาก repository `climate simple plot/station_data`
(ไฟล์ csv ดิบจากสถานีต่างๆ แยกเป็นสถานีละไฟล์)

### `/observed_clean`

ไฟล์ csv ข้อมูลรูปแบบใหม่ จัด column ตามสถานี เพื่อความง่ายในการเรียกใช้งาน?

ไฟล์ csv มาจาก repository `climate simple plot/station_data`

### `/RCM`

```
RCM
  |- MPI-ESM-MR (เก็บ dataset มี 3 folder ย่อย)
  |- export_rcm_to_csv.py (สำหรับแปลงข้อมูลรอบๆประเทศไทยจาก nc ไฟล์มาเป็น csv)
```

## Bias Correction (การปรับปรุงความเอนเอียง)

จะใช้ไลบรารี่ Qmap (ภาษา R) และ วิธีอย่างง่ายที่เขียนเองด้วยภาษา python (`my_bias_correction_lib.py`)


## Data Quality

ดูคุณภาพของข้อมูล 3 แบบ Missing, Outlier, Inconsistency (ไม่สอดคล้อง เช่น MAX < MIN)

### `/observed_qc`

folder สำหรับเก็บการ visaulization และ csv ของการทำ data QC

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

### `concat_csv.py`

รวมไฟล์ csv ของการทำ Data QC

### `data_qc_visualization.py`

พล็อตกราฟทำความเข้าใจข้อมูลและดูคุณภาพของข้อมูล เช่น outlier, inconsistency(เช่น TMIN > TMAX)

### `concat_img_to_pdf.py`

รวมรูปภาพ output จาก `data_qc_visualization.py` ให้เป็นไฟล์ pdf

### `/my_data_qc_lib`

ไลบรารี่ QC ที่เขียนเอง


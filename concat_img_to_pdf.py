import os
from fpdf import FPDF

def concat():
    image_folders = [
        "./observed_qc/box_dist/prcp/",
        "./observed_qc/box_dist/temperature/",
        "./observed_qc/missing_value/month/",
        "./observed_qc/missing_value/monthly/",
        "./observed_qc/outlier/Visualization/"
    ]

    output_path = "./observed_qc/pdf_summary_qc/"

    output_pdf_names = [
        "prpcp_boxplot.pdf",
        "temperature_boxplot.pdf",
        "missing_value_heatmap_by_month.pdf",
        "missing_value_heatmap_monthly.pdf",
        "outlier.pdf"
    ]

    A4_WIDTH = 210
    IMG_WIDTH = 150
    IMG_X_POS = (A4_WIDTH-IMG_WIDTH)//2

    for i in range(len(image_folders)):
        folder = image_folders[i]
        output_file = output_pdf_names[i]

        # create pdf file
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_font("Arial", size=14)

        cnt = 0
        img_per_page = 2
        for img_file in os.listdir(folder):
            print(f"{cnt} \t {img_file}")
            if cnt % img_per_page == 0:
                pdf.add_page()
            
            pdf.cell(200, 10, txt=img_file[:-4], ln=1, align="C")
            image_path = folder+img_file
            pdf.image(image_path, x=IMG_X_POS, w=IMG_WIDTH)
            pdf.ln(h = '')
            cnt += 1
        pdf.output(output_path+output_file)
        pdf.close()

if __name__ == '__main__':
    concat()
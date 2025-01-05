from openpyxl import Workbook
import os
from tkinter import messagebox
import datetime
import tkinter as tk
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,Spacer, Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER


class Informe:
    @classmethod
    def generar_informe_caja(cls,ventas_turno,saldo_caja, efectivo, saldo_fiado, saldo_pagado,lista_nombres):
        # Crear archivo Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Informe de Ventas"

        # Agregar encabezados
        ws.append(["Total Ventas", "Total Caja", "Total (Ventas + Caja)"])
        ws.append([ventas_turno, saldo_caja, ventas_turno + saldo_caja])

        # Agregar un espacio
        ws.append([])
        ws.append([])

        # Agregar encabezados para productos
        ws.append(["Nombre del Producto", "Cantidad Vendida"])

        # Agregar productos vendidos
        for item in lista_nombres:
            ws.append([item["nombre"], item["cantidad"]])

        
        # Crear una ventana de Tkinter oculta (no queremos que aparezca una ventana vacía)
        root = tk.Tk()
        root.withdraw()

        fecha_ac = datetime.datetime.now().strftime("%Y-%m-%d")
        # Abrir el cuadro de diálogo "Guardar como" y obtener la ruta y el nombre del archivo
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                filetypes=[("Excel files", "*.xlsx"),
                                                            ("All files", "*.*")],
                                                initialfile=f"Informe_cierre_caja_{fecha_ac}")
        if file_path:
            wb.save(file_path)
            
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                filetypes=[("PDF files", "*.pdf"),
                                                            ("All files", "*.*")],
                                                initialfile=f"Informe_cierre_caja_{fecha_ac}")
        if file_path:
            # Crear un documento PDF con ReportLab
            pdf = SimpleDocTemplate(file_path, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            style_normal = styles["Normal"]

            # Añadir el total de ventas, el total en caja y la suma de ambos
            style_centered = ParagraphStyle(name='Centered', alignment=TA_CENTER, fontSize=14)
            elements.append(Paragraph(f"<b>Informe de Cierre de Caja</b>", style_centered))
            elements.append(Spacer(1,12))
            elements.append(Paragraph(f"<b>Total pagado clientes:</b>"+ "${:,.2f}".format(saldo_pagado), style_normal))
            
            elements.append(Paragraph(f"<b>Total de cartera:</b>"+"${:,.2f}".format(saldo_fiado), style_normal))
            elements.append(Paragraph(f"<b>Total ventas:</b>"+"${:,.2f}".format(ventas_turno), style_normal))
            elements.append(Spacer(1,12))
            elements.append(Paragraph(f"<b>Total efectivo:</b>"+"${:,.2f}".format(efectivo), style_normal))
            elements.append(Paragraph(f"<b>Total Caja:</b>"+ "${:,.2f}".format(saldo_caja), style_normal))
            elements.append(Paragraph(f"<b>Total (Efectivo + Caja):</b>"+"${:,.2f}".format(efectivo + saldo_caja), style_normal))
            elements.append(Spacer(1,12))
            # Crear una tabla con los productos vendidos
            data = [["Nombre del Producto", "Cantidad"]]  # Encabezados de la tabla
            for item in lista_nombres:
                data.append([item['nombre'], item['cantidad']])

            # Estilo de la tabla
            table = Table(data)
            custom_color = colors.Color(96/255, 20/255, 156/255, alpha=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), custom_color),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))

            elements.append(table)

            # Construir el PDF
            pdf.build(elements)
        
        messagebox.showinfo("LMH SOLUTIOS", f"El informe de ventas ha sido guardado")
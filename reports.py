import pandas as pd
import os


# Invoice directories
dir_posti = os.fsencode("/Users/esko/Documents/invoice_reports/posti_invoices/")
dir_mh = os.fsencode("/Users/esko/Documents/invoice_reports/matkahuolto_invoices/")

# Output directory
dir_reports = "/Users/esko/Documents/invoice_reports/reports/"


def posti(df1, df2):
    for file in os.listdir(dir_posti):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            invoice = pd.read_csv(dir_posti.decode("utf-8") + filename, delimiter=";")
            invoice = invoice[["Lisätietoja tai lähettäjän viite", "Hinta yhteensä"]]
            invoice = invoice.rename(
                columns={
                    "Lisätietoja tai lähettäjän viite": "Myyntitilaus",
                    "Hinta yhteensä": "Hinta",
                }
            )
            df_report = pd.merge(df1, df2, on="Myyntitilaus")
            df_report = pd.merge(df_report, invoice, on="Myyntitilaus")
            df_report = df_report.drop_duplicates(subset="Tilausnum", keep="first")
            # removing ".csv" from the file name
            report = f"Tilitysraportti {filename}"[:-4]
            df_report.to_excel(
                dir_reports + report + ".xlsx", index=False,
            )
            print(f"Created: {report}")


def matkahuolto():
    for file in os.listdir(dir_mh):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            invoice = pd.read_csv(
                dir_mh.decode("utf-8") + filename,
                delimiter=";",
                usecols=[0, 10, 11],
                encoding="cp1252",
            )
            # Changing the order of columns
            invoice = invoice[[invoice.columns[i] for i in [0, 2, 1]]]
            invoice.columns.values[0] = "Pvm"
            invoice.columns.values[1] = "Toimitus"
            invoice.columns.values[2] = "Hinta"
            invoice["Pvm"] = invoice["Pvm"].apply(lambda x: x[-10:])
            invoice = invoice[
                invoice["Toimitus"].str.startswith("Lähtöpaikka: Turku", na=False)
            ]
            report = f"Tilitysraportti {filename}"[:-4]
            invoice.to_excel(
                dir_reports + report + ".xlsx", index=False,
            )
            print(f"Created: {report}")

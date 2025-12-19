import os
import pandas as pd

# Path dataset (file raw tetap berada di luar folder preprocessing)
RAW_DIR = "../DataPenjualanMotor_raw"
RAW_FILE = "DataPenjualanMotor.csv"


def load_raw_data():
    path = os.path.join(RAW_DIR, RAW_FILE)
    print(f"Membaca data dari: {path}")
    df = pd.read_csv(path, sep=";")
    return df


def preprocess(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Melakukan preprocessing dasar pada data penjualan motor."""
    df = df_raw.copy()

    # Bersihkan kolom angka
    df["HARGA JUAL"] = (
        df["HARGA JUAL"].astype(str)
        .str.replace(".", "", regex=False)
        .astype("int64")
    )

    df["DISKON"] = (
        df["DISKON"].astype(str)
        .str.replace(".", "", regex=False)
        .astype("int64")
    )

    # Tanggal ke datetime
    df["TANGGAL"] = pd.to_datetime(
        df["TANGGAL"],
        format="%d-%b-%y",
        errors="coerce"
    )

    # Hapus duplikat
    df = df.drop_duplicates()

    return df


def save_processed(df: pd.DataFrame):
    # Simpan hasil preprocessing di folder ini (preprocessing)
    output_file = "DataPenjualanMotor_preprocessing.csv"
    df.to_csv(output_file, index=False)
    print(f"Data hasil preprocessing disimpan ke: {output_file}")


def main():
    df_raw = load_raw_data()
    df_clean = preprocess(df_raw)
    save_processed(df_clean)


if __name__ == "__main__":
    main()

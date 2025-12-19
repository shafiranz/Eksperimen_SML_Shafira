import os
import pandas as pd

# Daftar kandidat lokasi file raw (urutkan dari yang paling mungkin)
CANDIDATE_RAW_PATHS = [
    "DataPenjualanMotor_raw.csv",                    # file ada di root repo (punyamu di GitHub)
    "DataPenjualanMotor.csv",                        # kalau suatu saat kamu pakai nama ini
    os.path.join("preprocessing", "DataPenjualanMotor_raw.csv"),  # kalau filenya kamu taruh di folder preprocessing
    os.path.join("..", "DataPenjualanMotor_raw", "DataPenjualanMotor.csv"),  # struktur awalmu
]

def load_raw_data():
    # cari file yang benar-benar ada
    for path in CANDIDATE_RAW_PATHS:
        if os.path.exists(path):
            print(f"Membaca data dari: {path}")
            return pd.read_csv(path, sep=";")

    # kalau tidak ketemu, kasih error yang jelas + tampilkan isi folder untuk debugging
    cwd = os.getcwd()
    root_files = os.listdir(".")
    raise FileNotFoundError(
        "File dataset tidak ditemukan. Saya sudah mencoba:\n"
        + "\n".join([f"- {p}" for p in CANDIDATE_RAW_PATHS])
        + f"\n\nCurrent working dir: {cwd}\nFiles in repo root: {root_files}"
    )

def preprocess(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()

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

    df["TANGGAL"] = pd.to_datetime(
        df["TANGGAL"],
        format="%d-%b-%y",
        errors="coerce"
    )

    df = df.drop_duplicates()
    return df

def save_processed(df: pd.DataFrame):
    # simpan hasil di folder preprocessing (biar rapi & konsisten di CI)
    output_path = os.path.join("preprocessing", "DataPenjualanMotor_preprocessing.csv")
    df.to_csv(output_path, index=False)
    print(f"Data hasil preprocessing disimpan ke: {output_path}")

def main():
    df_raw = load_raw_data()
    df_clean = preprocess(df_raw)
    save_processed(df_clean)

if __name__ == "__main__":
    main()

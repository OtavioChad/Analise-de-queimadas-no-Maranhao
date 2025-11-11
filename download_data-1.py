# download_data.py
# Faz o download dos arquivos focos_br_ma_ref_2023.zip e focos_br_ma_ref_2024.zip do servidor COIDS (INPE)
import os, zipfile, urllib.request, io

BASE_URL = "https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/anual/EstadosBr_sat_ref/MA/"
FILES = ["focos_br_ma_ref_2023.zip", "focos_br_ma_ref_2024.zip"]

def download_and_extract_ma(target_folder="dados"):
    os.makedirs(target_folder, exist_ok=True)
    for fname in FILES:
        url = BASE_URL + fname
        print(f"Baixando {url} ...")
        try:
            resp = urllib.request.urlopen(url, timeout=60)
            data = resp.read()
        except Exception as e:
            print(f"Erro ao baixar {url}: {e}. Verifique conexão e tente novamente.")
            continue
        # Save zip to temp and extract CSV(s)
        try:
            zf = zipfile.ZipFile(io.BytesIO(data))
            for member in zf.namelist():
                if member.lower().endswith('.csv'):
                    out_path = os.path.join(target_folder, os.path.basename(member))
                    print(f"Extraindo {member} -> {out_path}")
                    with open(out_path, 'wb') as out_f:
                        out_f.write(zf.read(member))
        except Exception as e:
            print(f"Erro ao extrair {fname}: {e}")

if __name__ == '__main__':
    download_and_extract_ma()

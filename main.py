# Script extending results from https://github.com/sybila/bn-ck-analysis
import requests
import pandas as pd
import re
import os


SUPPLEMENTAL_INFO_FILE = '20200820_control_kernel_supplemental_info.csv'
OUTPUT_INFO_FILE = 'output.csv'


def download_cell_collective_bn(model_id):
    os.makedirs(f'./models/sbml', exist_ok=True)
    model_file = f'./models/sbml/{model_id}.sbml'
    if os.path.exists(model_file):
        return

    url = f'https://cellcollective.org/api/model/{model_id}/export/version/1?type=SBML'
    print(f'Downloading from {url}')
    r = requests.get(url, allow_redirects=True)

    with open(model_file, 'wb') as file:
        file.write(r.content)


def convert_to_bnet(model_id):
    """
    Prerequisites: java 8 runtime, bioLQM release - https://github.com/colomoto/bioLQM/releases

    :param model_id: Cell collective's id of the model
    """
    os.makedirs(f'./models/bnet', exist_ok=True)
    source_model_file = f'./models/sbml/{model_id}.sbml'
    target_model_file = f'./models/bnet/{model_id}.bnet'
    if os.path.exists(target_model_file):
        return

    print(f'Converting model {model_id}')
    output = os.popen(f'java -jar bioLQM-0.6.1.jar {source_model_file} {target_model_file}').read()
    print(output)


if __name__ == '__main__':
    cc_url_id = re.compile('https:\/\/cellcollective.org\/#(\d+)[:\d]*\/.*')

    df_bn_data = pd.read_csv(SUPPLEMENTAL_INFO_FILE)

    df_bn_data['id'] = df_bn_data.apply(lambda row: re.match(cc_url_id, row['url to cell collective model']).group(1), axis=1)

    df_bn_data.apply(lambda row: download_cell_collective_bn(row['id']), axis=1)
    df_bn_data.apply(lambda row: convert_to_bnet(row['id']), axis=1)



    # df_bn_data.to_csv(OUTPUT_INFO_FILE)

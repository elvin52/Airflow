from datetime import datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.S3_hook import S3Hook
import pandas as pd
import matplotlib.pyplot as plt

def upload_to_s3(filepaths: list ,keys: list, bucket_name: str) -> None:
    try:
         hook = S3Hook('s3_conn')
         for filepath, key in zip(filepaths, keys):
             hook.load_file(filename=filepath, key=key, bucket_name=bucket_name)
    except Exception as e:
        print(f"Greška prilikom prijenosa podataka {str (e)}")

def analiza():
    music = pd.read_csv('D:/Users/elvin/Downloads/archive/mxmh_survey_results.csv')

    zanr = music.groupby('Fav genre')

    anks = zanr['Music effects'].value_counts()

    prosjek_najvecih = zanr[['Anxiety', 'Depression', 'Insomnia', 'OCD']].mean()

    std_najvecih = zanr[['Anxiety', 'Depression', 'Insomnia', 'OCD']].std()

    bolje = zanr['Music effects'].value_counts()

    prosjek_najvecih.to_csv('D:/Users/elvin/Downloads/archive/prosjek.csv', index=False)

    std_najvecih.to_csv('D:/Users/elvin/Downloads/archive/std.csv', index=False)

    bolje.to_csv('D:/Users/elvin/Downloads/archive/efekt_muzike.csv', index=False)

    prosjek_najvecih.plot(kind='bar', figsize=(10, 6))
    plt.title('Mean Scores by Genre')
    plt.xlabel('Genre')
    plt.ylabel('Mean Score')
    plt.xticks(rotation=45)
    plt.savefig('prosjek.png')
    plt.show()


    std_najvecih.plot(kind='bar', figsize=(10, 6))
    plt.title('Standard Deviation of Scores by Genre')
    plt.xlabel('Genre')
    plt.ylabel('Standard Deviation')
    plt.xticks(rotation=45)
    plt.savefig('std.png')
    plt.show()

    bolje.plot(kind='bar', figsize=(10, 6))
    plt.title('Efekti muzike na mentalno stanje po žanru')
    plt.xlabel('Genre')
    plt.ylabel('Efekti muzike')
    plt.xticks(rotation=45)
    plt.savefig('efekti.png')
    plt.show()

with DAG(
    dag_id='s3_dag',
    schedule_interval='@daily',
    start_date=datetime(2022, 7, 1),
    catchup=False
) as dag:

    task_upload_to_s3 = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3,
        op_kwargs={
            'filepaths': [
                'D:/Users/elvin/Downloads/archive/prosjek.csv',
                'D:/Users/elvin/Downloads/archive/std.csv',
                'D:/Users/elvin/Downloads/archive/efekt_muzike.csv'
            ],
            'keys': [
                'top50MusicFrom2010-2019/prosjek.csv',
                'top50MusicFrom2010-2019/std.csv',
                'top50MusicFrom2010-2019/efekt_muzike.csv'
            ],
            'bucket_name': 'mojipodaci'
        }
    )


analiza()
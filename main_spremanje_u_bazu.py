from datetime import datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.S3_hook import S3Hook
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
import sqlalchemy


def upload_to_s3(filepaths: list ,keys: list, bucket_name: str) -> None:
    try:
         hook = S3Hook('s3_conn')
         for filepath, key in zip(filepaths, keys):
             hook.load_file(filename=filepath, key=key, bucket_name=bucket_name)
    except Exception as e:
        print(f"Greška prilikom prijenosa podataka {str (e)}")

def analiza():
    engine = sqlalchemy.create_engine("postgresql+psycopg2://postgres:elvin@localhost:5432/analiza")

    music = pd.read_csv('D:/Users/elvin/Downloads/archive/mxmh_survey_results.csv')

    music = music[[  # 'Timestamp',
        'Age',
        # 'Primary streaming service',
        'Hours per day',
        # 'While working', 'Instrumentalist', 'Composer',
        'Fav genre',
        # 'Exploratory', 'Foreign languages', 'BPM', 'Frequency [Classical]',
        # 'Frequency [Country]', 'Frequency [EDM]', 'Frequency [Folk]',
        # 'Frequency [Gospel]', 'Frequency [Hip hop]', 'Frequency [Jazz]',
        # 'Frequency [K pop]', 'Frequency [Latin]', 'Frequency [Lofi]',
        # 'Frequency [Metal]', 'Frequency [Pop]', 'Frequency [R&B]',
        # 'Frequency [Rap]', 'Frequency [Rock]', 'Frequency [Video game music]',
        'Anxiety', 'Depression', 'Insomnia', 'OCD', 'Music effects',
        # 'Permissions'
    ]].copy()

    # dataframeovi koji sluze kao tablice za bazu

    music['participant_id'] = music.index
    user = music[['participant_id', 'Age', 'Fav genre']]

    mental = music[['Anxiety', 'Depression', 'Insomnia', 'OCD', 'Music effects']]
    mental['mental_id'] = mental.index

    zanr = music.groupby('Fav genre')

    bins = [0, 25, 40, 60, float('inf')]
    labels = ['0-25', '25-40', '40-60', '60+']

    music['Dob'] = music['Age'] = pd.cut(music['Age'], bins=bins, labels=labels, right=False)
    age_genre_counts = music.groupby('Dob')['Fav genre'].value_counts().groupby(level=0).nlargest(1)


    prosjek_std = zanr[['Anxiety', 'Depression', 'Insomnia', 'OCD']].agg(['mean', 'std'])

    user.to_sql('Users', engine)
    mental.to_sql('Mental_states', engine)

    bolje = zanr['Music effects'].value_counts()

    prosjek_std.to_csv('D:/Users/elvin/Downloads/archive/prosjek.csv', index=False)
    bolje.to_csv('D:/Users/elvin/Downloads/archive/efekt_muzike.csv', index=False)

    bolje.plot(kind='bar', figsize=(10, 6))
    plt.title('Efekti muzike na mentalno stanje po žanru')
    plt.xlabel('Žanr')
    plt.ylabel('Efekti muzike')
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.35)
    plt.savefig('efekti.png')
    plt.show()

    prosjek_std.plot(kind='bar', figsize=(15, 5))
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
                'D:/Users/elvin/Downloads/archive/efekt_muzike.csv'
            ],
            'keys': [
                'top50MusicFrom2010-2019/prosjek.csv',
                'top50MusicFrom2010-2019/efekt_muzike.csv'
            ],
            'bucket_name': 'mojipodaci'
        }
    )
    

analiza()
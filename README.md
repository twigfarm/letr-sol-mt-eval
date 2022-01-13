# letr-sol-mt-eval

## 번역기 품질 평가
  
기계번역의 품질은 아직 완벽하지 않으며, 기계번역 서비스 이용자는 최적의 번역문을 얻기 위해 여러 번역기의 반환 결과를 비교함으로써 번역 품질을 스스로 평가해보아야 합니다. 기계 번역의 품질 평가에 대해서는 대해 다양한 논의가 이루어져 왔으며, 학자마다 다양한 평가 기준을 제시 및 사용하고 있습니다. 출발어 및 도착어의 언어적 특성, 처리 속도, 인간에 의한 평가 결과와의 상관관계 등을 고려해 최적의 번역 품질 척도를 선정 및 활용할 필요가 있습니다. 이는 한영 기계번역을 활용하는 한국인 사용자의 서비스 만족도를 높이는 데 기여할 것입니다.  

## Dependency
사용에 필요한 dependency는 아래와 같이 git clone 후 설치합니다.
~~~
git clone https://github.com/twigfarm/letr-sol-mt-eval
cd letr-sol-mt-eval
pip install -r requirements.txt
~~~

## 하이퍼파라미터 및 경로 설정
각종 경로 및 데이터를 나눌 비율, 학습 에포크 설정 등은 ```config/config.yml```을 통해 진행합니다.

- ```data_path```: 학습에 사용되는 데이터 경로 (default: data/sample.xlsx)
- ```split_ratio```: 학습 데이터셋을 나눌 비율 (default: 0.3)
- ```epochs```: 학습시 에포크 수 (default: 50)
- ```model_path```: 학습 후 저장되는 모델 폴더 (default: models/)
- ```user_data_path```: 추론에 사용되는 데이터 경로 (default: data/test.xlsx)
- ```use_vanilla```: 추론 때 훈련된 모델이 아닌, 기본(vanilla) 모델을 사용할지 여부 (default: False)

## HTER 스코어링 및 해당 척도의 타당성 평가
번역기별 기계번역문과, 이에 대한 Post-Edited 기계번역문 쌍이 포함된 데이터셋을 준비합니다. HTER 스코어링을 진행 후, BLEU, chrF, METEOR, hLEPOR, RIBES, BLEURT 등 reference-based 척도와의 Pearson's r 상관계수를 구하여 HTER 척도의 타당성을 평가합니다. 이때 상관계수 산출은 ```scipy.stats.pearsonr()``` 메소드를 활용합니다. 상세정보는 ```HTER_sanity_check.ipynb```를 참고해주세요.

## 데이터
### Training 데이터
학습에 사용되는 데이터는 아래의 형태를 가집니다. 샘플 데이터는 ```data/sample.xlsx```를 참고해주세요.

|source|target|score|
|------|---|---|
|그게 1달러가 팔천 한 삼백 원 됩니다.|That's about eight thousand and three hundred one for a dollar.|54.5454545454545|
|이후 수행단이 함께 참석하는 만찬이 이어질 예정이다.|Afterwards, a dinner with the entourage will be held.|44.4444444444444|
|특히 화장품 판매직 사원은 그 정도가 심하다.|It is especially severe for cosmetics salespeople.|0|

  - ```source```: 원문
  - ```target```: 원문에 대한 번역문
  - ```score```: 번역문 점수
  

### Test 데이터
Training이 완료되었다면, 완료된 모델을 이용하여 사용자가 입력하는 원문-번역문 간의 점수를 부여할 수 있습니다. 샘플 데이터는 ```data/test.xlsx```를 참고해주세요.

|source|target|
|------|---|
|그게 1달러가 팔천 한 삼백 원 됩니다.|That's about eight thousand and three hundred one for a dollar.|
|이후 수행단이 함께 참석하는 만찬이 이어질 예정이다.|Afterwards, a dinner with the entourage will be held.|
|특히 화장품 판매직 사원은 그 정도가 심하다.|It is especially severe for cosmetics salespeople.|

점수는 ```scores``` 칼럼이 새롭게 만들어진 ```result.xlsx```로 저장됩니다.


## 학습 및 테스트
학습을 위해서는 본 레포지토리의 최상단 경로에서 아래의 코드를 실행시킵니다.
~~~
python train.py
~~~

학습이 완료되었다면, ```models```폴더에 모델이 저장됩니다.  
  
**이 모델**을 이용하여 추론을 진행하려면 아래의 코드를 실행시킵니다.  
단, 만약 파인튜닝된 모델이 아닌, **vanilla** 모델을 사용하시려면 ```config.yml```에서 ```use_vanilla```의 값을 ```True```로 설정한 후 아래의 코드를 실행시킵니다.
~~~
python main.py
~~~
테스트가 완료되었다면, ```data```폴더에 엑셀 형식의 ```results.xlsx```파일이 저장되고, 상기했듯 ```scores```칼럼에 점수가 저장됩니다.

# 결과
에포크 150으로 학습한 결과, HTER 점수에 대해 **0.2878**의 상관계수를 기록하였으며, 이때의 p-value는 **2.5011e-20**을 기록했습니다.

-----------------------------
```
letr-sol-mt-eval
│  .gitignore
│  data.py
│  main.py
│  README.md
│  requirements.txt
│  train.py
│
├─config
│      config.yml
│
├─data
│      sample.xlsx
│      test.xlsx
```

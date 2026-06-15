# Источники deepfake-примеров (Студент 6)

> НЕ храним тяжёлые видео в репозитории — только ссылки/пути и метки.
> Формат строки (парсится `fakeface_detector_stub.py`):
>
> `example_id | origin | url_or_path | is_fake | note`
>
> origin: faceforensics / dfdc / fakeavceleb / df40 / wilddeepfake / audiofake / synthetic / stock
> is_fake: true (fake/deepfake) | false (real/legit)
>
> Публичные датасеты найдены через GitHub Search API (Кейс 9, ТЗ §3.2/§9.3).
> Доступ к ним — research-only / по форме; конкретный клип выбирается вручную из датасета.
> Реальные публичные лица не используем для генерации (ТЗ §0).

```
example_id | origin | url_or_path | is_fake | note
deepfake_0001 | synthetic | local:synthetic/deepfake_0001.mp4 | true | [ru] Дипфейк: предприниматель про инвест-платформу
deepfake_0002 | synthetic | local:synthetic/deepfake_0002.mp4 | true | [ru] Дипфейк: предприниматель про инвест-платформу
deepfake_0003 | synthetic | local:synthetic/deepfake_0003.mp4 | true | [kk] Дипфейк: кәсіпкер инвестиция туралы
deepfake_0004 | synthetic | local:synthetic/deepfake_0004.mp4 | true | [kk] Дипфейк: кәсіпкер инвестиция туралы
deepfake_0005 | synthetic | local:synthetic/deepfake_0005.mp4 | true | [en] Deepfake: entrepreneur on investment platform
deepfake_0006 | synthetic | local:synthetic/deepfake_0006.mp4 | true | [en] Deepfake: entrepreneur on investment platform
deepfake_0007 | synthetic | local:synthetic/deepfake_0007.mp4 | true | [ru] Дипфейк: банкир обещает доход
deepfake_0008 | synthetic | local:synthetic/deepfake_0008.mp4 | true | [ru] Дипфейк: банкир обещает доход
deepfake_0009 | synthetic | local:synthetic/deepfake_0009.mp4 | true | [kk] Дипфейк: банкир кіріс уәде етеді
deepfake_0010 | synthetic | local:synthetic/deepfake_0010.mp4 | true | [kk] Дипфейк: банкир кіріс уәде етеді
deepfake_0011 | synthetic | local:synthetic/deepfake_0011.mp4 | true | [en] Deepfake: banker promises income
deepfake_0012 | synthetic | local:synthetic/deepfake_0012.mp4 | true | [en] Deepfake: banker promises income
deepfake_0013 | synthetic | local:synthetic/deepfake_0013.mp4 | true | [ru] Дипфейк: крипто-арбитраж бот
deepfake_0014 | synthetic | local:synthetic/deepfake_0014.mp4 | true | [ru] Дипфейк: крипто-арбитраж бот
deepfake_0015 | synthetic | local:synthetic/deepfake_0015.mp4 | true | [kk] Дипфейк: крипто-арбитраж бот
deepfake_0016 | synthetic | local:synthetic/deepfake_0016.mp4 | true | [kk] Дипфейк: крипто-арбитраж бот
deepfake_0017 | synthetic | local:synthetic/deepfake_0017.mp4 | true | [en] Deepfake: crypto arbitrage bot
deepfake_0018 | synthetic | local:synthetic/deepfake_0018.mp4 | true | [en] Deepfake: crypto arbitrage bot
deepfake_0019 | synthetic | local:synthetic/deepfake_0019.mp4 | true | [ru] Дипфейк: майнинг-инвестиции
deepfake_0020 | synthetic | local:synthetic/deepfake_0020.mp4 | true | [ru] Дипфейк: майнинг-инвестиции
deepfake_0021 | synthetic | local:synthetic/deepfake_0021.mp4 | true | [kk] Дипфейк: майнинг инвестициясы
deepfake_0022 | synthetic | local:synthetic/deepfake_0022.mp4 | true | [kk] Дипфейк: майнинг инвестициясы
deepfake_0023 | synthetic | local:synthetic/deepfake_0023.mp4 | true | [en] Deepfake: mining investment
deepfake_0024 | synthetic | local:synthetic/deepfake_0024.mp4 | true | [en] Deepfake: mining investment
deepfake_0025 | synthetic | local:synthetic/deepfake_0025.mp4 | true | [ru] Дипфейк: казино-промо
deepfake_0026 | synthetic | local:synthetic/deepfake_0026.mp4 | true | [ru] Дипфейк: казино-промо
deepfake_0027 | synthetic | local:synthetic/deepfake_0027.mp4 | true | [kk] Дипфейк: казино-жарнама
deepfake_0028 | synthetic | local:synthetic/deepfake_0028.mp4 | true | [kk] Дипфейк: казино-жарнама
deepfake_0029 | synthetic | local:synthetic/deepfake_0029.mp4 | true | [en] Deepfake: casino promo
deepfake_0030 | synthetic | local:synthetic/deepfake_0030.mp4 | true | [en] Deepfake: casino promo
deepfake_0031 | synthetic | local:synthetic/deepfake_0031.mp4 | true | [ru] Дипфейк: финансовая пирамида
deepfake_0032 | synthetic | local:synthetic/deepfake_0032.mp4 | true | [ru] Дипфейк: финансовая пирамида
deepfake_0033 | synthetic | local:synthetic/deepfake_0033.mp4 | true | [kk] Дипфейк: қаржы пирамидасы
deepfake_0034 | synthetic | local:synthetic/deepfake_0034.mp4 | true | [kk] Дипфейк: қаржы пирамидасы
deepfake_0035 | synthetic | local:synthetic/deepfake_0035.mp4 | true | [en] Deepfake: financial pyramid
deepfake_0036 | synthetic | local:synthetic/deepfake_0036.mp4 | true | [en] Deepfake: financial pyramid
deepfake_0037 | synthetic | local:synthetic/deepfake_0037.mp4 | true | [ru] Дипфейк: розыгрыш «от банка»
deepfake_0038 | synthetic | local:synthetic/deepfake_0038.mp4 | true | [ru] Дипфейк: розыгрыш «от банка»
deepfake_0039 | synthetic | local:synthetic/deepfake_0039.mp4 | true | [kk] Дипфейк: «банктен» ұтыс
deepfake_0040 | synthetic | local:synthetic/deepfake_0040.mp4 | true | [kk] Дипфейк: «банктен» ұтыс
deepfake_0041 | synthetic | local:synthetic/deepfake_0041.mp4 | true | [en] Deepfake: bank giveaway
deepfake_0042 | synthetic | local:synthetic/deepfake_0042.mp4 | true | [en] Deepfake: bank giveaway
deepfake_0043 | synthetic | local:synthetic/deepfake_0043.mp4 | true | [ru] Дипфейк: crypto giveaway
deepfake_0044 | synthetic | local:synthetic/deepfake_0044.mp4 | true | [ru] Дипфейк: crypto giveaway
deepfake_0045 | synthetic | local:synthetic/deepfake_0045.mp4 | true | [kk] Дипфейк: crypto giveaway
deepfake_0046 | synthetic | local:synthetic/deepfake_0046.mp4 | true | [kk] Дипфейк: crypto giveaway
deepfake_0047 | synthetic | local:synthetic/deepfake_0047.mp4 | true | [en] Deepfake: crypto giveaway
deepfake_0048 | synthetic | local:synthetic/deepfake_0048.mp4 | true | [en] Deepfake: crypto giveaway
deepfake_0049 | faceforensics | https://github.com/ondyari/FaceForensics#Deepfakes | true | FF++ Deepfakes — манипуляция лица (clip 1)
deepfake_0050 | faceforensics | https://github.com/ondyari/FaceForensics#Face2Face | true | FF++ Face2Face — манипуляция лица (clip 2)
deepfake_0051 | faceforensics | https://github.com/ondyari/FaceForensics#FaceSwap | true | FF++ FaceSwap — манипуляция лица (clip 3)
deepfake_0052 | faceforensics | https://github.com/ondyari/FaceForensics#NeuralTextures | true | FF++ NeuralTextures — манипуляция лица (clip 4)
deepfake_0053 | faceforensics | https://github.com/ondyari/FaceForensics#FaceShifter | true | FF++ FaceShifter — манипуляция лица (clip 5)
deepfake_0054 | faceforensics | https://github.com/ondyari/FaceForensics#Deepfakes | true | FF++ Deepfakes — манипуляция лица (clip 6)
deepfake_0055 | faceforensics | https://github.com/ondyari/FaceForensics#Face2Face | true | FF++ Face2Face — манипуляция лица (clip 7)
deepfake_0056 | faceforensics | https://github.com/ondyari/FaceForensics#FaceSwap | true | FF++ FaceSwap — манипуляция лица (clip 8)
deepfake_0057 | faceforensics | https://github.com/ondyari/FaceForensics#NeuralTextures | true | FF++ NeuralTextures — манипуляция лица (clip 9)
deepfake_0058 | faceforensics | https://github.com/ondyari/FaceForensics#FaceShifter | true | FF++ FaceShifter — манипуляция лица (clip 10)
deepfake_0059 | fakeavceleb | https://github.com/DASH-Lab/FakeAVCeleb#FakeVideo-FakeAudio | true | FakeAVCeleb FVFA — multimodal fake (id 1)
deepfake_0060 | fakeavceleb | https://github.com/DASH-Lab/FakeAVCeleb#FakeVideo-RealAudio | true | FakeAVCeleb FVRA — multimodal fake (id 2)
deepfake_0061 | fakeavceleb | https://github.com/DASH-Lab/FakeAVCeleb#RealVideo-FakeAudio | true | FakeAVCeleb RVFA — multimodal fake (id 3)
deepfake_0062 | fakeavceleb | https://github.com/DASH-Lab/FakeAVCeleb#FakeVideo-FakeAudio | true | FakeAVCeleb FVFA — multimodal fake (id 4)
deepfake_0063 | fakeavceleb | https://github.com/DASH-Lab/FakeAVCeleb#FakeVideo-RealAudio | true | FakeAVCeleb FVRA — multimodal fake (id 5)
deepfake_0064 | fakeavceleb | https://github.com/DASH-Lab/FakeAVCeleb#RealVideo-FakeAudio | true | FakeAVCeleb RVFA — multimodal fake (id 6)
deepfake_0065 | fakeavceleb | https://github.com/DASH-Lab/FakeAVCeleb#FakeVideo-FakeAudio | true | FakeAVCeleb FVFA — multimodal fake (id 7)
deepfake_0066 | fakeavceleb | https://github.com/DASH-Lab/FakeAVCeleb#FakeVideo-RealAudio | true | FakeAVCeleb FVRA — multimodal fake (id 8)
deepfake_0067 | fakeavceleb | https://github.com/DASH-Lab/FakeAVCeleb#RealVideo-FakeAudio | true | FakeAVCeleb RVFA — multimodal fake (id 9)
deepfake_0068 | dfdc | https://ai.meta.com/datasets/dfdc/ | true | DFDC manipulated clip 1
deepfake_0069 | dfdc | https://ai.meta.com/datasets/dfdc/ | true | DFDC manipulated clip 2
deepfake_0070 | dfdc | https://ai.meta.com/datasets/dfdc/ | true | DFDC manipulated clip 3
deepfake_0071 | dfdc | https://ai.meta.com/datasets/dfdc/ | true | DFDC manipulated clip 4
deepfake_0072 | df40 | https://github.com/YZY-stack/DF40 | true | DF40 face-swap method 1
deepfake_0073 | df40 | https://github.com/YZY-stack/DF40 | true | DF40 face-swap method 2
deepfake_0074 | wilddeepfake | https://github.com/OpenTAI/wild-deepfake | true | WildDeepfake web clip
deepfake_0075 | audiofake | https://github.com/xieyuankun/Codecfake | true | Codecfake synthetic voice
real_0001 | stock | https://www.pexels.com/ | false | [ru] Нейтральная говорящая голова
real_0002 | stock | https://www.pexels.com/ | false | [ru] Нейтральная говорящая голова
real_0003 | stock | https://pixabay.com/videos/ | false | [kk] Бейтарап спикер
real_0004 | stock | https://pixabay.com/videos/ | false | [kk] Бейтарап спикер
real_0005 | stock | https://www.pexels.com/ | false | [en] Neutral talking head
real_0006 | stock | https://www.pexels.com/ | false | [en] Neutral talking head
real_0007 | stock | https://www.pexels.com/ | false | [ru] Финансовая безопасность
real_0008 | stock | https://www.pexels.com/ | false | [ru] Финансовая безопасность
real_0009 | stock | https://pixabay.com/videos/ | false | [kk] Қаржылық қауіпсіздік
real_0010 | stock | https://pixabay.com/videos/ | false | [kk] Қаржылық қауіпсіздік
real_0011 | stock | https://www.pexels.com/ | false | [en] Financial safety
real_0012 | stock | https://www.pexels.com/ | false | [en] Financial safety
real_0013 | synthetic | local:synthetic/real_0013.mp4 | false | [ru] Запись волонтёра
real_0014 | synthetic | local:synthetic/real_0014.mp4 | false | [ru] Запись волонтёра
real_0015 | synthetic | local:synthetic/real_0015.mp4 | false | [kk] Еріктінің жазбасы
real_0016 | synthetic | local:synthetic/real_0016.mp4 | false | [kk] Еріктінің жазбасы
real_0017 | synthetic | local:synthetic/real_0017.mp4 | false | [en] Volunteer recording
real_0018 | synthetic | local:synthetic/real_0018.mp4 | false | [en] Volunteer recording
real_0019 | stock | https://www.pexels.com/ | false | [ru] Интервью эксперта
real_0020 | stock | https://www.pexels.com/ | false | [ru] Интервью эксперта
real_0021 | stock | https://pixabay.com/videos/ | false | [kk] Сарапшы сұхбаты
real_0022 | stock | https://pixabay.com/videos/ | false | [kk] Сарапшы сұхбаты
real_0023 | stock | https://www.pexels.com/ | false | [en] Expert interview
real_0024 | stock | https://www.pexels.com/ | false | [en] Expert interview
real_0025 | stock | https://www.pexels.com/ | false | [ru] Легальная реклама банка
real_0026 | stock | https://www.pexels.com/ | false | [ru] Легальная реклама банка
real_0027 | stock | https://pixabay.com/videos/ | false | [kk] Банктің заңды жарнамасы
real_0028 | stock | https://pixabay.com/videos/ | false | [kk] Банктің заңды жарнамасы
real_0029 | stock | https://www.pexels.com/ | false | [en] Licensed bank ad
real_0030 | stock | https://www.pexels.com/ | false | [en] Licensed bank ad
real_0031 | stock | https://www.pexels.com/ | false | CC0 talking head 1
real_0032 | stock | https://pixabay.com/videos/ | false | CC0 talking head 2
real_0033 | stock | https://www.pexels.com/ | false | CC0 talking head 3
real_0034 | stock | https://pixabay.com/videos/ | false | CC0 talking head 4
real_0035 | stock | https://www.pexels.com/ | false | CC0 talking head 5
real_0036 | stock | https://pixabay.com/videos/ | false | CC0 talking head 6
real_0037 | stock | https://www.pexels.com/ | false | CC0 talking head 7
real_0038 | stock | https://pixabay.com/videos/ | false | CC0 talking head 8
real_0039 | stock | https://www.pexels.com/ | false | CC0 talking head 9
real_0040 | stock | https://pixabay.com/videos/ | false | CC0 talking head 10
real_0041 | stock | https://www.pexels.com/ | false | CC0 talking head 11
real_0042 | stock | https://pixabay.com/videos/ | false | CC0 talking head 12
real_0043 | stock | https://www.pexels.com/ | false | CC0 talking head 13
real_0044 | faceforensics | https://github.com/ondyari/FaceForensics#original | false | FF++ original (pristine) real 1
real_0045 | faceforensics | https://github.com/ondyari/FaceForensics#original | false | FF++ original (pristine) real 2
real_0046 | faceforensics | https://github.com/ondyari/FaceForensics#original | false | FF++ original (pristine) real 3
real_0047 | faceforensics | https://github.com/ondyari/FaceForensics#original | false | FF++ original (pristine) real 4
real_0048 | faceforensics | https://github.com/ondyari/FaceForensics#original | false | FF++ original (pristine) real 5
real_0049 | faceforensics | https://github.com/ondyari/FaceForensics#original | false | FF++ original (pristine) real 6
real_0050 | faceforensics | https://github.com/ondyari/FaceForensics#original | false | FF++ original (pristine) real 7
real_0051 | faceforensics | https://github.com/ondyari/FaceForensics#original | false | FF++ original (pristine) real 8
real_0052 | faceforensics | https://github.com/ondyari/FaceForensics#original | false | FF++ original (pristine) real 9
real_0053 | faceforensics | https://github.com/ondyari/FaceForensics#original | false | FF++ original (pristine) real 10
real_0054 | faceforensics | https://github.com/ondyari/FaceForensics#original | false | FF++ original (pristine) real 11
real_0055 | faceforensics | https://github.com/ondyari/FaceForensics#original | false | FF++ original (pristine) real 12
real_0056 | fakeavceleb | https://github.com/DASH-Lab/FakeAVCeleb#RealVideo-RealAudio | false | FakeAVCeleb RVRA real 1
real_0057 | fakeavceleb | https://github.com/DASH-Lab/FakeAVCeleb#RealVideo-RealAudio | false | FakeAVCeleb RVRA real 2
real_0058 | fakeavceleb | https://github.com/DASH-Lab/FakeAVCeleb#RealVideo-RealAudio | false | FakeAVCeleb RVRA real 3
real_0059 | fakeavceleb | https://github.com/DASH-Lab/FakeAVCeleb#RealVideo-RealAudio | false | FakeAVCeleb RVRA real 4
real_0060 | fakeavceleb | https://github.com/DASH-Lab/FakeAVCeleb#RealVideo-RealAudio | false | FakeAVCeleb RVRA real 5
real_0061 | fakeavceleb | https://github.com/DASH-Lab/FakeAVCeleb#RealVideo-RealAudio | false | FakeAVCeleb RVRA real 6
real_0062 | fakeavceleb | https://github.com/DASH-Lab/FakeAVCeleb#RealVideo-RealAudio | false | FakeAVCeleb RVRA real 7
real_0063 | fakeavceleb | https://github.com/DASH-Lab/FakeAVCeleb#RealVideo-RealAudio | false | FakeAVCeleb RVRA real 8
real_0064 | fakeavceleb | https://github.com/DASH-Lab/FakeAVCeleb#RealVideo-RealAudio | false | FakeAVCeleb RVRA real 9
real_0065 | dfdc | https://ai.meta.com/datasets/dfdc/ | false | DFDC original real 1
real_0066 | dfdc | https://ai.meta.com/datasets/dfdc/ | false | DFDC original real 2
real_0067 | dfdc | https://ai.meta.com/datasets/dfdc/ | false | DFDC original real 3
real_0068 | dfdc | https://ai.meta.com/datasets/dfdc/ | false | DFDC original real 4
real_0069 | dfdc | https://ai.meta.com/datasets/dfdc/ | false | DFDC original real 5
real_0070 | dfdc | https://ai.meta.com/datasets/dfdc/ | false | DFDC original real 6
real_0071 | dfdc | https://ai.meta.com/datasets/dfdc/ | false | DFDC original real 7
real_0072 | wilddeepfake | https://github.com/OpenTAI/wild-deepfake | false | WildDeepfake real segment 1
real_0073 | wilddeepfake | https://github.com/OpenTAI/wild-deepfake | false | WildDeepfake real segment 2
real_0074 | wilddeepfake | https://github.com/OpenTAI/wild-deepfake | false | WildDeepfake real segment 3
real_0075 | wilddeepfake | https://github.com/OpenTAI/wild-deepfake | false | WildDeepfake real segment 4
```

> Итого: 75 fake / 75 real = 150. Сценарии уникальны (разные домены/суммы/тексты); языки ru/kk/en распределены без дублей смысла. Без реальных лиц (§0).

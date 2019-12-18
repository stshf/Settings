# Darknet Yolo train
## Compile
`Makefile`を編集
```bash
GPU=1
CUDNN=0
CUDNN_HALF=0
OPENCV=1
AVX=0
OPENMP=0
LIBSO=0
```
`GPU=1`, `OPENCV=1`
にしておく
```bash
make
```
`./darknet`が生成される
```
./darknet
```
を実行して
```bash
usage: ./darknet <function>
```
がでてくればMake完了

## Need

* `.data` file
```py
classes = [the number of classes]
train = [path for train.txt]
valid = [path for test.txt]
names = [path for .names file]
backup = [path for weight backup]
```

* train and test `.txt` file

```py
path for image file
...
```
label は image fileのディレクトリと同じ階層にlabel dirを作成しその中にいれる
* `.names` file
```py
can
bottle
case
```
各番号に対応したラベルの名前を順に書く

*  `.cfg`   
`/darknet/cfg/yolov3-voc.cfg`をコピー  
コピーした`yolov3-voc.cfg`を修正  
`classes = `  
` filters = `  
を修正  
`filters = masknum * (classes + 5)`
となるように修正
ex)
`classes = 3`  
`filters = 3 * (3 + 5) = 24`  
   - `classes`はファイル内全て(３つ)  
   - `filters`は`[yolo]`の一つ上の`[conbolutional]`内のみ(3つ)  
* `train/valid.txt`
データセットの場所を書いておく
```bash
/workspace/sample_pic/pic/sample_1.JPG
/workspace/sample_pic/pic/sample_2.JPG
/workspace/sample_pic/pic/sample_3_JPG
```
こんな感じ
`.JPG`, `.txt`は同じフォルダに置く

* Yolov3用の学習モデル初期値ファイルをダウンロード
```bash
wget https://pjreddie.com/media/files/darknet53.conv.74
```

## Training
```bash
./darknet detector train [path]/[name].data [path]/yolov3-voc.cfg darknet53.conv.74
```
Dockerコンテナ下などでは`-dont_show`をつけとく


## Test
```bash
./darknet detector test mydata/sample.data mydata/yolov3-voc_test.cfg  mydata/backup/yolov3-voc_6000.weights /workspace/hashimoto_data/figs/1case/bento_08.JPG
```

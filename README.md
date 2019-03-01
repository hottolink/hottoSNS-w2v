## 日本語大規模SNS+Webコーパスによる分散表現モデル

### 概要
* 日本語大規模SNS+Webコーパス（以下，大規模SNSコーパス）から作成したword2vecによる分散表現を構築した
* 本分散表現モデル(以下，大規模SNSモデル）は下記登録フォームから登録した方のみに配布する

### 日本語大規模SNS+Webコーパス
* 日本語大規模SNS+Webコーパスとは，以下3種類の媒体から作成した超大規模コーパスである．
	1. SNSデータ
 	1. 日本語Wikipedia
 	2. 自動収集ウェブページ

* 超大規模である．量的には，英語NLPでしばしば利用される[English Gigaword](https://catalog.ldc.upenn.edu/ldc2011t07)を上回っている．
* 各媒体の規模は，SNSデータ > 自動収集ウェブページ  > 日本語Wikipedia の順である
* 適切な前処理および長単位志向の分かち書きを行ってあるため，語彙情報が豊富かつ応用向きである
    * 単語分散表現の語彙数は，約200万語である
* 各媒体について，以下4種類の処理を順に実施した
	i. 平文コーパスの収集・構築
	ii 前処理
	iii. 分かち書きコーパスの構築
	iv. 全媒体を統合，単語分散表現(Word2Vec)の学習

* データの性質上，本コーパスを配布することは差し控える
* 処理の詳細は，以下の節を参照のこと



### 利用方法
#### 実行確認環境
* Python 3.5.2
* Anaconda3 4.4.0
* gensim 3.4.0

#### 付属評価コードの利用方法
```
git clone [URL]
cd [DIR名]
sh setup.sh
corpus/以下にダウンロードしたhottolink_broadsnscorpus.tar.gzを配置
tar zxf corpus/hottolink_broadsnscorpus.tar.gz
python run_evaluate.py
```

#### モデルの読み込み方法
```
from gensim.models import KeyedVectors
from gensim.models import Word2Vec

file_w2v_hottolink = corpusdir + "w2v_all_vector200_win5_sgns0.vec"

model_hottolink = KeyedVectors.load_word2vec_format(file_w2v_hottolink, binary=False) 

# 類義語の出力
print(model_hottolink.wv.most_similar("ルンバ"))

# 2語の類似度の算出
print(model_hottolink.wv.similarity("尊い","気高い")

```

### 分散表現の性能評価
* 評価方法：
	* 日本語大規模SNSコーパスによる分散表現とWikipediaによる分散表現の性能を比較する
	* スコアの妥当性を検証するために，日本語大規模SNS分散表現と同様の方法で作成したWikipediaによる分散表現と東北大により公開されている[日本語Wikipedia エンティティベクトル](http://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/)の性能を比較する

* 評価指標：Speamanの順位相関係数

* 評価対象モデル
	* 大規模SNSモデル：
	* Wikipediaモデル（ホットリンク）
	* [Wikipediaモデル（東北大）](https://github.com/singletongue/WikiEntVec/releases/download/20181001/jawiki.word_vectors.200d.txt.gz)
		* 2018年10月1日版　単語のみの分散表現（200次元）を利用
		* jawiki.word_vectors.200d.txt.gz

* 正解データ：[日本語単語類似度・関連度データセット JWSAN](http://www.utm.inf.uec.ac.jp/JWSAN/)[猪原]
	* JWSAN-1400を利用：単語の分散表現の性能評価用に、単語ペアを厳選したデータセット

* 評価結果

|モデル|大規模SNS| Wikipedia（ホットリンク）  |　Wikipedia（東北大）|
|---|---|---|---|
|相関係数|0.548|0.478|0.472|

* 考察
	* Wikipediaのみで学習した2つのモデルと比較し，良い性能が得られている
	* Wikipediaのみが学習した2つのモデルがほぼ同程度の性能であるため，分散表現の学習手法は妥当であると推測される

[猪原] 猪原 敬介，内海 彰： 日本語類似度・関連度データセットの作成，言語処理学会第24回年次大会発表論文集，pp.1011-1014 (2018).


### コーパスの統計情報

####  平文コーパスの収集・構築
1. SNSデータ
	1. ブログ
		* 期間 : 2015年1月～2016年6月
		* 除外 : 弊社ロジックによりスパムと判定されたブログ記事

	2. Twitter
		* 期間 : 2016年に投稿されたデータの一部
		* 除外 : 
			1. 公式RT / 非公式RT : 
			2. 公式モバイルアプリ（Twitter for iPhone, Twitter for Android）以外からの投稿 : 
				* 目的はいずれも，ReTweet / スパムツイート / BOTツイート に起因する重複文の除外である
				* 投稿数は十分な量が確保できるので，精緻なフィルタを考える必要はない


2. 日本語Wikipedia
	* 時点 : 2015年11月23日(付のダンプファイル)
	* 除外 : 特になし

3. 自動収集ウェブページ
 	* 期間 : 2009年9月～2016年6月(=弊社が保有する全期間)
 	* 除外 : 特になし

#### 前処理
1. SNSデータ
	1. 	ブログ
		* 本文抽出 : HTMLタグを除去し，本文と思われる部分のみを抽出
		* 文字列正規化 : neologdn方式

	2. Twitter
		* 本文から除外 : ReTweetヘッダ / URL / メンションタグ / ハッシュタグ
		* 文字列正規化 : [mecab-ipadic-NEologdの方式](https://github.com/neologd/mecab-ipadic-neologd/wiki/Regexp.ja)
			* 実装は [Python::neologdn package](https://pypi.python.org/pypi/neologdn/) を使用した
		  以下，本方式のことを「neologdn方式」と略記する


2. 日本語Wikipedia
	* 本文抽出 : [WikiExtractor](https://github.com/attardi/wikiextractor)を使用して，タグ・テーブル等のメタ情報を除外
		* `WikiExtractor.py FILE -o DIR -b 10G --no-templates --filter_disambig_pages --escapedoc=false`
		* `<doc>` xmlタグの行および，見出し行を削除
	* 文字列正規化 : neologdn方式

3. 自動収集ウェブページ
	* 本文抽出 : HTMLタグを除去し，本文と思われる部分のみを抽出
	* 文字列正規化 : neologdn方式



#### 分かち書きコーパスの構築
1. SNSデータ
	1. Twitter
		* 分かち書き器 : Juman
			* 全角に変換して解析実施，解析結果を半角に変換
		* 最小形態素数 : 10 (形態素数が9以下の文は削除)
	2．ブログ
		* 分かち書き器 : MeCab + [mecab-ipadic-NEologd(2016年2月)](https://github.com/neologd/mecab-ipadic-neologd)
		* 最小形態素数 : 10 (形態素数が9以下の文は削除)

2. 日本語Wikipedia
	* 分かち書き器 : MeCab + [mecab-ipadic-NEologd(2016年2月)](https://github.com/neologd/mecab-ipadic-neologd)
	* 最小形態素数 : 5 (形態素数が4以下の文は削除)

3. 自動収集ウェブページ
    * 分かち書き器 : MeCab + [mecab-ipadic-NEologd(2016年2月)](https://github.com/neologd/mecab-ipadic-neologd)
	* 最小形態素数 : 10 (形態素数が9以下の文は削除)




#### 単語分散表現(Word2Vec)の学習
* Mikolov(2013)[^mikolov]，いわゆるWord2Vecに従って，単語分散表現を学習する
	* 実装は [Python::gensim package](http://radimrehurek.com/gensim/index.html) を使用した
* Word2Vecの学習パラメータは以下のとおりとした

	パラメータ|値
	----|----
	アルゴリズム|Word2Vec [CBOW,Skip-Gram]
	次元数|200
	最低単語頻度|10
	context window size|5
	負例サンプリング|25
	α(初期学習率)|0.025
	α(Context Distribution Smoothing)|0.75
	down-sanpling ratio|1e-5
	iteration|20
	単語表現|**ｗ**

[Mikolov]: Mikolov, T., and J. Dean. "Distributed representations of words and phrases and their compositionality." Advances in neural information processing systems (2013).

#### コーパスの規模
* 構築したコーパスの規模は，以下のとおりである

* 平文コーパス

	| 媒体      | 行数[Mil]        | ファイルサイズ[GB] |
	|-----------|-------------|--------------------|
	| SNSデータ  | 288  | 36.2                |
	| Wikipedia | 7  | 2.2                |
	| ウェブページ  | 126  | 25                |

* 分かち書きコーパス

	| 媒体      | 行数[Mil]        | ファイルサイズ[GB] |
	|-----------|-------------|--------------------|
	| SNSデータ   | 180  | 37.1                |
	| Wikipedia | 7  | 2.5                |
	| ウェブページ  | 95  | 28                |


* 分かち書きコーパスの統計量

	| 指標                  | 値          |
	|-----------------------|-------------|
	| 行数[Mil]               | 282  |
	| トークン数[Giga]      | 12         |
	| ユニークな形態素数    | 計量中   |
	| 　　うち，頻度10回以上 | 2,067,629   |



#### (参考)Twitterの分かち書きについて
* Twitterはくだけた文体が多いことから，通常の形態素解析器では分かち書きの性能が十分でないことが知られている
	* F値は，MeCab(IPADIC) = 90%前後，KyTea(BCCWJ+UniDic) = 92%程度 という報告がある[1,2]
	* KyTeaをTwitterコーパスで追加学習すると，95%程度まで向上させられる？[2]
	* Jumanは未知語モデルを搭載しているため，比較的頑健な処理ができるとされている[3]

	```
    [1] 北川善彬, 小町守. 深層ニューラルネットワークを利用した日本語単語分割.
	[2] 森信介. 多様なテキストの言語処理(招待講演). 第112回音声言語情報処理研究会 (SIG-SLP).  http://sig-slp.jp/2016-SLP-112.html
	[3] 笹野遼平, 黒橋禎夫, and 奥村学. "日本語形態素解析における未知語処理の一手法―既知語から派生した表記と未知オノマトペの処理―." 自然言語処理 21.6 (2014): 1183-1205.
	```

* このため，Twitterの分かち書き精度向上を目的として構築されたコーパス(Twitter Corpus)が存在する
    * 約1,000文の分かち書き・品詞付与を行ったデータセット

    ```
    大崎彩葉, 唐口翔平, 大迫拓矢, 佐々木俊哉, 北川善彬, 堺澤勇也, 小町守. Twitter 日本語形態素解析のためのコーパス構築.
    https://github.com/tmu-nlp/TwitterCorpus
	```
	
* そこで，実際にTwitterの本文を分かち書きを行い，いずれの方法が優れているかを簡単にテストした
	* 対象文 : 129文をランダム抽出
	* 形態素解析器および辞書・モデル : 以下の5種類
		1. MeCab + IPADIC
		2. MeCab + [mecab-ipadic-NEologd](https://github.com/neologd/mecab-ipadic-neologd)
		3. Juman
		4. KyTea + default(BCCWJ+UniDic)
		5. KyTea + Twitter Corpus(re-training)
	* 評価方法 : 文ごとに，分かち書き誤りが特に少ない方法に投票(複数投票可)
* 得票結果は以下のとおり．今次のテストでは，Jumanが最良という結果になった

	| Tokenizer | Dict / Model          | 得票数 |
	|-----------|-----------------------|--------|
	| MeCab     | ipadic                | 37     |
	| MeCab     | mecab-ipadic-NEologd  | 41     |
	| Juman     | default               | 47     |
	| KyTea     | default(BCCWJ+UniDic) | 16     |
	| KyTea     | twitter               | 14     |

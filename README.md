# hottoSNS-w2v: 日本語大規模SNS+Webコーパスによる単語分散表現モデル

## 概要
* 日本語大規模SNS+Webコーパス（以下，大規模SNSコーパス）から作成したword2vecによる単語分散表現を構築した
* 本単語分散表現モデル(以下，大規模SNSモデル）は下記登録フォームから登録した方のみに配布する
  * 利用規約は本README.mdの末尾に記載されている．またLICENSE.mdにも同じ内容が記載されている．

[登録フォーム](https://forms.office.com/Pages/ResponsePage.aspx?id=Zpu1Ffmdi02AfxgH3uo25PxaMnBWkvJLsXoQLeuzhoBUQlVKM0NQNVFGRUUzSVdJQjBTUFA5Vko4QSQlQCN0PWcu)

<img src="https://github.com/hottolink/hottoSNS-w2v/blob/master/images/QR_hottoSNS-w2v.png" width="128">

## 配布リソースに関する説明
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
	1. 平文コーパスの収集・構築
	1. 前処理
	1. 分かち書きコーパスの構築
	1. 全媒体を統合，単語分散表現(Word2Vec)の学習

* データの性質上，本コーパスを配布することは差し控える
  * 本コーパスにおいては，SNSサービスのユーザ名やURLなど，個人の特定につながる可能性があるメタデータは削除済みである
  * 構築した単語分散表現から元のコーパスを再現することは不可能である
* 処理の詳細は，以下の節を参照のこと


### ファイル構成

| モデル | ファイル名 |
|-----------|-----------------------|
| hottoSNS-w2vモデル | w2v_all_vector200_win5_sgns0.vec  |
| Wikipediaモデル（ホットリンク） | w2v_wiki_vector100_win5_sgns1.vec | 



### 利用方法
#### 実行確認環境
* Python 3.5.2
* Anaconda3 4.4.0
* gensim 3.4.0

#### 付属評価コードの利用方法
```
# リポジトリのClone
git clone https://github.com/hottolink/hottoSNS-w2v.git
cd hottoSNS-w2v

# 取得した分散表現ファイルを `corpus/` 以下に配置
cp [download_dir]/hottoSNS-w2v_20190301.tar.bz2 corpus

# 評価環境の構築・評価実行
# ※テキストファイルから分散表現を読み込むため、実行に時間がかかります。
sh setup.sh
python run_evaluate.py

```

#### モデルの読み込み方法
```
from gensim.models import KeyedVectors
from gensim.models import Word2Vec

corpusdir = "./corpus/"
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
	* hottoSNS-w2vモデル
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
			1. 公式RT / 非公式RT 
			2. 公式モバイルアプリ（Twitter for iPhone, Twitter for Android）以外からの投稿 
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


## 利用規約
同一の内容をLICENSE.mdに記述
```
第１条（定義）
本契約で用いられる用語の意味は、以下に定めるとおりとする。
（１）「本規約」とは、本利用規約をいう。
（２）「甲」とは、 株式会社ホットリンク（以下「甲」という）をいう。
（３）「乙」とは、本規約に同意し、甲の承認を得て、甲が配布する単語ベクトルデータを利用する個人をいう。
（４）「「本データ」とは、甲が作成した単語分散表現のデータ全部をいう。


第２条（利用許諾）
甲は、乙が本規約に従って本データを利用することを非独占的に許諾する。なお、甲及び乙は、本規約に明示的に定める以外に、乙に本データに関していかなる権利も付与するものではないことを確認する。


第４条（許諾の条件）
甲が乙に本データの利用を許諾する条件は、以下の通りとする。 
（１）利用目的： 日本語に関する学術研究・産業研究（以下「本研究」という）を遂行するため。
（２）利用の範囲： 乙及び乙が所属する研究グループ
（３）利用方法： 本研究のために本データを乙が管理するコンピューター端末またはサーバーに複製し、本データを分析・研究しデータベース等に保存した解析データ（以下「本解析データ」という）を得る。


第５条（利用申込）
１．乙は、甲が指定するウェブ上の入力フォーム（以下、入力フォーム）を通じて、乙の名前や所属、連絡先等、甲が指定する項目を甲に送信し、本データの利用について甲の承認を得るものとする。 なお、甲が承認しなかった場合、甲はその理由を開示する義務を負わない。
２．前項に基づき甲に申告した内容に変更が生じる場合、乙は遅滞なくこれを甲に報告し、改めて甲の承認を得るものとする。
３．乙が入力フォームを送信した時点で、乙は本規約に同意したものとみなされる。

第６条（禁止事項）
乙は、本データの利用にあたり、以下に定める行為をしてはならない。 
（１）本データ及びその複製物（それらを復元できるデータを含む）を譲渡、貸与、販売すること。また、書面による甲の事前許諾なくこれらを配布、公衆送信、刊行物に転載するなど前項に定める範囲を超えて利用し、甲または第三者の権利を侵害すること。  
（２）本データを用いて甲又は第三者の名誉を毀損し、あるいはプライバシーを侵害するなどの権利侵害を行うこと。
（３）乙及び乙が所属する研究グループ以外の第三者に本データを利用させること。
（４）本規約で明示的に許諾された目的及び手段以外にデータを利用 すること。

第７条（対価） 
本規約に基づく本データの利用許諾の対価は発生しない。

第８条（公表）
１．乙は、学術研究の目的に限り、本データを使用して得られた研究成果や知見を公表することができる。これらの公表には、本解析データや処理プログラムの公表を含む。
２．乙は、公表にあたっては、本データをもとにした成果であることを明記し、成果の公表の前にその概要を書面やメール等で甲に報告する。
３．乙は、論文発表の際も、本データを利用した旨を明記し、提出先の学会、発表年月日とともに論文の別刷りまたはコピー（電子的媒体を含む）を１部甲に提出するものとする。



第９条（乙の責任）
１．乙は、本データをダウンロードする為に必要な通信機器やソフトウェア、通信回線等の全てを乙の責任と費用で準備し、操作、接続等をする。
２．乙は、本データを本研究の遂行のみに使用する。
３．乙は、本データが漏洩しないよう善良な管理者の注意義務をもって管理し、乙のコンピューター端末等に適切な対策を施すものとする。
４．乙が、本研究を乙が所属するグループのメンバーと共同で遂行する場合、乙は、本規約の内容を当該グループの他のメンバーに遵守させるものとし、万一、当該他のメンバーが本規約に違反し甲又は第三者に損害を与えた場合は、乙はこれを自らの行為として連帯して責任を負うものとする。
５．甲が必要と判断する場合、乙に対して、本データの利用状況の開示を求めることができるものとし、乙はこれに応じなければならない。


第１０条（知的財産権の帰属）
甲及び乙は、本データに関する一切の知的財産権、本データの利用に関連して甲が提供する書類やデータ等に関する全ての知的財産権について、甲に帰属することを確認する。ただし、本データ作成の素材となった各文書の著作権は正当な権利を有する第三者に帰属する。

第１１条（非保証等）
１．甲は、本データが、第三者の著作権、特許権、その他の無体財産権、営業秘密、ノウハウその他の権利を侵害していないこと、法令に違反していないこと、本データ作成に利用したアルゴリズムに誤り、エラー、バグがないことについて一切保証せず、また、それらの信頼性、正確性、速報性、完全性、及び有効性、特定目的への適合性について一切保証しないものとし、瑕疵担保責任も負わない。
２．本データに関し万一、第三者から知的財産権侵害等の主張がなされた場合には、乙はただちに甲に対しその旨を通知し、甲に対する情報提供等、当該紛争の解決に最大限協力するものとする。


第１２条（違反時の措置） 
１．甲は、乙が次の各号の一つにでも該当した場合、甲は乙に対して本データの利用を差止めることができる。
（１）本規約に違反した場合
（２）法令に違反した場合
（３）虚偽の申告等の不正を行った場合
（４）信頼関係を破壊するような行為を行った場合
（５）その他甲が不適当と認めた場合
２．前項の規定は甲から乙に対する損害賠償請求を妨げるものではない。 
３．第１項に基づき、甲が乙に対して本データの利用の差し止めを求めた場合、乙は、乙が管理する設備から、本データ、本解析データ及びその複製物の一切を消去するものとする。

第１３条（甲の事情による利用許諾の取り消し）
１．甲は、その理由の如何を問わず、なんらの催告なしに、本データの利用許諾を停止することができるものとする。その際は、第１５条に基づき、乙は速やかに本データおよびその複製物の一切を消去または破棄する。 
２．前項の破棄、消去の対象に本解析データは含まない。


第１４条（利用期間）
１．乙による本データの利用可能期間は、第５条にもとづく甲の承認日より１年間とする。
２．乙が１年間を超えて本データの利用継続を希望する場合、第５条に基づく方法で再度利用申請を行うこととする。


第１５条（本契約終了後の措置等）
１．理由の如何を問わず、第１４条に定める利用期間が終了したとき、もしくは、本データの利用許諾が取り消しとなった場合、乙は本データおよびその複製物の一切を消去または破棄する。  
２．前項の破棄、消去の対象に本解析データは含まない。ただし、乙は、本解析データから本データを復元して再利用することはできないものとする。
３．第１０条、第１１条、第１５条から第１９条は、本契約の終了後も有効に存続する。

第１６条（権利義務譲渡の禁止）
乙は、相手方の書面による事前の承諾なき限り、本契約上の地位及び本契約から生じる権利義務を第三者に譲渡又は担保に供してはならない。

第１７条 （個人情報等の保護および法令遵守）
１．甲が取得した乙の個人情報は、別途定める甲２のプライバシーポリシーに従って取り扱われる。
２．甲は、サーバー設備の故障その他のトラブル等に対処するため、乙の個人情報を他のサーバーに複写することがある。

第１８条（準拠法）
本契約の準拠法は、日本法とする。

第１９条（管轄裁判所）
本契約に起因し又は関連して生じた一切の紛争については、東京地方裁判所を第一審の専属的合意管轄裁判所とする。

第２０条（協　議）
本契約に定めのない事項及び疑義を生じた事項は、甲乙誠意をもって協議し、円満にその解決にあたる。

第２１条（本規約の効力）
本規約は、本データの利用の関する一切について適用される。なお、本規約は随時変更されることがあるが、変更後の規約は特別に定める場合を除き、ウェブ上で表示された時点から効力を生じるものとする。
```


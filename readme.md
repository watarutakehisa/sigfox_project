# Sigfox_projectを実行することができるまで

1. python3を入れる（ローカルで動かすなら3系であればなんでもいいと思う）
2. pythonに必要なライブラリをインストール
3. mysqlをインストール
4. mysqlの初期設定を完了する

## 1. python3を入れる
OSによって違いが激しいのと多分みんな入れてると思うので省略。

## 2.pythonに必要なライブラリをインストール

- flask
- mysql-connector
この２つをインストールする、pipを使うなら

```
sudo pip3 install flask
sudo pip3 install mysql-connector
```

## 3.mysqlをインストール

これもOSによって違いが激しいため、省略。[これ](https://qiita.com/nooboolean/items/7efc5c35b2e95637d8c1)を参照。また、ユーザーを作る際に詰まったので[こちら](https://qiita.com/keisukeYamagishi/items/d897e5c52fe9fd8d9273)も参照

## 4.mysqlへのデータ格納の準備

mysqlサーバーを起動し、ルート権限でログインする。僕のMacだとこんな感じ。
```
mysql.server start
mysql -u root -p
```

ログインしたのちこのようにユーザー、データベースを作り初期設定を行う。
```
CREATE USER sigfox@localhost;
SET PASSWORD FOR sigfox@localhost='sigfoxuno';
CREATE DATABASE sigfoxdata;
GRANT ALL ON sigfoxdata.* TO sigfox@localhost;
```

これが終了したら、Githubにあげているsigfox_project/datastore/mysql-init.py を起動する。これで初期設定終わり！

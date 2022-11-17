Amazon EC2で、CentOS7環境でGromacsをインストールする。

> 操作方法の画像をもっと増やす。

## 0. AWSのアカウントを作成

クレジットカードの登録が必要。

## 1. EC2のインスタンスの生成

* c6g.4xlarge (Arm 16 cores)を選ぶ。足りなくなったらあとで停止後にtypeを変更できる。(これはありがたい)
* OSはUbuntu (GPUを使わない予定なので)
* 料金は1時間100円ぐらい。
* Key pairを作っておく。
* 起動までしばらくかかる。
* ホームのあるディスクの容量は標準で8 GBしかない。うち2.5 GBはシステムが埋めているので、残りは5.3 GB。これは足りないかも→16 GBに増やした。これでいく。

## 2. sshでログイン

* キーペア生成でできた.pemファイルの所在を手許の端末の~/.ssh/Configに書く。ユーザ名はubuntuとしておく。
```
Host  35.78.254.xxx
  HostName  35.78.254.xxx
  IdentityFile "/Users/.../ec2 gromacs.pem"
  User ubuntu
```
* sshでログイン。パスワードは聞かれない。

## 3. 必要物のインストール

### 3-1 aptのアップデート。
```
sudo apt update
```

### 3-2 Gromacs
```
sudo apt install gromacs
```

### 3-3 PyPI
Python 3。10があらかじめインストールされている.
```
sudo apt install python3-pip
```

### 3-4 GenIce
```
sudo pip install numpy genice2
```

## 4. Tutorialsの試行

コードを取得。
```
git clone https://github.com/vitroid/gromacs-usecases.git
```

せっかくなので、VSCodeでアクセスする。

New Window =>  "><" => "ssh ubuntu@35.78.254.100"の追加 => "Connect"

Terminalを開き、
```
cd Environment
make
```

* `-nt 4`: 1.4 ns/day。
* `-nt 8`: 2.6 ns/day。Apple M1より少し速い。wall timeは33秒。
* `-nt 16`: 5.7 ns/day。MPIx16になった。速い!
* `-nt 16 -ntomp 16`: 4.9 ns/day。こちらはOpenMPx16。

まだまだ伸びそうな感じ。

> MeltingPointでの実測も行うべし。

## 5. ユーザの作成

* ユーザ名はq1〜q10とする。
* パスワードは個別に設定する。

## 6. sshdの設定変更

* /etc/ssh/sshd_configを修正し、パスワードでログインできるようにする。

## 7. 事後の設定変更

インスタンスの停止後、以下のことが可能

* ディスクの増量
* CPUの増量(インスタンスタイプの変更)
* インストール済みのアプリ、設定などは停止では失われない。
